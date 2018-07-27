from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Post,Category,Tag
from comments.forms import CommentForm
import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.generic import ListView
from django.views.generic import DetailView
from django.db.models import Q
# Create your views here.
# def index(request):kk
# 	post_list = Post.objects.all()

# 	tag_list = Tag.objects.all()
# 	return render(request,'blog/index.html',locals())
class IndexView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
	paginate_by=2

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')
		pagination_data = self.pagination_data(paginator,page,is_paginated)

		context.update(pagination_data)

		return context
	def pagination_data(self,paginator,page,is_paginated):
		if not is_paginated:
			return {}
		left = []
		right = [ ]
		left_has_more = False
		right_has_more =False
		first = False
		last=False
		page_number = page.number
		total_pages = paginator.num_pages
		page_range=paginator.page_range
		if page_number == 1:
			right = page_range[page_number:page_number+1]
			if right[-1] < total_pages -1:
				right_has_more = True
			if right[-1] < total_pages:
				last=True
		elif page_number == total_pages:
			left = page_range[(page_number - 2 ) if (page_number -2) > 0 else 0:page_number -1]
			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True
		else:
			left = page_range[(page_number - 2 ) if (page_number -2) > 0 else 0:page_number -1]
			right = page_range[page_number:page_number+1]
			if right[-1] < total_pages -1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True
			if left[0] > 2:
				left_has_more = True
			if left[0]>1:
				first = True

		data={
			'left':left,
			'right':right,
			'left_has_more':left_has_more,
			'right_has_more':right_has_more,
			'first':first,
			'last':last,
		}
		return data 
# def detail(request,pk):
# 	post = get_object_or_404(Post,pk=pk)
# 	post.increase_views()
# 	post.body = markdown.markdown(post.body,
# 				extensions=[		#为markdown语法扩展
# 					'markdown.extensions.extra',  #包含很多扩展
# 					'markdown.extensions.codehilite', #语法高亮扩展
# 					'markdown.extensions.toc',   #自动生成目录扩展
# 				])
# 	form = CommentForm()
# 	comment_list=post.comment_set.all()
# 	context={
# 		'post':post,
# 		'form':form,
# 		'comment_list':comment_list
# 	}
# 	return render(request,'blog/detail.html',context=context)

# def archives(request,year,month):
# 	post_list = Post.objects.filter(create_time__year=year,
# 									create_time__month=month
# 									)
	
# 	return render(request,'blog/index.html',locals())
# 	
class PostDetailView(DetailView):
	model = Post
	template_name='blog/detail.html'
	context_object_name = 'post'

	def get(self,request,*args,**kwargs):
		response=super(PostDetailView,self).get(request,*args,**kwargs)
		self.object.increase_views()
		return response
	def get_object(self,queryset=None):
		post = super(PostDetailView,self).get_object(queryset=None)
		# post.body = markdown.markdown(
		# 					post.body,
		# 					extensions=[
		# 						'markdown.extensions.extra',
		# 						'markdown.extensions.codehilite',
		# 						'markdown.extensions.toc',
		# 					]
		# 			)
		md = markdown.Markdown(extensions=[
						'markdown.extensions.extra',
						'markdown.extensions.codehilite',
						# 'markdown.extensions.toc',
						TocExtension(slugify = slugify),
					])
		post.body = md.convert(post.body)
		post.toc = md.toc
		return post 
	def get_context_data(self,**kwargs):
		context = super(PostDetailView,self).get_context_data(**kwargs)
		form = CommentForm()
		comment_list = self.object.comment_set.all()
		tag_list = self.object.tag.all()
		context.update(
				{
				'form':form,
				'comment_list':comment_list,
				'tag_list':tag_list
				}
			)
		return context
class ArchivesView(IndexView):
	def get_queryset(self):
		return super(ArchivesView,self).get_queryset().filter(create_time__year=self.kwargs.get('year'),
														create_time__month=self.kwargs.get('month')
														)

# def category(request,pk):
# 	cate = get_object_or_404(Category,pk=pk)

# 	post_list=Post.objects.filter(category=cate)

# 	return render(request,'blog/index.html',locals())
class CategoryView(IndexView):
	def get_queryset(self):
		cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
		return super(CategoryView,self).get_queryset().filter(category=cate)
def about(request):
	return render(request,'blog/about.html')
def contact(request):
	return render(request,'blog/contact.html')
class TagView(IndexView):
	def get_queryset(self):
		tag=get_object_or_404(Tag,pk=self.kwargs.get('pk'))

		return super(TagView,self).get_queryset().filter(tag=tag)
	
def search(request):
	q = request.GET.get('q')
	error_msg = ''
	if not q:
		error_msg = "请输入关键字"
		return render(request,'blog/index.html',{'error_msg':error_msg})

	post_list = Post.objects.filter(Q(title__icontains=q)|Q(body__icontains=q))
	return render(request,'blog/index.html',{'error_msg':error_msg,
							'post_list':post_list})