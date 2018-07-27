from django.contrib.syndication.views import Feed
from .models import Post

class AllPostRssFeed(Feed):
	title = "Django博客学习网站"

	link='/'
	description = 'Django博客学习'

	def items(self):
		return Post.objects.all()
	def item_title(self,item):
		return '[%s]%s' % (item.category,item.title)

	def item_description(self,item):
		return item.body