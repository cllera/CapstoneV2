
    # Created by: CJ
    # Date: 2/9/2016
    # Purpose: All views for the project are created in this page, separated by functional segment

from django.shortcuts import render, get_object_or_404, render_to_response
from .forms import UserLoginForm, NewUserAccountForm, NewAdminForm, selectedEvent
from .forms import NewEventForm, NewActivityForm, NewSceneForm, NewSceneOptForm
from .models import Admin as amod
from .models import Event as emod
from .models import Activity as act
from .models import ActivitySession as actssn
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
from datetime import datetime
from django.contrib.auth.models import User


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

	# user = request.User

	if form.is_valid():
		instance = User.objects.create_user(username = form.cleaned_data['username'], 
			password = form.cleaned_data['password'], first_name = form.cleaned_data['first_name'], 
			last_name = form.cleaned_data['last_name'], email = form.cleaned_data['email'])
		instance.save()
		# u = User.objects.get(instance.username)
		# u.set_password(instance.password)
		# u.save()
		return HttpResponseRedirect("/userLogin/")
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

	user = request.user
	userID = user.id
	username = user.username
	print("//////////////////////////////////User and admin ID/////////////////////////////")
	print("UserID: " + str(userID))
	adminID = amod.objects.get(user_id=userID)
	print("AdminID: " + str(adminID))
	events = emod.objects.all().filter(adminID_id = adminID).order_by('eventID')
	print(events)
	eventsList = events.values_list('eventID', flat=True).distinct()
	print(eventsList)

	activities = act.objects.all().filter(adminID_id = adminID).order_by('eventID_id')
	print(activities)
	activitiesList = activities.values_list('eventID_id', flat=True)
	print(activitiesList)

	# create list of sessions
	
	# for a in activities:
	# 	session=actssn.objects.all().filter(activityID=a.activityID)
	# 	print("LOOK HERE for ACTIVITYIDs")
	# 	print(a.activityID)
	# 	context = {
	# 		'session': session,
	# 	}

	allUsers = User.objects.all()
	ses = actssn.objects.all()
	print("////here for ses")
	print(ses)

	context = {
		'title': title,
		'username': username,
		'events': events,
		'ses': ses,
		'activities': activities,
		'activitiesList': activitiesList,
		'allUsers': allUsers,
	}
	return render(request,"adminDashboard.html", context)





#=================================Event-related Functions===================================#


#View for event dashboard
def eventDashboard(request):
	title = "Events"

	events = emod.objects.all().filter(enforceUser=0) #Gathering all general events (no user account required)

	context = {
		'title': title,
		'events': events,
	}
	return render(request,"eventDashboard.html", context)

#Adding new events -- Will be used by admin
@requires_csrf_token
def newEventForm(request):
	title = "Create New Event"
	formtitle = "Create New Event"
	instruction = "Enter the event title, desired joincode, and your preference as to whether or not a user limit is to be enforced."
	form = NewEventForm(request.POST or None)

	#Admin values strictly for testing purposes right now
	user = request.user
	userID = user.id
	print("////////////////////////////////////")
	print(str(userID))
	admin = amod.objects.get(adminID=1)

	if form.is_valid():
		print('gets inside form validation if')
		print(str(userID))
		print(request.user.id)
		event = emod()
		event.user_id = userID
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
def activityDashboard(request, id):
	title = "Dashboard"
	currentuser = request.user
	# event = emod.objects.get(eventID=id)

	#gets only activities related to that event
	activities = act.objects.all().filter(eventID_id=id)


	context = {
		'title': title,
		'activities': activities,
		'currentuser': currentuser,
	}
	return render(request,"activityDashboard.html", context)


