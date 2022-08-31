from django.shortcuts import render
from django.http import HttpResponse
import json
from collections import deque

from django.template import loader

from .data_processing import enqueue, hrv_generator, get_ppg


ppg_data = deque()
ppg = []
measures = {}
num = 0

# Create your views here.

def index(request):
    # global ppg, ppg_data, measures
    # sampling_rate, ppg, ppg_data = get_ppg(100, ppg_data)
    # working_data, measures = hrv_generator(measures, ppg, sampling_rate)
    return HttpResponse("hello HRV")


# 接口函数
def post(request):
    global ppg_data, ppg, sampling_rate
    global measures
    global num
    if request.method == 'POST':  # 当提交表单时
        # 判断是否传参
        num += 1
        print(num)
        data = json.loads(request.body)
        # print(data["total_event"])
        if len(data):
            ppg_data = enqueue(ppg_data, data)
            sampling_rate, ppg, ppg_data = get_ppg(ppg_data, 60)
            working_data, measures = hrv_generator(measures, ppg, sampling_rate)
    # return render(request, "measures.html", {"measures": measures})
    template = loader.get_template('measures.html')
    context = {
        "measures": measures
    }
    return HttpResponse(template.render(context, request))
