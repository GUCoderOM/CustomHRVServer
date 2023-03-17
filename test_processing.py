import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'mysite.settings')

import django
django.setup()

from hrv.models import UserProfile
from hrv.data_processing import enqueue, hrv_generator, get_ppg
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from collections import deque
import random
import json
import string
import time
from datetime import datetime, timedelta

testing = True

ppg_data = deque()
ppg = []
measures = {}
num = 0
def test_data_processing(username):
    userprofile = UserProfile.objects.filter(user__username__startswith = username)[0]
    unprocessed_data = userprofile.unprocessed
    print(type(unprocessed_data))
    global ppg_data, ppg, sampling_rate
    global measures
    global num
    successful_attempts = 0
    failed = 0
    measures_dict = {}
    error_types = []
    errors = {}
    error_type_count = {}
    for data in unprocessed_data.values():
        try:
            time = data['time']
            ppg_data = enqueue(ppg_data,data)
            sampling_rate, ppg, ppg_data = get_ppg(ppg_data, 60)
            working_data, measures = hrv_generator(measures, ppg, sampling_rate)
            if measures != {}:
                measures_dict[time] = json.dumps(measures)
                successful_attempts+=1
        except Exception as e:
            if type(e) not in error_types:
                error_types.append(type(e))
                errors[type(e)] = e
                error_type_count[type(e)] = 1
                #print(e)
            else:
                error_type_count[type(e)] = error_type_count[type(e)]+1
            failed+=1

    #print("Failed",failed, "times")
    #print(measures)
    print(successful_attempts,'successful_attempts.')
    print(failed,'failed')
    print((successful_attempts/ len(unprocessed_data.values()))*100)

    print(error_type_count)

    #print(type(json.loads(measures_dict['2023-03-02T16:44:38.048'])))
    #print(type(measures_dict['2023-03-02T16:44:38.048']))
    return measures_dict
def save_user_data(username):
    userprofile = UserProfile.objects.filter(user__username__startswith = username)[0]
    measures = test_data_processing()
    userprofile.data = measures
    userprofile.save()
    print("Saved data onto Yara's userprofile.")
def test_data_filtration():
    userprofile = UserProfile.objects.filter(user__username__startswith = "bookar")[0]
    stored_measures = userprofile.data
    now = datetime.utcnow()

    # Calculate start time of the past week
    start_time = now - timedelta(days=7)
    start_time = start_time.replace(tzinfo=None)
    # Filter data based on time range
    filtered_data = {}
    #print(type(stored_measures['2023-03-02T16:44:38.048']))
    for key, value in stored_measures.items():
        timestamp = datetime.fromisoformat(key + '+00:00')
        timestamp = timestamp.replace(tzinfo=None)
        #timestamp = datetime.fromisoformat(key[:-1])
        if start_time <= timestamp <= now:
            filtered_data[key] = value
    data = filtered_data
    print(type(json.loads(data['2023-03-02T16:44:38.048'])))

    for date, value in data.items():
        value = json.loads(value)
        print(date,value['bpm'])
def testing():
    userprofile = UserProfile.objects.filter(user__username__startswith = "bookar")[0]
    print(type(userprofile.unprocessed))
# Start execution here!
if __name__ == '__main__':
    print("Testing data_processing")
    test_data_processing("bookar")
    #save_user_data('bookar')
    #test_data_filtration()
    #testing()
