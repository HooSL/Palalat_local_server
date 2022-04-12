import pandas as pd
import numpy as np
from seaborn.axisgrid import pairplot
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import joblib
from flask_restful import Resource
from flask import request
from flask.json import jsonify
from flask_restful import Resource
from http import HTTPStatus
import math

class ml_rf(Resource):
    def post(self):

        brand = request.form.get('brand')
        year = request.form.get('year')
        milege = request.form.get('milege')
        enginsize = request.form.get('enginsize')
        trans = request.form.get('trans')
        fuel = request.form.get('fuel')
        mpg = request.form.get('mpg')


        #변속기
        if trans =='Automatic':
            trans = [0,0]
        elif trans =='Manual':
            trans = [1,0]
        elif trans =='Semi-Auto':
            trans = [0,1]

        #연료
        if fuel =='Diesel':
            fuel = [0,0]
            print(fuel)
        elif fuel =='Hybrid':
            fuel = [1,0]
        elif fuel =='Petrol':
            fuel = [0,1]

        #제조사
        if brand =='Audi':
            brand = [0,0,0,0,0]
        elif brand =='BMW':
            brand = [1,0,0,0,0]
        elif brand =='Ford':
            brand = [0,1,0,0,0]
        elif brand =='Hyundai':
            brand = [0,0,1,0,0]
        elif brand =='Mercedes Benz':
            brand = [0,0,0,1,0]
        elif brand =='Toyota':
            brand = [0,0,0,0,1]


        first_list = [year,milege,enginsize,mpg]

        new_data = first_list + brand + trans + fuel
        print("짜잔1")

        #new_data=np.array([year,milege,enginsize,mpg,trans,fuel,brand])
        new_data = np.array([new_data])
    
        new_data = new_data.reshape(1,13)
        
        print("짜잔2")
        #인공지능 불러오기
        scaler_X = joblib.load('data/scaler_X.pkl')
        scaler_y = joblib.load('data/scaler_y.pkl')
        regressor = joblib.load('data/regressor.pkl')
        print("짜잔3")
        #유저 데이터 피쳐스케일링
        new_data = scaler_X.transform(new_data)

        #예측
        y_pred = regressor.predict(new_data)

        #피쳐스케일링 한거 원래대로 복구
        #터미널로 확인
        print(y_pred)
        y_pred = scaler_y.inverse_transform(y_pred.reshape(1,1))

        y_pred = y_pred[0][0]

        y_pred = math.floor(y_pred)

        print(y_pred)

        return {"예측 값" : y_pred}