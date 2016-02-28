
    # Created by: CJ
    # Date: 2/9/2016
    # Purpose: All views for the project are created in this page

from django.shortcuts import render, get_object_or_404
from .forms import UserLoginForm, ContactForm, NewUserAccountForm, NewAdminForm
from .forms import NewEventForm, NewActivityForm, NewSceneForm, NewSceneOptionForm
from .models import Activity as act
from .models import Scene as scn
from .models import SceneOptions as scnopt
from .models import NextScene as nxtscn
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count



# Create your views here.
def home(request):
	# title = "Welcome"
	# if request.user.is_authenticated():
	title = "Welcome, %s" % (request.user)

	context = {
		"title": title,
	}

	return render(request,"home.html", context)

def userLogin(request):
	form = UserLoginForm(request.POST or None)

	#video 14/42 has alternate validation methods
	if form.is_valid():
		# print (request.POST['username'])
		instance = form.save(commit=False)
		instance.save()
		context = {
			"title":"Thank you." #does not yet take you to the user's dashboard
		}
		return HttpResponseRedirect("/activityDashboard/")

	#parens create instance
	context = {
		"form": form,
	}

	return render(request,"userLogin.html", context)

def newUserLogin(request):
	form = NewUserAccountForm(request.POST or None)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		context = {
			"Hello."
		}
		return HttpResponseRedirect("/activityDashboard/")

	context = {
		"form": form,
	}
	return render(request,"newUserLogin.html", context)

#View for activity splash page
def activityDashboard(request):
	title = "Dashboard"

	activities = act.objects.all()
	# activityID = act.objects.get(filter)

	context = {
		'title': title,
		'activities': activities,
	}
	return render(request,"activityDashboard.html", context)

#View for activity start page
def activityStart(request, id):
	title = "Start Activity"

	# activity = act.objects.get(activityID=request.urlparams[0])
	activity = get_object_or_404(act, activityID=id) #id here is the activityID
	scenes = scn.objects.all().filter(activityID_id=id)
	intro = scn.objects.get(activityID_id=id, sceneType=None)
	sceneOpt = scnopt.objects.get(sceneID_id = intro.sceneID)
	nextScene = nxtscn.objects.get(sceneID_id = intro.sceneID)
	activitySceneCount = scenes.count() #returns 7 items, which it should

	#New problem, how to get page to reload with new information each time?
	#New problem, how to get page to go back to mission screen afterwards?

	print("LOOK HERE!***********************************")
	print(intro.sceneID)
	print(sceneOpt.sceneText)
	print(nextScene.nextSceneNumber)
	print(activitySceneCount)

	context = {
		'title': title,
		'activity': activity,
		'scenes': scenes,
		'intro': intro,
		'sceneOpt': sceneOpt,
		'nextScene': nextScene,
		'activitySceneCount': activitySceneCount,
	}
	return render(request,"activityStart.html", context)

#View for activity start page
def activityPage(request, id):
	title = "Activity"

	activity = get_object_or_404(act, activityID=id) #id here is the activityID
	scene = scn.objects.all().filter(activityID_id=id)
	activitySceneCount = scene.count()
	print(activitySceneCount)

	#Add for loop to go through rows in Scene where ActivityID = id
	for a in activitySceneCount:
	#add nested if statement to figure out if the scenetype is 0 or 1
		if scene.sceneType == None:
			sceneInfo = scn.objects.get(activityID_id=id, sceneType=None)
			sceneOpt = scnopt.objects.get(sceneID_id = sceneInfo.sceneID)
			nextScene = nxtscn.objects.get(sceneID_id = sceneInfo.sceneID)
		elif scene.sceneType == 0:
			#-load in sceneinformation 
			sceneInfo = scn.objects.get(activityID_id=id, sceneType=0)
			sceneOpt = scnopt.objects.get(sceneID_id = sceneInfo.sceneID)
			nextScene = nxtscn.objects.get(sceneID_id = sceneInfo.sceneID)
		elif scene.sceneType == 1:
			sceneInfo = scn.objects.get(activityID_id=id, sceneType=1)
			sceneOpt = scnopt.objects.get(sceneID_id = sceneInfo.sceneID)
			#won't need nextscene here because the link will send them to the mission page.
		else:
			print("There should be no other option in this if statement")
	else: 
		print("There should be no other option for this for loop")


	context = {
		'title': title,
		'scene': scene,
		'activitySceneCount': activitySceneCount,
		'sceneInfo': sceneInfo,
		'sceneOpt': sceneOpt,
		'nextScene': nextScene,
	}
	return render(request,"activityPage.html", context)








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

#Adding new events -- Will be used by admin; right now just need to create for table.
#*******************Haven't tested this as of (2/13/16)********************
def newEventForm(request):
	form = NewEventForm(request.POST or None)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		context = {
			"saved Event information"
		}
		return HttpResponseRedirect("") #add event url here when created.

	context = {
		"form": form,
	}
	return render(request,"",context)

#Adding new activity -- Will be used by admin; right now just need to create for table.
#*******************Haven't tested this as of (2/13/16)********************
def newActivityForm(request):
	form = NewActivityForm(request.POST or None)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		context = {
			"saved Activity information"
		}
		return HttpResponseRedirect("") #add activity url here when created.

	context = {
		"form": form,
	}
	return render(request,"",context)

#Adding new scene -- Will be used by admin; right now just need to create for table.
#*******************Haven't tested this as of (2/13/16)********************
def newSceneForm(request):
	form = NewSceneForm(request.POST or None)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		context = {
			"saved Scene information"
		}
		return HttpResponseRedirect("") #add scene url here when created

	context = {
		"form": form,
	}
	return render(request,"",context)

#Adding new sceneoption -- Will be used by admin; right now just need to create for table.
#*******************Haven't tested this as of (2/13/16)********************
def newSceneOptionForm(request):
	form = NewSceneOptionForm(request.POST or None)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		context = {
			"saved Scene Option information"
		}
		return HttpResponseRedirect("") #add scene option url when created

	context = {
		"form": form,
	}
	return render(request,"",context)


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

