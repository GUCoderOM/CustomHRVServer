import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'mysite.settings')

import django
django.setup()

from hrv.models import UserProfile
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import random
import json
import string

from django.utils import timezone
from datetime import datetime, timedelta
def test():
    userprofile = UserProfile.objects.filter(user__username__startswith = 'Adam')[0]
    watch = userprofile.watch
    # Get today's date
    today = timezone.now().date()
    today_str = today.strftime("%Y-%m-%d")
    #print(userprofile.data[list(userprofile.data.keys())[0]])
    data_str = json.dumps(userprofile.data)
    user_data = json.loads(data_str)
    print(user_data[list(userprofile.data.keys())[0]])
    today_data = {k: v for k, v in user_data.items() if k.startswith(today_str)}
    shown_length = 1
    if len(today_data) > shown_length:
        sorted_today_data = sorted(today_data.items(), key=lambda x: x[0], reverse=True)
        shown_data = dict(sorted_today_data[:shown_length])
    else:
        shown_data = today_data
    grouped_data = {}
    for time_str, recordings in userprofile.data.items():
        time = iso_to_datetime(time_str)
        if time not in grouped_data:
            grouped_data[time] = []
        grouped_data[time].append(recordings)

    # Sort the grouped data by time
    sorted_grouped_data = dict(sorted(grouped_data.items()))
    print("We have",len(sorted_grouped_data),"minute intervals")
    sorted_grouped_data = list(sorted_grouped_data.values())
    print(type(sorted_grouped_data[0][0]))
def iso_to_datetime(iso_datetime):
    return datetime.fromisoformat(iso_datetime.replace('Z', '+00:00'))
def test_user_data(username):
    userprofile = UserProfile.objects.filter(user__username__startswith = username)[0]
    print(userprofile.data)

if __name__ == '__main__':
    print("Running tests...")
    #test()
    test_user_data('r')
