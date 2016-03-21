
    # Created by: CJ
    # Date: 2/9/2016
    # Purpose: All views for the project are created in this page, separated by functional segment

from django.shortcuts import render, get_object_or_404, render_to_response
from .forms import UserLoginForm, NewUserAccountForm, NewAdminForm
from .forms import NewEventForm, NewActivityForm, NewSceneForm, NewSceneOptionForm, NextSceneForm
from .models import Users as umod
from .models import Admin as amod
from .models import Event as emod
from .models import Activity as act
from .models import Scene as scn
from .models import SceneOptions as scnopt
from .models import NextScene as nxtscn
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from array import array



# View for home/splash page
def home(request):
	# title = "Welcome"
	# if request.user.is_authenticated():
	title = "Welcome, %s" % (request.user)
	form = UserLoginForm(request.POST or None)
	if request.method=='Post':
		form = UserLoginForm(request.POST)
		print("you are the man!")
		if form.is_valid():
			user = authenticate(username=form.cleaned_data['username'], 
			password=form.cleaned_data['password'])
			print("You go this far at least")
		if user is not None:
			login(request,user)
			print("maybe just maybe.....")
		return HttpResponseRedirect("/activityDashboard/")

	#video 14/42 has alternate validation methods
	context = {
		"form": form,
		"title": title,
	}


	return render(request,"home.html", context)


#=================================User-related Functions===================================#
def userLogin(request):
	
	#video 14/42 has alternate validation methods
	state = "Please log in below..."
	username = ''
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				login(request, user)
				print("You're login")
				state = "Youre in"
				return HttpResponseRedirect("/activityDashboard/")
			else:
				print("Your account is broken")
		else:
			print("Your username and password were incorrect")

	context = {
	'state': state,
	'username':username,
	}

	return render(request, "userLogin.html", context)


def newUserLogin(request):
	# if request.method == 'POST':
	form = NewUserAccountForm(request.POST or None)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect("/activityDashboard/")
	else:
		form = NewUserAccountForm()

	context = {
		"form": form,
	}
	return render(request,"newUserLogin.html", context)



#=================================Admin-related Functions===================================#

#View for admin splash page
def adminDashboard(request):
	title = "Admin Dashboard"

	events = emod.objects.all().filter(adminID_id = 1)

	activities = act.objects.all().filter(adminID_id = 1)
	# activityID = act.objects.get(filter)

	context = {
		'title': title,
		'events': events,
		'activities': activities,
	}
	return render(request,"adminDashboard.html", context)



#=================================Event-related Functions===================================#

#Adding new events -- Will be used by admin
@requires_csrf_token
def newEventForm(request):
	title = "Create New Event"
	formtitle = "Create New Event"
	instruction = "Enter the event title, desired joincode, and your preference as to whether or not a user limit is to be enforced."
	form = NewEventForm(request.POST or None)

	#User/Admin values strictly for testing purposes right now
	user = umod.objects.get(userID=2)
	admin = amod.objects.get(adminID=1)

	if form.is_valid():
		print('gets inside form validation if')
		event = emod()
		event.userID_id = user.userID
		event.adminID_id = admin.adminID
		event.eventName = form.cleaned_data['eventName']
		event.joincode = form.cleaned_data['joincode']
		event.enforceUser = form.cleaned_data['enforceUser']
		event.save()
		print('gets past event creation .save command')
		context = {
			"saved Event information after creation"
		}
		return HttpResponseRedirect("/adminDashboard/")

	context = {
		"title" : title,
		"formtitle": formtitle,
		"instruction": instruction,
		"form": form,
	}
	return render(request, "createEvent.html", context)

def editEvent(request, id):
	#Edit Function
	title = "Edit Existing Event"
	formtitle = "Edit Existing Event"
	instruction = "Alter the event title, desired joincode, and your preference as to whether or not a user limit is to be enforced."

	event = emod.objects.get(eventID=id)
	data={'eventName': event.eventName, 'joincode': event.joincode, 'enforceUser': event.enforceUser}

	form = NewEventForm(request.POST or None, 
		initial=data)

	if form.is_valid():
		event.eventName = form.cleaned_data['eventName']
		event.joincode = form.cleaned_data['joincode']
		event.enforceUser = form.cleaned_data['enforceUser']
		event.save()
		context = {
			"saved Event information after creation"
		}
		return HttpResponseRedirect("/adminDashboard/")

	context = {
	"title" : title,
	"formtitle": formtitle,
	"instruction": instruction,
	"form": form,
	}
	return render(request, "editEvent.html", context)

