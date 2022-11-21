from django.shortcuts import render
from django.urls import reverse # ADDED
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render,redirect # ADDED
import json
from collections import deque

from django.template import loader
import pandas as pd
from .data_processing import enqueue, hrv_generator, get_ppg
from django.contrib.auth.decorators import login_required
from hrv.forms import UserForm, UserProfileForm,UserWatchForm
from hrv.models import User, UserProfile
from django.contrib.auth import authenticate, login,logout
import csv

ppg_data = deque()
ppg = []
measures = {}
num = 0
# Create your views here.

def index(request):
    return render(request, 'hrv/index.html',context = {})


def post(request):
    global ppg_data, ppg, sampling_rate
    global measures
    global num
    with open('test.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        if request.method == 'POST':
            num += 1
            print(num)
            data = json.loads(request.body)
            if len(data):
                ppg_data = enqueue(ppg_data, data)
                sampling_rate, ppg, ppg_data = get_ppg(ppg_data, 60)
                working_data, measures = hrv_generator(measures, ppg, sampling_rate)
                if len(ppg):
                    print("SUCCESS!")
                    print(measures['bpm'])
                    writer.writerow([measures['bpm']])
                else:
                    print('FAILURE!')

    return render(request, 'hrv/post.html',context = {'measures':measures,})


def register(request):
    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
         # Attempt to grab information from the raw form information.
         # Note that we make use of both UserForm and UserProfileForm.
         user_form = UserForm(request.POST)
         profile_form = UserProfileForm(request.POST)

         # If the two forms are valid...
         if user_form.is_valid() and profile_form.is_valid():
         # Save the user's form data to the database.
             user = user_form.save()

             # Now we hash the password with the set_password method.
             # Once hashed, we can update the user object.
             user.set_password(user.password)
             user.save()
             # until we're ready to avoid integrity problems.
             profile = profile_form.save(commit=False)
             profile.user = user

         # Did the user provide a profile picture?
         # If so, we need to get it from the input form and
         #put it in the UserProfile model.
             if 'picture' in request.FILES:
                 profile.picture = request.FILES['picture']

             # Now we save the UserProfile model instance.
             profile.save()

             # Update our variable to indicate that the template
             # registration was successful.
             registered = True
         else:
             # Invalid form or forms - mistakes or something else?
             # Print problems to the terminal.
             print(user_form.errors, profile_form.errors)
    else:
         # Not a HTTP POST, so we render our form using two ModelForm instances.
         # These forms will be blank, ready for user input.
         user_form = UserForm()


         profile_form = UserProfileForm()

     # Render the template depending on the context.
    return render(request,
                         'hrv/register.html',
                                            context = {'user_form': user_form,
                                                                        'profile_form': profile_form,
                                                                                                'registered': registered})

def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
        # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return render(request, 'hrv/index.html')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your hrv account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            messages.info(request, 'Invalid username or password.')
            #return redirect(reverse('just_for_fun:login'))
            #return HttpResponse("Invalid login details supplied. Return to previous page to retry")
        # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'hrv/login.html')
    context = {}
    return render(request, 'hrv/login.html',context)

@login_required
def user_logout(request):
# Since we know the user is logged in, we can now just log them out.
    logout(request)
# Take the user back to the homepage.
    return redirect(reverse('hrv:index'))

def user(request,username):
    userprofile = UserProfile.objects.filter(user__username__startswith = username)[0]
    watch = userprofile.watch
    print(userprofile.picture)
    return render(request, 'hrv/user.html', context = {"userprofile":userprofile, 'watch':watch,'top':top,})



def register_watch(request, username):
    user = UserProfile.objects.filter(user__username__startswith = username)[0]
    registered = False

    if request.method == 'POST':

         watch_form = UserWatchForm(request.POST)

         if watch_form.is_valid():
             watch = watch_form.save()
             print("THE USER:",user)
             print("THE FORM:",watch_form)
             user.watch = watch.watch
             print("The watch:",watch.watch)
             user.save()
             registered = True
         else:

             print(watch_form.errors)
    else:

         watch_form = UserWatchForm()

    return render(request,
                         'hrv/register_watch.html',context ={'watch_form': watch_form, 'registered':registered,})
