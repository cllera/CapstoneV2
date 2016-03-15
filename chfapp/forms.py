#must have models created in order to import into here
from django import forms
from django.forms import ModelForm
from .models import UserForm, Users, Admin, Event, Activity, Scene, SceneOptions, NextScene
from django.conf import settings

#Form appears when you choose to add user in the .../admin/createaccount page
class UserLoginForm(forms.ModelForm):
	class Meta:
		model = UserForm
		fields = ['username','password']
	#self = instance of form
	def clean_username(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		return username


#New User Form
class NewUserAccountForm(forms.ModelForm):
	class Meta:
		model = Users
		fields = ['userName','password','firstName','lastName','email']

	# def clean_all(self):
	# 	userName = self.cleaned_data.get('userName')
	# 	return userName


# class scenePassForm(forms.Form):
# 	sceneID = forms.IntegerField()
# 	choice = forms.ChoiceField()
# 	integerSelected = forms.IntegerField()

# 	def clean_sceneID(self):
# 		self.cleaned_data.get('sceneID')
# 		return sceneID

# 	def clean_choice(self):
# 		self.cleaned_data.get('choice')
# 		return choice

# 	def clean_integerSelected(self):
# 		self.cleaned_data.get('integerSelected')
# 		return integerSelected

class NewEventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ['eventName','joincode', 'enforceUser']

	def clean_event(self):
		return eventName, joincode, enforceUser

class NewActivityForm(forms.ModelForm):
	class Meta:
		model = Activity
		fields = ['activityName','description','superUser','userLimit','allowReplayActivity']

	def clean_activity(self):
		return activityName, description


# Not using these yet

class NewAdminForm(forms.ModelForm):
	class Meta:
		model = Admin
		fields = ['organization']

	def clean_organization(self):
		organization = self.cleaned_data.get('organization')
		return organization


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