#Function to delete selected event - no html page
#id is eventID from event
def deleteEvent(request, id):
	activityCount = act.objects.filter(eventID_id=id).count()

	#if activities exist for the event to be deleted, remove activities, then the event
	if activityCount > 0:
		activity = act.objects.filter(eventID_id=id)
		deleteActivity = activity
		deleteActivity.delete()
		deleteEvent = emod.objects.filter(eventID=id)
		deleteEvent.delete()
	else:
		deleteEvent = emod.objects.filter(eventID=id)
		deleteEvent.delete()

	return HttpResponseRedirect('/adminDashboard/')





#=================================Activity-related Functions===================================#

#View for activity dashboard
def activityDashboard(request):
	title = "Dashboard"

	activities = act.objects.all()
	# activityID = act.objects.get(filter)

	context = {
		'title': title,
		'activities': activities,
	}
	return render(request,"activityDashboard.html", context)


#View for activity dashboard
def activity(request, id):
	title = "Activity Information"

	activities = act.objects.get(activityID=id)
	scenes = scn.objects.all().filter(activityID_id = id).order_by('sceneID')

	# activityID = act.objects.get(filter)

	context = {
		'title': title,
		'activities': activities,
		'scenes': scenes,

	}
	return render(request,"activity.html", context)


#View for activity pages
def activityPage(request, id, *sc):
	title = "Activity"

	activity = get_object_or_404(act, activityID=id) #id here is the activityID

	#QuerySet and List of scenes associated with activity
	scene = scn.objects.all().filter(activityID_id=id).order_by('sceneID')
	sceneList = scene.values_list('sceneID', flat=True).distinct()

	#QuerySet and List of sceneTypes associated with activity
	scnType = scn.objects.all().filter(activityID_id=id).order_by('sceneType')
	scnTypeList = scene.values_list('sceneType', flat=True).distinct()

	#QuerySet and List of sceneOptions associated with scenes
	scnOptions = scnopt.objects.all().filter(sceneID_id__in=sceneList)
	scnOptionsList = scnOptions.values_list('soID', flat=True).distinct()

	#QuerySet and List of nextScenes associated with scene and sceneOptions
	nxtScene = nxtscn.objects.all().filter(sceneID_id__in=sceneList)
	nxtSceneList = nxtScene.values_list('nextSceneNumber', flat=True)

	context = {
		'title': title,
		'scene': scene,
		'activity': activity,
		'sceneList': sceneList,
		'scnType': scnType,
		'scnOptions': scnOptions,
		'nxtScene': nxtScene,
	}
	return render(request,"activityPage.html", context)


#Adding new activity
def newActivityForm(request, id):
	title = "Create New Activity"

	#hardcoding this as admin 1 until user authentication is complete
	admin = amod.objects.get(adminID=1)
	event = get_object_or_404(emod, eventID=id) #id here is the activityID

	formtitle = "Create New Activity for " + event.eventName
	instruction = "Enter the activity name and description, followed by the optional fields below: second administrator, user limit and ability to replay the activity."

	form = NewActivityForm(request.POST or None)

	if form.is_valid():
		activity = act()
		activity.adminID_id = admin.adminID
		activity.eventID_id = event.eventID
		activity.activityName = form.cleaned_data['activityName']
		activity.description = form.cleaned_data['description']
		activity.superUser = form.cleaned_data['superUser']
		activity.userLimit = form.cleaned_data['userLimit']
		activity.allowReplayActivity = form.cleaned_data['allowReplayActivity']
		activity.save()

		context = {
			"saved Activity information"
		}
		return HttpResponseRedirect("/adminDashboard/") #add activity url here when created.

	context = {
		"title": title,
		"formtitle": formtitle,
		"instruction": instruction,
		"form": form,
	}
	return render(request,"createActivity.html",context)


#View to edit selected activity
def editActivity(request, id): #id parameter is the activity ID passed by page
	title = "Edit Existing Activity"
	formtitle = "Edit Existing Activity"
	instruction = "Alter the activity-related data below. Click 'Submit' to save changes."

	activity = act.objects.get(activityID=id)
	data={'activityName': activity.activityName, 'description': activity.description, 'superUser': activity.superUser,
		'userLimit': activity.userLimit, 'allowReplayActivity': activity.allowReplayActivity}

	form = NewActivityForm(request.POST or None, 
		initial=data)

	if form.is_valid():
		activity.activityName = form.cleaned_data['activityName']
		activity.description = form.cleaned_data['description']
		activity.superUser = form.cleaned_data['superUser']
		activity.userLimit = form.cleaned_data['userLimit']
		activity.allowReplayActivity = form.cleaned_data['allowReplayActivity']
		activity.save()
		context = {
			"saved Activity information after update"
		}
		return HttpResponseRedirect("/adminDashboard/")

	context = {
	"title" : title,
	"formtitle": formtitle,
	"instruction": instruction,
	"form": form,
	}
	return render(request, "editActivity.html", context)


