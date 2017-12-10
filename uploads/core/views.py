from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import numpy as np
import pandas as pd

import csv
import codecs
from sklearn import datasets, linear_model, metrics
from math import ceil
import datetime as dt


from uploads.core.models import Document
from uploads.core.forms import DocumentForm


def home(request):
    documents = Document.objects.all()
    return render(request, 'core/home.html', { 'documents': documents })

def simple_upload(request):
    print (request.FILES.keys())
    if request.method == 'POST' and request.FILES:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        myfile.open()
        reader = csv.reader(codecs.EncodedFile(myfile, "utf-8"), delimiter=',')
        #reader = pd.read_csv('bill.csv')
        print (reader)
        count = 0
        DAY = []
        DATE = []
        ITEM_ID = []
        QUANTITY = []
        for row in reader:
            count = count + 1
            if(count>1) :
                DATE.append(row[0])
                DAY.append(row[1])
                ITEM_ID.append(int(row[2]))
                QUANTITY.append(int(row[3]))
            
        x_weekend = []
        x_time = []
        x =0
        print(DAY) 
    #print(dt.datetime.strptime(DAY[0], "%d/%m/%Y").date().weekday())
        for i in DAY:
        #print(i,"  ",dt.datetime.strptime(DAY[0], "%d/%m/%Y").date())
            if dt.datetime.strptime(i, "%d/%m/%Y").date().weekday() < 5:
                x_weekend.append(0);
            else:
                x_weekend.append(1);
        print(x_weekend)

    #print(dt.datetime.strptime('14/05/2017', "%d/%m/%Y").date().weekday())
        for i in DATE:
            x_time.append(time_check(dt.datetime.strptime(i, '%H:%M:%S').time()))

        num_items = len(np.unique(ITEM_ID))
        coefficients = []
        intercepts = []
        X = np.array([x_weekend,x_time]).T


        for i in range(1,num_items+1):
            train_set_size = len(ITEM_ID)
            y = []
            for j in range(0,train_set_size):
                if ITEM_ID[j] == i:
                    y.append(QUANTITY[j])
                else:
                    y.append(0)
            #print(i)
            #print(X,y)
            A,B = lin_reg(X,y)
            print(A)
            coefficients.append(A)
            intercepts.append(B)
            #print(coefficients[i-1],"--",intercepts[i-1])

        test_date = request.POST['Order date']
        uploaded_file_url = fs.url(filename)
        if dt.datetime.strptime(test_date, "%Y-%m-%d").date().weekday() <5 :
            day = 0
        else :
            day = 1

         
        model_y = np.ndarray((4, num_items))
        for daytime in range(1,5):
            test_x = np.array([day,daytime])
            print(daytime)
            for food_type in range(0,num_items):
                model_y[daytime-1][food_type] = ceil(np.dot(coefficients[food_type], test_x.T)+intercepts[food_type])
                print (round(model_y[daytime-1][food_type])),
                #print(daytime , food_type ,"==" ,np.dot(coefficients[food_type], test_x.T)+intercepts[food_type]),
            
        print(model_y.astype(int))
        Expected_order = model_y.astype(int)
        Daytime = ['BREAKFAST','LUNCH','EVENING SANCKS','DINNER']
        test_date = dt.datetime.strptime(test_date, "%Y-%m-%d").date()

        Expected_order_day = zip(Expected_order,Daytime)
	'''data = pd.read_csv("media/"+filename)
	data.columns = ['item_id','wasted','day' , 'time']
        a1 = list(data.day)
        a2 = list(data.time)
        a3 =list(data.wasted)
        a4=list(data.item_id) 
        uploaded_file_url = fs.url(filename)
	print (a1,a2,a3,a4)'''
        return render(request, 'core/simple_upload.html', {
                'uploaded_file_url': uploaded_file_url , 'Expected_order_day':Expected_order_day,
                'test_date' :test_date 
            })
    return render(request, 'core/simple_upload.html')

def time_check(now):
    x = 0
    time_now = dt.datetime.now().time()
    today8am = time_now.replace(hour=8, minute=0, second=0, microsecond=0)
    today12pm = time_now.replace(hour=12, minute=0, second=0, microsecond=0)
    today16pm = time_now.replace(hour=16, minute=0, second=0, microsecond=0)
    today19pm = time_now.replace(hour=19, minute=0, second=0, microsecond=0)
    today24pm = time_now.replace(hour=23, minute=59, second=59, microsecond=59)

    if today8am <= now and now <= today12pm: 
        x=1
    elif today12pm <= now and now <= today16pm :
        x=2
    elif today16pm <= now and now <= today19pm :
        x=3
    elif today19pm <= now and now <= today24pm :
        x=4
    return x

def lin_reg(X,y):
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4,
    #                                               random_state=1)
    reg = linear_model.LinearRegression(fit_intercept=True, normalize = True)
    print("in lin_reg")
 
    # train the model using the training sets
    reg.fit(X, y)
 
    # regression coefficients
    #print('Coefficients: \n', reg.coef_)
    #print('intercept',reg.intercept_)

    return (reg.coef_,reg.intercept_)
    
