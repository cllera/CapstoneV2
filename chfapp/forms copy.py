#must have models created in order to import into here
from django import forms
from .models import UserForm, Users, Admin, Event, Activity, Scene, SceneOptions, NextScene
from django.conf import settings

#form that doesn't need a model; literally no use case I can think of now for it, but 
#just in case let's keep it here for now.
class ContactForm(forms.Form):
	first_name = forms.CharField(required=False)
	email = forms.EmailField()
	message = forms.CharField()

	# def cleaned_data(self):
	# 	email = self.cleaned_data.get('email')
	# 	first_name = self.cleaned_data.get('first_name')
	# 	message = self.cleaned_data.get('message')
	# 	return email, first_name, message
	# 	print ('GOT HERE')

#Form appears when you choose to add user in the .../admin/createaccount page
class UserLoginForm(forms.ModelForm):
	class Meta:
		model = UserForm
		fields = ['username','password','joincode']
	#self = instance of form
	def clean_username(self):
		username = self.cleaned_data.get('username')
		# email_base, provider = email.split("@")
		# domain, extension = provider.split('.')
		# if not extension == "edu":
		# 	raise forms.ValidationError("Please use an academic email address.")
		return username

	def clean_joincode(self):
		joincode = self.cleaned_data.get('joincode')
		return joincode

#New User Form
class NewUserAccountForm(forms.ModelForm):
	class Meta:
		model = Users
		fields = ['userName','password','firstName','lastName','email']

	def clean_all(self):
		userName = self.cleaned_data.get('userName')
		return userName

class NewAdminForm(forms.ModelForm):
	class Meta:
		model = Admin
		fields = ['organization']

	def clean_organization(self):
		organization = self.cleaned_data.get('organization')
		return organization

class NewEventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ['eventName','joincode']

	def clean_event(self):
		return eventName, joincode

class NewActivityForm(forms.ModelForm):
	class Meta:
		model = Activity
		fields = ['activityName','description','superUser','userLimit','allowReplayActivity']

	def clean_activity(self):
		return activityName, description

class NewSceneForm(forms.ModelForm):
	class Meta:
		model = Scene
		fields = ['instructionText','allowReplayScene']

	def clean_scene(self):
		return instructionText, allowReplayScene

class NewSceneOptionForm(forms.ModelForm):
	class Meta:
		model = SceneOptions
		fields = ['sceneText']

	def clean_sceneOption(self):
		return sceneText

class NextSceneForm(forms.ModelForm):
	class Meta:
		model = NextScene
		fields = ['sceneID']

	def clean_sceneOption(self):
		return sceneID




