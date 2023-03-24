import heartpy as hp
import neurokit2 as nk
import numpy as np
import pandas as pd
import json
from collections import deque
from django.utils import timezone
import sqlite3
from .models import PPG

con = sqlite3.connect("db.sqlite3")
cur = con.cursor()


# SAMPLING_RATE = 1e9
# INTERVAL = 1 / SAMPLING_RATE * 1e9


def csv_data_loader(file, data_queue):
    data = pd.read_csv(file)


def enqueue(data_queue, data):
    if not isinstance(data, dict):
        data = json.loads(data)
    data_dict = {"time": data["time"], "event": data["total_event"], "ts": data["time_stamp"],
            "ppg": data["data1"]}
    # print(data['data1'])
    queue = data_queue
    # if len(queue):
    #     queue.popleft()
    queue.append(data_dict)
    return queue


def get_ppg(data_queue, window_size, data_freq=100):
    sampling_rate = 100
    signal = []
    length = len(data_queue)
    # data_queue.popleft()
    window_size = window_size
    if length > window_size:
        timer = []
        for i in range(length - window_size):
            data_queue.popleft()  # should save
        for i in range(len(data_queue)):
            timer += data_queue[i]["ts"]
            signal += data_queue[i]["ppg"]
        sampling_rate = int(len(signal) / (timer[-1] - timer[0]) * 1e9)
    return sampling_rate, signal, data_queue


def insert(data):
    if not isinstance(data, dict):
        data = json.loads(data)
    ppg = PPG(date=timezone.now(), time_stamp=data['time_stamp'], ppg_signal=data['data1'])
    ppg.save()


def hrv_generator(measures, signal, sampling_rate=100):
    working_data = -1
    measures = measures
    if len(signal):
        ppg_clean = nk.ppg_clean(signal, sampling_rate=sampling_rate)
        ppg_scaled = hp.scale_data(signal)
        #bpmmin = 10, bpmmax = 200
        working_data, measures = hp.process(ppg_clean, sampling_rate,calc_freq=True)
    return working_data, measures
def group_data(data_list):
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
        data_field_dict = {}
    return data_dict
def save_data(time,measures,slug):
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
    data.save()

    print("Successfully saved Data object with time:",time)
if __name__ == "__main__":
    test_data = {"total_event": 36, "sensor_type": "com.google.wear.sensor.ppg", "time": "2022-07-24T21:40:04.253",
                 "time_stamp": 81376855103961, "data0": 24729472, "data1": 3723379, "data2": 0}
    json_data = json.dumps(test_data)
    # json_data = json.loads(json_data)
    data_queue = deque()
    data_queue = enqueue(test_data, data_queue)
    print(data_queue)
    #ppg_filtered = nk.signal_filter(signal, lowcut=1, highcut=10, method='butterworth', order=4)     # print(ppg_clean)

# not functional when called on command line
