
    # Created by: CJ
    # Date: 2/9/2016
    # Purpose: All views for the project are created in this page

from django.shortcuts import render, get_object_or_404
from .forms import UserLoginForm, NewUserAccountForm, NewAdminForm
from .forms import NewEventForm, NewActivityForm, NewSceneForm, NewSceneOptionForm
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
from array import array



# Create your views here.
def home(request):
	# title = "Welcome"
	# if request.user.is_authenticated():
	title = "Welcome, %s" % (request.user)
	form = UserLoginForm(request.POST)
	#video 14/42 has alternate validation methods

	if form.is_valid():
		# print (request.POST['username'])
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect("/activityDashboard/")
	else:
		form = UserLoginForm()
	print("HELOOOOOOOOOOOOOO")
	print(form)

	context = {
		"title": title,
		"form": form,
	}

	return render(request,"home.html", context)

def userLogin(request):
	form = UserLoginForm(request.POST)
	#video 14/42 has alternate validation methods

	if form.is_valid():
		# print (request.POST['username'])
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect("/activityDashboard/")
	else:
		form = UserLoginForm()
	print("HELOOOOOOOOOOOOOO")
	print(form)
	#parens create instance
	context = {
		"form": form,
	}

	return render(request,"userLogin.html", context) #redirecting to actDash for now


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
		event = emod()
		event.userID_id = user.userID
		event.adminID_id = admin.adminID
		event.eventName = form.cleaned_data['eventName']
		event.joincode = form.cleaned_data['joincode']
		event.enforceUser = form.cleaned_data['enforceUser']
		event.save()
		context = {
			"saved Event information"
		}
		return HttpResponseRedirect("/activityDashboard/") #add event url here when created. home for now

	context = {
		"title" : title,
		"formtitle": formtitle,
		"instruction": instruction,
		"form": form,
	}
	return render(request, "createEvent.html", context)


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

