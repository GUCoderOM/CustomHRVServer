import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'mysite.settings')

import django
django.setup()

from hrv.models import UserProfile,Data
from hrv.data_processing import enqueue, hrv_generator, get_ppg
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from decimal import Decimal
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
def test_data_processing(username,save):
    userprofile = UserProfile.objects.filter(user__username__startswith = username)[0]
    with open('unprocessed_data.json', 'r') as f:
        # Load the JSON data from the file into a Python variable
        unprocessed_data = json.load(f)
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
                if save:
                    save_data(time,measures,userprofile.slug,save)
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
    print("Success rate:",(successful_attempts/ len(unprocessed_data.values()))*100)

    print(error_type_count)

    #print(type(json.loads(measures_dict['2023-03-02T16:44:38.048'])))
    #print(type(measures_dict['2023-03-02T16:44:38.048']))

    return measures_dict
def save_user_data(username):
    userprofile = UserProfile.objects.filter(user__username__startswith = username)[0]
    measures = test_data_processing()
    userprofile.data = measures
    userprofile.save()
    print("Saved data onto",username,"userprofile.")
def test_data_filtration(username):
    userprofile = UserProfile.objects.filter(user__username__startswith = "username")[0]
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


def test_group_data(data_list):
    # Takes list of Data objects and combines them all in one dictionary
    # in following format: {timestamp: {datappoint1: x, datapoint2:y...},timestamp:...}
    data_dict = {}
    data_field_dict = {}
    ignore = ['id','user_id','time']
    for data in data_list:
        for field in vars(data):
            # Filter out any unwanted attributes
            if not field.startswith('_') and not callable(getattr(data, field)) and field not in ignore:
                data_field_dict[field] = getattr(data, field)
        data_dict[data.time] = data_field_dict
    return data_dict

def save_data(time,measures,slug,save):
    decimals = '.0001'
    data = Data(time=time)
    data.bpm =Decimal(measures["bpm"]).quantize(Decimal(decimals))

    data.ibi =Decimal(measures["ibi"]).quantize(Decimal(decimals))

    data.sdnn =Decimal(measures["sdnn"]).quantize(Decimal(decimals))
    data.sdsd =Decimal(measures["sdsd"]).quantize(Decimal(decimals))
    data.rmssd =Decimal(measures["rmssd"]).quantize(Decimal(decimals))
    data.pnn20 =Decimal(measures["pnn20"]).quantize(Decimal(decimals))
    data.pnn50 =Decimal(measures["pnn50"]).quantize(Decimal(decimals))
    data.hr_mad =Decimal(measures["hr_mad"]).quantize(Decimal(decimals))
    data.sd1 =Decimal(measures["sd1"]).quantize(Decimal(decimals))
    data.sd2= Decimal(measures["sd2"]).quantize(Decimal(decimals))
    data.s =Decimal(measures["s"]).quantize(Decimal(decimals))
    #data.sd1_sd2 =Decimal(measures["sd1/sd2"])
    data.breathingrate =Decimal(measures["breathingrate"]).quantize(Decimal(decimals))
    data.vlf =Decimal(measures["vlf"]).quantize(Decimal(decimals))
    data.lf =Decimal(measures["lf"]).quantize(Decimal(decimals))
    data.hf =Decimal(measures["hf"]).quantize(Decimal(decimals))
    data.lf_hf =Decimal(measures["lf/hf"]).quantize(Decimal(decimals))
    data.p_total =Decimal(measures["p_total"]).quantize(Decimal(decimals))
    data.vlf_perc =Decimal(measures["vlf_perc"]).quantize(Decimal(decimals))
    data.lf_perc =Decimal(measures["lf_perc"]).quantize(Decimal(decimals))
    data.hf_perc =Decimal(measures["hf_perc"]).quantize(Decimal(decimals))
    data.lf_nu =Decimal(measures["lf_nu"]).quantize(Decimal(decimals))
    data.hf_nu =Decimal(measures["hf_nu"]).quantize(Decimal(decimals))

    data.user_id =slug
    if save:
        data.save()

    print("Successfully saved Data object with time:",time)
# Start execution here!
if __name__ == '__main__':
    print("Testing data_processing")
    test_data_processing("y", False)
    #save_user_data('y')
    #test_data_filtration(username)
    #testing()
    #userprofile = UserProfile.objects.filter(user__username__startswith = 'y')[0]
    #data = Data.objects.filter(user_id__startswith = userprofile.slug)
    #test_group_data(data)
