from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.core.cache import cache

# Create your models here.

class UserSkill(models.Model):
	skill = models.CharField(max_length=200)
	
	def __str__(self):
		return self.skill

class UserProfile(models.Model):
	name = models.AutoField(primary_key=True)
	user_name = models.CharField(_('User Name'), max_length=200)
	age = models.IntegerField()
	
	CATEGORY = (('Male', 'Male'),
		('Female', 'Female'))
	gender = models.CharField(_('Gender'), max_length=100, choices=CATEGORY, null=True)

	image = models.ImageField(default="profile_image.png", null=True, blank=True)

	skill = models.ManyToManyField(UserSkill)
	date_created = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		if self.image:
			self.image = self.compressImage(self.image)
		super(UserProfile, self).save(*args, **kwargs)
		cache.delete('userprofile-%s' % (self.name))
	
	def compressImage(self, uploadedImage):
		imageTemproary = Image.open(uploadedImage)
		outputIoStream = BytesIO()
		imageTemproary = imageTemproary.resize((1280, 960))
		imageTemproary.save(outputIoStream , format='JPEG', quality=60)
		outputIoStream.seek(0)
		uploadedImage = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % uploadedImage.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
		return uploadedImage

	def __str__(self):
		return self.user_name


class PostImage(models.Model):
	parent = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	image = models.ImageField(upload_to="images/")
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.parent.user_name