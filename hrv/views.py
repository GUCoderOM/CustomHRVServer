from django.shortcuts import render
from django.urls import reverse # ADDED
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect # ADDED
import json
from collections import deque
from django.template import loader
import pandas as pd
from .data_processing import enqueue, hrv_generator, get_ppg
from django.contrib.auth.decorators import login_required
from hrv.forms import UserForm, UserProfileForm, UserWatchForm
from hrv.models import User, UserProfile
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime, timedelta

ppg_data = deque()
ppg = []
measures = {}
num = 0

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
def index(request):
    return render(request,'hrv/index.html', context = {})

def post(request):
    global ppg_data, ppg, sampling_rate
    global measures
    global num
    userprofile = UserProfile.objects.filter(user__username__startswith = "yousuf")[0]
    stored_measures = dict(userprofile.data) #Ensure that data field is populated
    if request.method == "POST":
        num+=1
        print(num)
        data = json.loads(request.body)
        if len(data):
            time = data['time']
            ppg_data = enqueue(ppg_data, data)
            sampling_rate, ppg, ppg_data = get_ppg(ppg_data, 60)
            working_data, measures = hrv_generator(measures, ppg, sampling_rate)
            if len(ppg) and len(measures):
                print("SUCCESS!")
                try:
                    stored_measures[time] = measures
                    userprofile.data = dict(stored_measures)
                    userprofile.save()
                except Exception as e:
                    print(e)
    entries = len(list(stored_measures.keys()))
    return render(request, 'hrv/post.html', context = {'measures':measures, 'stored_measures':stored_measures,'entries':entries})
def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()

            #password hashed with set_password method
            #then user object updated
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'hrv/register.html', context = {'user_form':user_form, 'profile_form':profile_form,'registered':registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return render(request, 'hrv/index.html')
            else:
                return HttpResponse("Your account is disabled")
        else:

            print(f"Invalid login details: {username}, {password}")
            messages.info(request, 'Invalid username or password.')
    else:
        return render(request, 'hrv/login.html')
    context = {}
    return render(request, 'hrv/login.html', context)

@login_required
def user_logout(request):
    logout(request)

    return redirect(reverse('hrv:index'))

def user(request,username):
    stored_measures = {}
    shown_data = None
    today_data = ""
    userprofile = UserProfile.objects.filter(user__username__startswith = username)[0]
    watch = userprofile.watch
    if userprofile.data:

        # Get today's date
        today = timezone.now().date()
        today_str = today.strftime("%Y-%m-%d")
        data_str = json.dumps(userprofile.data)
        user_data = json.loads(data_str)
        today_data = {k: v for k, v in user_data.items() if k.startswith(today_str)}
        shown_length = 1
        if len(today_data) > shown_length:
            sorted_today_data = sorted(today_data.items(), key=lambda x: x[0], reverse=True)
            shown_data = dict(sorted_today_data[:shown_length])
        else:
            shown_data = today_data
        stored_measures = dict(userprofile.data)
    global ppg_data, ppg, sampling_rate
    global measures
    global num

    if request.method == 'POST':
        num+=1
        print(num)
        data = json.loads(request.body)
        if len(data):
            userprofile.unprocessed[data['time']] = data
            userprofile.save()
            time = data['time']
            ppg_data = enqueue(ppg_data,data)
            sampling_rate, ppg, ppg_data = get_ppg(ppg_data, 60)
            working_data, measures = hrv_generator(measures, ppg, sampling_rate)
            if len(ppg) and len(measures):
                print("SUCCESS!")
                stored_measures[time] = measures
                stored_measures = dict(stored_measures)
                stored_measures = {k: json.dumps(v) for k, v in stored_measures.items()}
                try:
                    userprofile.data = stored_measures
                    userprofile.save()

                except Exception as e:
                    print("After success",e)
    entries = len(list(stored_measures.keys()))
    # Group recordings by time
    # Get current time
    now = datetime.utcnow()

    # Calculate start time of the past week
    start_time = now - timedelta(days=7)
    start_time = start_time.replace(tzinfo=None)
    # Filter data based on time range
    filtered_data = {}
    for key, value in stored_measures.items():
        value = json.loads(value)
        timestamp = datetime.fromisoformat(key + '+00:00')
        timestamp = timestamp.replace(tzinfo=None)
        #timestamp = datetime.fromisoformat(key[:-1])
        if start_time <= timestamp <= now:
            filtered_data[key] = value

    return render(request, 'hrv/user.html', context = {"userprofile": userprofile, 'watch':watch, 'measures':measures, 'today': shown_data, 'today_len':len(today_data), 'entries':entries, 'data':filtered_data})
def register_watch(request, username):
    user = UserProfile.objects.filter(user__username__startswith = username)[0]
    registered = False
    print("Here is the username!",user.user.username)

    if request.method == 'POST':

        watch_form = UserProfileForm(request.POST)

        if watch_form.is_valid():
            user.save()
            watch = watch_form.save()
            print("THE USER:", user)
            print("THE FORM:", watch_form)
            user.watch = watch.watch
            print("The watch:", watch.watch)

            registered = True
        else:
            print(watch_form.errors)
    else:

        watch_form = UserWatchForm()
    return render(request, 'hrv/register_watch.html', context = {'watch_form': watch_form, 'registered': registered,})