#Admin view for activity tasks; also includes some scene option and next scene functionality
def activity(request, id):
	title = "Activity Information"

	activities = act.objects.get(activityID=id) #id here is the activityID

	#QuerySet and List of scenes associated with activity
	scenes = scn.objects.all().filter(activityID_id = id).order_by('sceneID')
	sceneList = scenes.values_list('sceneID', flat=True).distinct()

	#Conversion of number of scenes to list, then array to be compared against sceneList
	sceneCount = len(sceneList)
	sceneCountList = list(range(sceneCount))
	for s in sceneCountList:
		sceneCountList[s] = sceneCountList[s] + 1


	#QuerySet and List of nextScenes associated with scene and sceneOptions
	nxtScene = nxtscn.objects.all().filter(sceneID_id__in=sceneList)
	nxtSceneList = nxtScene.values_list('nextSceneNumber', flat=True)


	#QuerySet and List of sceneOptions associated with scenes
	scnOptions = scnopt.objects.all().filter(sceneID_id__in=sceneList)
	scnOptionsList = scnOptions.values_list('soID', flat=True).distinct()


	#need sceneoption and nextscene instances
	form = NewSceneOptForm(request.POST or None)

	if form.is_valid():

		From = form.cleaned_data['From']
		Option = form.cleaned_data['Option']
		To = form.cleaned_data['To']

		# print("Index value in sceneList array")
		source = sceneCountList.index(From)
		# print(source)
		# print("Above should be three.")

		realSource = sceneList[source]
		# print("Actual Scene's Number")
		# print(realSource)
		# print("Above should be twelve.")

		sceneoption = scnopt()
		sceneoption.sceneID_id = realSource
		sceneoption.sceneText = Option
		sceneoption.save()

		soID_id = int(sceneoption.soID)

		destination = sceneCountList.index(To)
		realDestination = sceneList[destination]

		nextscene = nxtscn()
		nextscene.sceneID_id = realSource
		nextscene.sceneOptionID_id = soID_id
		nextscene.nextSceneNumber = realDestination
		nextscene.weight = 1.00 #hardcoded weight for now
		nextscene.save()

		#Check to ensure correct items are coming through
		print(From, soID_id, To)

		context = {
			"saved scene option information"
		}
		return HttpResponseRedirect("/activity/" + id + '/') #add activity url here when created.

	context = {
		'title': title,
		'activities': activities,
		'scenes': scenes,
		'scnOptions': scnOptions,
		'nxtSceneList': nxtSceneList,
		'nxtScene': nxtScene,
		'form': form,
	}
	return render(request, "activity.html", context)



