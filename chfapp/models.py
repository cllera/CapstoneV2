#The forms in forms.py will refer to models made here

from django.db import models

# Create your models here. 
# Structuring forms, mapping fields, storing in database table.

#class enables UserLogin (Not create account)
class UserForm(models.Model):
	#inherits from Model class
	username = models.CharField(max_length=10,default='',blank=False)
	password = models.CharField(max_length=10,default='',blank=False)
	# joincode = models.CharField(max_length=10,default='',blank=False, null=False)
	#timestamp = models.DateTimeField(auto_now_add=True, auto_now=False) for things that are only added once
	#updated = models.DateTimeField(auto_now_add=False, auto_now=True) for updating timestamps frequently

	def __str__(self): #python3 uses __str__
		return self.username

#not sure what to do with this for now.
class AdminForm(models.Model):
	#inherits from Model class
	first_name = models.CharField(max_length=10, default='',blank=False)
	last_name = models.CharField(max_length=10,default='',blank=False)
	username = models.CharField(max_length=10,default='',blank=False)
	password = models.CharField(max_length=10,default='',blank=False)
	email = models.EmailField()
	organization = models.CharField(max_length=50,default='',blank=False, null=True)
	#timestamp = models.DateTimeField(auto_now_add=True, auto_now=False) for things that are only added once
	#updated = models.DateTimeField(auto_now_add=False, auto_now=True) for updating timestamps frequently

	def __str__(self): #python3 uses __str__
		return self.email

#Users Table
class Users(models.Model):
	userID = models.IntegerField(primary_key=True)
	userName = models.CharField(max_length=20)
	password = models.CharField(max_length=20)
	firstName = models.CharField(max_length=30)
	lastName = models.CharField(max_length=30)
	email = models.EmailField(max_length=40)

	def __str__(self):
		return self.userName, self.password, self.firstName, self.lastName, self.email

#Admin Table
class Admin(models.Model):
	adminID = models.IntegerField(primary_key=True)
	userID = models.ForeignKey(Users)
	organization = models.CharField(max_length=100)

	def __str__(self):
		return self.organization

#Events Table
class Event(models.Model):
	eventID = models.IntegerField(primary_key=True)
	userID = models.ForeignKey(Users)
	adminID = models.ForeignKey(Admin)
	eventName = models.CharField(max_length=255,blank=False)
	joincode = models.CharField(max_length=50)
	enforceUser = models.NullBooleanField(null=True)

	def __str__(self):
		return self.eventName

class Activity(models.Model):
	activityID = models.IntegerField(primary_key=True)
	adminID = models.ForeignKey(Admin,related_name='adminOwner')
	eventID = models.ForeignKey(Event)
	activityName = models.CharField(max_length=100)
	description = models.CharField(max_length=255)
	superUser = models.IntegerField(blank = True)
	userLimit = models.IntegerField(blank = True)
	inactiveUsers = models.NullBooleanField(null=True)
	revisionState = models.NullBooleanField(null=True)
	allowReplayActivity = models.NullBooleanField(null=True)

	def __str__(self):
		return self.activityName, self.description

#Not sure if we even need this as a model but just in case
class ActivitySession(models.Model):
	userID = models.ForeignKey(Users)
	activityID = models.ForeignKey(Activity)
	startTime = models.DateTimeField()
	inactive = models.NullBooleanField(null=True)
	activityCompleted = models.NullBooleanField(null=True)
	class Meta:
		unique_together = (('userID', 'activityID', 'startTime'),)

	def __str__(self):
		return self.startTime

class Scene(models.Model):
	sceneID = models.IntegerField(primary_key=True)
	activityID = models.ForeignKey(Activity)
	instructionText = models.CharField(max_length=255)
	sceneType = models.NullBooleanField(null=True)
	allowReplayScene = models.NullBooleanField(null=True)

	def __str__(self):
		return self.instructionText, self.sceneType

class SceneOptions(models.Model):
	soID = models.IntegerField(primary_key=True)
	sceneID = models.ForeignKey(Scene)
	sceneText = models.CharField(max_length=500)
	class Meta: 
		unique_together=(('soID', 'sceneID'),)

	def __str__(self):
		return self.sceneText

class NextScene(models.Model):
	nextSceneID = models.IntegerField(primary_key=True)
	sceneOptionID = models.ForeignKey(SceneOptions,related_name='sceneOptionNS')
	sceneID = models.ForeignKey(SceneOptions,related_name='sceneNS')
	nextSceneNumber = models.IntegerField()
	weight = models.DecimalField(max_digits = 3, decimal_places=2)
	class Meta:
		unique_together=(('sceneOptionID', 'sceneID'))

	def __str__(self):
		return self.weight
