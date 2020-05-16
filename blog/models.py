from django.db import models
from django.shortcuts import reverse

from django.utils.text import slugify
from time import time

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


def gen_slug(s):
	new_slug = slugify(s, allow_unicode=True)
	return new_slug + '-' + str(int(time()))


class Post(models.Model):
	title = models.CharField(max_length=50, db_index=True)
	slug = models.SlugField(max_length=150, blank=True, unique=True)
	short_description = models.CharField(max_length=200, blank=True, null=True)
	body = RichTextUploadingField(null=True, blank=True)
	tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
	date_pub = models.DateTimeField(auto_now_add=True)

	def get_absolute_url(self):
		return reverse('post_detail_url', kwargs={'slug': self.slug})

	def get_update_url(self):
		return reverse('post_update_url', kwargs={'slug':self.slug})

	def get_delete_url(self):
		return reverse('post_delete_url', kwargs={'slug':self.slug})

	def leave_comment_url(self):
		return reverse('leave_comment_url', kwargs={'slug':self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self.title)
		super().save(*args, **kwargs)
		
	def __str__(self):
		return self.title


class Tag(models.Model):
	title = models.CharField(max_length=50)
	slug = models.SlugField(max_length=50, blank=True, unique = True)

	def get_absolute_url(self):
		return reverse('tag_detail_url', kwargs={'slug':self.slug}) 

	def get_update_url(self):
		return reverse('tag_update_url', kwargs={'slug': self.slug})

	def get_delete_url(self):
		return reverse('tag_delete_url', kwargs={'slug': self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self.title)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.title


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
	comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, blank=True, related_name='comments_set')
	author = models.CharField(max_length=50)
	body = RichTextField(null=True, blank=True, config_name='comment_conf')
	date_pub = models.DateTimeField(auto_now_add=True)

	def get_absolute_url(self):
		return reverse('comment_create_url', kwargs={'slug': self.slug})

	def __str__(self):
		return f"{self.id} | {self.author}"

	class Meta:
		ordering = ['date_pub', 'author']
