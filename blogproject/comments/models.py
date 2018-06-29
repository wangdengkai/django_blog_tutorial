from django.db import models

# Create your models here.
class Comment(models.Model):
	name = models.CharField(max_length=100,verbose_name="姓名")
	email = models.EmailField(max_length=255,verbose_name="邮箱")
	url = models.URLField(blank=True,verbose_name="个人网站")
	text = models.TextField(verbose_name="评论主体")
	create_time = models.DateTimeField(auto_now_add=True,verbose_name="发表时间")
	post = models.ForeignKey('blog.Post')

	def __str__(self):
		return self.text[:20]

	class Meta:
		verbose_name = "评论表"
		ordering=['-create_time']