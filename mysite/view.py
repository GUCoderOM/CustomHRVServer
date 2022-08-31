from django.http import HttpResponse
import json


# 定义功能
def add_args(a, b):
    return a + b


# 接口函数
def post(request):
    if request.method == 'POST':  # 当提交表单时
        dic = {}
        # 判断是否传参
        print(request.body)
        data = json.loads(request.body)
            # 判断参数中是否含有a和b
        if len(data):
            return HttpResponse(data)
        else:
            return HttpResponse('输入错误')


    else:
        return HttpResponse('方法错误')

