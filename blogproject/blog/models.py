from django.db import models
from django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
# Create your models here.
# @python_2_unicode_compatible
class Category(models.Model):
	'''
	Django要求模型必须继承models.Model,
	Categor 只需要一个简单的分类名字就可以啦
	CharField指定了分类名字的数据类型,是字符类型
	CharField的max_length制定了最大长度,超过这个长度的类名就不
	会存入数据库

	'''
	name = models.CharField(max_length=100,
			editable=True,unique=True,verbose_name='名称')
	def __str__(self):
		return self.name

	class Meta:
		verbose_name = '分类表'
@python_2_unicode_compatible
class Tag(models.Model):
	'''
	标签tag也比较简单,和category一样,
	'''
	name = models.CharField(max_length=100,
		editable=True,unique=True,verbose_name='名称')
	def __str__(self):
		return self.name
	class Meta:
		verbose_name = '标签表'
@python_2_unicode_compatible
class Post(models.Model):
	'''文章的数据表稍微复杂一点,主要是设计的字段多
	'''
	title = models.CharField(max_length=70,editable=True,verbose_name='标题')  #标题
	body = models.TextField(verbose_name='文章正文',
			editable=True)  #文章正文
	create_time = models.DateTimeField(verbose_name='创建时间'
			,editable=True)	#创建时间
	modified_time = models.DateTimeField(verbose_name='修改时间')	#最后一次修改时间
	excerpt = models.CharField(max_length=200,blank=True,verbose_name='摘要')	#文章摘要
	category = models.ForeignKey(Category,verbose_name='分类',on_delete=models.CASCADE,
		editable=True)	#文章分类
	tag = models.ManyToManyField(Tag,blank=True,verbose_name='标签')	#文章标签
	author = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE,
		editable=True)	#作者
	views = models.PositiveIntegerField(default=0)


	def __str__(self):
		return self.title
	def increase_views(self):
		self.views +=1
		self.save(update_fields=['views'])
	def save(self,*args,**kwargs):
		#如果没有填写摘要
		if not self.excerpt:
			md= markdown.Markdown(extensions=[
					'markdown.extensions.extra',
					'markdown.extensions.codehilite',
				])
			self.excerpt = strip_tags(md.convert(self.body))[:54]

		#
		super(Post,self).save(*args,**kwargs)
	def get_absolute_url(self):
		return reverse('blog:detail',kwargs={'pk':self.pk})
	class Meta:
		verbose_name = '文章信息表'
		ordering = ['-create_time','title']