#View for activity pages and creating an activity session.
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

	user = request.user
	username = user.username

	#Creates an activity session
	session = actssn()
	session.user_id = user.id
	session.startTime = datetime.now()
	session.inactive = False
	session.activityCompleted = False
	session.activityID_id = id
	session.save()


	context = {
		'title': title,
		'scene': scene,
		'activity': activity,
		'sceneList': sceneList,
		'scnType': scnType,
		'scnOptions': scnOptions,
		'nxtScene': nxtScene,
		'session': session,
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


#View to edit selected activity
def editScene(request, id):
	title = "Edit Existing Scene"
	formtitle = "Edit Existing Scene"
	instruction = "Alter the scene-related data below. Click 'Submit' to save changes."

	scene = scn.objects.get(sceneID=id) #id parameter is the scene ID passed by page
	actID = str(scene.activityID_id) #related activityID for given scene
	data = {'instructionText': scene.instructionText, 'sceneType': scene.sceneType, 'allowReplayScene': scene.allowReplayScene}

	form = NewSceneForm(request.POST or None, 
		initial=data)

	if form.is_valid():
		scene.instructionText = form.cleaned_data['instructionText']
		scene.sceneType = form.cleaned_data['sceneType']
		scene.allowReplayScene = form.cleaned_data['allowReplayScene']
		scene.save()
		context = {
			"saved Scene information after update"
		}
		return HttpResponseRedirect("/activity/" + actID + "/")

	context = {
	"title" : title,
	"formtitle": formtitle,
	"instruction": instruction,
	"form": form,
	}
	return render(request, "editScene.html", context)


#Function to delete scene - no html page
def deleteScene(request, id): #id is sceneID from event
	#Delete Function

	#delete the next scene first - those going to the deleted scene and those coming from the deleted scene
	nextscene = nxtscn.objects.all().filter(nextSceneNumber = id) # going to scene to be deleted
	nextsceneID = nxtscn.objects.all().filter(sceneID_id = id) # coming from scene to be deleted
	nextscene.delete()
	nextsceneID.delete()

	#delete the scene options second - those coming from the scene to be deleted
	sceneoptionID = scnopt.objects.all().filter(sceneID_id = id)

	# print(sceneoption.soID)
	sceneoption.delete()

	#delete the scene to be deleted
	deleteScene = scn.objects.get(sceneID=id)
	actID = str(deleteScene.activityID_id) #related activityID for given scene
	deleteScene.delete()

	return HttpResponseRedirect('/activity/' + actID + '/')



#=================================Scene Option-related Functions===================================#
#This includes scene options (NOT next scenes) for a scene.


#View to edit selected scene option (and related next scene mapping)
def editSceneOption(request, id): #importing sceneoptionID from sceneoption
	title = "Edit Existing Scene Option"
	formtitle = "Edit Existing Scene Option"
	instruction = "Alter the scene option-related data below. Click 'Submit' to save changes."

	#Used for the form and some page elements
	nextscene = nxtscn.objects.get(sceneOptionID_id = id)
	sceneoption = scnopt.objects.get(soID = id)
	scnID = str(sceneoption.sceneID_id)
	scene = scn.objects.get(sceneID=scnID)
	actID = str(scene.activityID_id)

	#Used to pull in scenes related to this activity
	scenes = scn.objects.all().filter(activityID_id = actID)
	orderedScenes = scn.objects.all().filter(activityID_id = actID).order_by('sceneID')
	sceneQS = orderedScenes.values_list('sceneID', flat=True).distinct()

	#Conversion of number of scenes to list, then array to be compared against sceneList
	sceneList = list(sceneQS)
	sceneCount = len(sceneQS)
	sceneCountList = list(range(sceneCount))
	for s in sceneCountList:
		sceneCountList[s] = sceneCountList[s] + 1

	############################## Converting the scene values ##############################
	
	#Getting the sceneID before conversion
	preConvertedSceneID = sceneoption.sceneID_id
	# print(str(preConvertedSceneID))

	#take scenevalue from database and see what index it belongs to in sceneList
	preConvertedSceneIndex = sceneList.index(preConvertedSceneID)

	#take the index of the scene's value in the sceneCount list and return
	convertedSceneID = sceneCountList[preConvertedSceneIndex]

	#Converting the next scene values
	preConvertedNextSceneNum = nextscene.nextSceneNumber

	#take scenevalue from database and see what index it belongs to in sceneList
	preConvertedNextSceneIndex = sceneList.index(preConvertedNextSceneNum)

	#take the index of the scene's value in the sceneCount list and return
	convertedNextSceneNum = sceneCountList[preConvertedNextSceneIndex]

	#Form for scene options and next scene input
	form = NewSceneOptForm(request.POST or None)

	if form.is_valid():

		From = form.cleaned_data['From']
		Option = form.cleaned_data['Option']
		To = form.cleaned_data['To']

		# source is the scene number (1, 2, etc.) the user enters as the starting scene for a scene option
		# retrieves the index position where the entered source value matches the sceneCountList
		source = sceneCountList.index(From)

		#realSource is the translated source value; retrieves the value at the index position of source
		realSource = sceneList[source]

		#saves values to the database's scene option table
		sceneoption.sceneID_id = realSource
		sceneoption.sceneText = Option
		sceneoption.save()

		soID_id = int(sceneoption.soID)

		# destination is the scene number (1, 2, etc.) the user enters as the endpoint scene for a scene option
		destination = sceneCountList.index(To)

		#realDestination is the translated destination value; retrieves the value at the index position of destination
		realDestination = sceneList[destination]

		#saves values to the database's next scene table
		nextscene.sceneID_id = realSource
		nextscene.sceneOptionID_id = soID_id
		nextscene.nextSceneNumber = realDestination
		nextscene.weight = 1.00 #hardcoded weight for now
		nextscene.save()

		#Check to ensure correct items are coming through
		print(From, soID_id, To)

		context = {
			"saved scene option information"
		}
		return HttpResponseRedirect("/activity/" + actID + '/') #add activity url here when created.

	context = {
	"title" : title,
	"formtitle": formtitle,
	"instruction": instruction,
	"form": form,
	"sceneoption": sceneoption,
	"scene": scene,
	"actID": actID,
	"scenes": scenes,
	"convertedSceneID": convertedSceneID,
	"convertedNextSceneNum": convertedNextSceneNum,
	}
	return render(request, "editSceneOption.html", context)


#Function to delete scene - no html page
def deleteSceneOption(request, id): #id is sceneOptionID passed in from activity.html
	#Delete Function

	# Used to capture the next scene related
	nextscene = nxtscn.objects.get(sceneOptionID_id = id)
	sceneoption = scnopt.objects.get(soID = id)
	scnID = str(sceneoption.sceneID_id)
	scene = scn.objects.get(sceneID=scnID)
	actID = str(scene.activityID_id)

	# Delete the nextscene record related
	nextscene.delete()

	# Delete the sceneoption record itself
	sceneoption.delete()

	return HttpResponseRedirect('/activity/' + actID + '/')






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


#This is for quickstart users
def quickStart(request):




	return render(request)