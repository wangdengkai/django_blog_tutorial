from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Post,Category,Tag
from comments.forms import CommentForm
import markdown
# Create your views here.
def index(request):
	post_list = Post.objects.all()

	tag_list = Tag.objects.all()
	return render(request,'blog/index.html',locals())

def detail(request,pk):
	post = get_object_or_404(Post,pk=pk)
	post.body = markdown.markdown(post.body,
				extensions=[		#为markdown语法扩展
					'markdown.extensions.extra',  #包含很多扩展
					'markdown.extensions.codehilite', #语法高亮扩展
					'markdown.extensions.toc',   #自动生成目录扩展
				])
	form = CommentForm()
	comment_list=post.comment_set.all()
	context={
		'post':post,
		'form':form,
		'comment_list':comment_list
	}
	return render(request,'blog/detail.html',context=context)

def archives(request,year,month):
	post_list = Post.objects.filter(create_time__year=year,
									create_time__month=month
									)
	
	return render(request,'blog/index.html',locals())


def category(request,pk):
	cate = get_object_or_404(Category,pk=pk)

	post_list=Post.objects.filter(category=cate)

	return render(request,'blog/index.html',locals())

def about(request):
	return render(request,'blog/about.html')
def contact(request):
	return render(request,'blog/contact.html')