#Function to delete activity - no html page
def deleteActivity(request, id): #id is activityID from event
	#Delete Function

	deleteActivity = act.objects.filter(activityID=id)
	deleteActivity.delete()

	return HttpResponseRedirect('/adminDashboard/')





#=================================Scene-related Functions===================================#
#This includes scenes (NOT scene options and next scenes) for an activity.

def newSceneSetForm(request, id):
	activity = act.objects.get(activityID=id) #id here is the activityID for which the scenes will be made
	activityNum = str(id) #converts id to string for user in HttpResponseRedirect
	title = "Add Scenes to Activity"

	formtitle = "Create Scene Set for " + activity.activityName
	instruction = "[Insert instructions for scene here.]"

	sceneForm = NewSceneForm(request.POST or None)

	if sceneForm.is_valid():
		
		#sceneForm items
		scene = scn()
		scene.activityID_id = id #referring to the activity ID at the beginning of the function
		scene.instructionText = sceneForm.cleaned_data['instructionText']
		scene.sceneType = sceneForm.cleaned_data['sceneType']
		scene.allowReplayScene = sceneForm.cleaned_data['allowReplayScene']
		scene.save()

		context = {
			"saved Scene information"
		}
		return HttpResponseRedirect("/activity/"+activityNum+"/") #add sceneOption url here when created.

	context = {
		"title": title,
		"formtitle": formtitle,
		"instruction": instruction,
		"form": sceneForm,
		"activity": activity,
	}
	return render(request,"createSceneSet.html",context)





#=================================Scene-related Functions===================================#
#This includes scene options (NOT next scenes) for a scene.

def newSceneOptionSetForm(request, id):
	title = "Add Scene Options"

	formtitle = "Create Scene Options"
	instruction = "[Insert instructions for sceneoption.]"

	sceneOptionForm = NewSceneOptionForm(request.POST or None)

	if sceneOptionForm.is_valid():
		#sceneOptionForm items
		sceneOptions = scnopt()
		sceneOptions.sceneID = sceneOptionForm.cleaned_data['sceneID']
		sceneOptions.sceneText = sceneOptionForm.cleaned_data['sceneText']
		sceneOptions.save()

		context = {
			"saved scene option information"
		}
		return HttpResponseRedirect("//") #add activity url here when created.

	context = {
		"title": title,
		"formtitle": formtitle,
		"instruction": instruction,
		"form": sceneOptionForm,
	}
	return render(request,"newSceneOptionSetForm.html",context)





#=================================Scene-related Functions===================================#
#This includes next scene information for a scene.

def newNextSceneSetForm(request, id):
	title = "Add Scenes to Activity"

	formtitle = "Map Scenes and Scene Options"
	instruction = "[Insert instructions for nextscene creation here.]"

	nextSceneForm = NextSceneForm(request.POST or None)

	if nextSceneForm.is_valid():

		nextScene = nxtscn()
		nextScene.sceneOptionID = nextSceneForm.cleaned_data['sceneOptionID']
		nextScene.sceneID = nextSceneForm.cleaned_data['sceneID']
		nextScene.nextSceneNumber = nextSceneForm.cleaned_data['nextSceneNumber']
		nextScene.save()

		context = {
			"saved nextScene information"
		}
		return HttpResponseRedirect("//") #add activity url here when created.

	context = {
		"title": title,
		"formtitle": formtitle,
		"instruction": instruction,
		"form": nextSceneForm,
	}
	return render(request,"newNextSceneSetForm.html",context)











#This is going to show up at the bottom when they sign up as a user
#don't do/test this until user use cases are working
#*******************Haven't tested this as of (2/13/16)********************
def newAdminLogin(request):
	form = NewAdminForm(request.POST or None)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		context = {
			"saved Admin organization"
		}
		return HttpResponseRedirect("") #add admindashboard here when created

	context = {
		"form": form,
	}
	return render(request,"",context) #figure out how to add to userloginAccountform


#********************test form from tutorials; email sending doesn't work yet******************
#Not actually using this now but don't delete it yet.
def contact(request):
	form = ContactForm(request.POST or None)
	if form.is_valid():
		# for key in form.cleaned_data:
		# 	print (key)
		# 	print (form.cleaned_data.get(key))
		form_email = form.cleaned_data.get("email")
		form_message = form.cleaned_data.get("message")
		form_first_name = form.cleaned_data.get("first_name")
		print (form_email)
		
		subject = 'Site contact form'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email, 'courtney.llera@ymail.com']
		contact_message = "%s: %s via %s"%(
			form_first_name, 
			form_message, 
			form_email
			)
		send_mail (
			subject, 
			contact_message, 
			from_email, 
			to_email, 
			fail_silently=False
			)
		#have fail silently if you're doing it in prod

	context = {
		"form":form,
	}
	
	return render(request, "forms.html", context)



