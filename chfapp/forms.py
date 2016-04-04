#must have models created in order to import into here
from django import forms
from django.forms import ModelForm
from .models import UserForm, User, Admin, Event, Activity, Scene, SceneOptions, NextScene
from django.conf import settings
from django.contrib.auth.models import User


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
		model = User
		fields = ['username','password','first_name','last_name','email']
		widgets = {
		'password': forms.PasswordInput(),
		}

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

class NewSceneForm(forms.ModelForm):
	# instructionText = forms.CharField(label='Instructions')
	# sceneType = forms.NullBooleanField(
	# 	label="Scene Type",
	# 	required=False,
	# 	widget=Select(choices=[(None, "Start"),
	# 							(False, "Normal"),
	# 							(True, "Ending")]),
	# 	help_text="Choose scene type",
	# 	)
	# allowReplayScene = forms.NullBooleanField(
	# 	label="Replayable scene?",
	# 	required=False,
	# 	widget=Select(choices=[(None, ""),
	# 							(False, "No"),
	# 							(True, "Yes")]),
	# 	help_text="Will scene be replayable?",
	# 	)
	class Meta:
		model = Scene
		fields = ['instructionText','sceneType', 'allowReplayScene']
		# fields=[instructionText,sceneType,allowReplayScene]

	def clean_scene(self):
		return instructionText, sceneType, allowReplayScene

class NewSceneOptForm(forms.Form):
	From = forms.IntegerField()
	Option = forms.CharField(widget=forms.Textarea)
	To = forms.IntegerField()


class joinForm(forms.Form):
	jcode = forms.CharField(widget=forms.Textarea)



		








# Not using these yet
class NewAdminForm(forms.ModelForm):
	class Meta:
		model = Admin
		fields = ['organization']

	def clean_organization(self):
		organization = self.cleaned_data.get('organization')
		return organization







