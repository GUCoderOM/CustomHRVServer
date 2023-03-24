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
import time
testing = False
def populate():
    f = open('data.json')
    data_file = json.load(f)
    n = int(len(data_file.keys())/10)
    items = list(data_file.items())
    item_dict = listTupletoDict(items)
    m = dict_slice(item_dict, n,- 1)
    l = m['2022-11-26T18:45:26.471']
    #print(list(l.keys()))
    dict_slice(item_dict, n*2,n - 1)
    users = [{'username': 'Yousuf','age':21,'email': 'Yousuf@gmail.com',
                'data':dict_slice(item_dict, n,- 1)},
            {'username': 'EmmaM','age':25,'email': 'Emma@gmail.com',
                        'data':dict_slice(item_dict, n*2,n - 1)},
            {'username': 'Joseph','age':19,'email': 'Joseph@gmail.com',
                        'data':dict_slice(item_dict, n*3,n*2 - 1)},
            {'username': 'Adam','age':55,'email': 'Adam@gmail.com',
                        'data':dict_slice(item_dict, n*4,n*3 - 1)},
            {'username': 'Rebecca','age':18,'email': 'Rebecca@gmail.com',
                        'data':dict_slice(item_dict, n*5,n*4 - 1)},
            {'username': 'Roberta','age':19,'email': 'Roberta@gmail.com',
                        'data':dict_slice(item_dict, n*6,n*5 - 1)},
            {'username': 'Isabella','age':34,'email': 'Isabella@gmail.com',
                        'data':dict_slice(item_dict, n*7,n*6 - 1)},
            {'username': 'Smith','age':40,'email': 'Smith@gmail.com',
                        'data':dict_slice(item_dict, n*8,n*7 - 1)},
            {'username': 'Lars','age':64,'email': 'Lars@gmail.com',
                        'data':dict_slice(item_dict, n*9,n*8 - 1)},
            {'username': 'Leopold','age':20,'email': 'Leopold@gmail.com',
                        'data':dict_slice(item_dict, n*10,n*9 - 1)},]
    for user in users:
        try:
            if not testing:
                u,mypass = add_UserProfile(user['username'],user['age'],user['email'])
                print("Successfully created user",u.user,'with password:',mypass)
            else:
                print("Test passed")
        except Exception as e:
            print('Failed to add UserProfile',e)
    if not testing:
        superuser=User.objects.create_user('y', password = 'y')
        superuser.is_superuser=True
        superuser.is_staff=True
        superuser.save()
def create_user(username):
    try:
        #mypass = get_random_string(8)
        mypass = 'y'
        user=User.objects.create_user(username, password=mypass)
        user.is_superuser=True
        user.is_staff=True
        user.save()
        return [user,mypass]
    except Exception as e:
        print(e)
def add_UserProfile(username,age,email):
    arr = create_user(username)
    user = arr[0]
    mypass = arr[1]
    u = UserProfile.objects.get_or_create(user= user)[0]
    u.user = user
    u.age = age
    u.email=email
    u.save()
    return u,mypass
def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def listTupletoDict(myList):
    result_dict = {}
    for date, dict_val in myList:
        result_dict[date] = dict_val
    return result_dict
def dict_slice(myDict,high, low):
    sliced_dict = {}
    keys = list(myDict.keys())
    i = low +1
    while i < high and i > low:
        sliced_dict[keys[i]] = myDict[keys[i]]
        i+=1
    return sliced_dict
def unprocessed_count():
    userprofile = UserProfile.objects.filter(user__username__startswith = "Yous")[0]
    unprocessed = userprofile.unprocessed
    print("Here is the count of unprocessed data:",len(unprocessed))
def unprocessed_count_live(delay):
    print("Here is the live count of unprocessed data, updated every",delay,'seconds.')


    while True:
        userprofile = UserProfile.objects.filter(user__username__startswith = "Yous")[0]
        print("unprocessed data count:",len(userprofile.unprocessed))
        time.sleep(delay)
# Start execution here!
if __name__ == '__main__':
    print("Populating HRVServer")
    populate()
    #unprocessed_count()
    #unprocessed_count_live(2)
