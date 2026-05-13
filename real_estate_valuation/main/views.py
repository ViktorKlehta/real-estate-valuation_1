from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import UpdateView
from django.conf import settings
from .forms import RealEstateForm
from geopy.distance import geodesic
import os
import pickle
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, StackingRegressor
from lightgbm import LGBMRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.utils import resample
from category_encoders import TargetEncoder
import warnings
# from tqdm import tqdm


def index(request):
    return render(request, 'main/index.html')


def input(request):
    error = ''
    predicted_price = None
    price_range = None
    # center_coords = (45.0453067, 38.97993490465748)
    center_coords = (45.045868, 38.978081)

    if request.method == 'POST':
        form = RealEstateForm(request.POST)
        if form.is_valid():
            estate = form.save(commit=False)
            with open('main/models/model_3.pkl', 'rb') as f:
                model = pickle.load(f)

            if estate.latitude and estate.longitude:
                estate_coords = (estate.latitude, estate.longitude)
                distance = geodesic(center_coords, estate_coords).kilometers
                estate.distance_to_center = round(distance, 2)
                estate.save()

                new_data = {
                    'Тип': [float(form.cleaned_data['type'])],
                    'Количество комнат': [float(form.cleaned_data['room_count'])],
                    'Тип дома': [form.cleaned_data['house_type']],
                    'Тип продажи': [form.cleaned_data['sale_type']],
                    'Улица': [form.cleaned_data['street']],
                    'Район': [form.cleaned_data['district']],
                    'Общая площадь': [float(form.cleaned_data['total_area'])],
                    'Этаж': [float(form.cleaned_data['floor'])],
                    'Этажность': [float(form.cleaned_data['total_floors'])],
                    'Широта': [float(form.cleaned_data['latitude'])],
                    'Долгота': [float(form.cleaned_data['longitude'])],
                    'Расстояние до центра': [float(distance)]
                }

                new_df = pd.DataFrame(new_data)


                log_pred = model.predict(new_df)
                predicted_price = np.expm1(log_pred)[0]

                print(float(form.cleaned_data['type']))
                print(form.cleaned_data['district'])

                # if predicted_price <= 7222500.0:
                #     dip = 8.900553 / 100
                # elif predicted_price <= 11076000.0:
                #     dip = 6.087530 / 100
                # elif predicted_price <= 14495000.0:
                #     dip = 4.217036 / 100
                # else:
                #     dip = 7.914894 / 100

                if float(form.cleaned_data['type']) == 0 :
                    dip = 14.7515 / 100
                else :
                    dip = 2.9774 / 100


                lower_bound = predicted_price * (1 - dip)
                upper_bound = predicted_price * (1 + dip)


                price_range = f"{lower_bound / 1e6:.1f} - {upper_bound / 1e6:.1f} млн руб."


                error = "Расчёт выполнен успешно"
            else:
                error = 'Укажите местоположение на карте'
                form.add_error(None, 'Укажите местоположение на карте')
        else:
            error = 'Пожалуйста, исправьте ошибки в форме'
    else:
        form = RealEstateForm()


    if predicted_price is not None and form.is_bound and form.is_valid():
        formatted_price = f"{predicted_price:,.0f}".replace(',', ' ')
        price_kvm = f"{predicted_price / float(form.cleaned_data['total_area']):,.0f}".replace(',', ' ')
    else:
        formatted_price = None
        price_kvm = None

    context = {
        'form': form,
        'error': error,
        'predicted_price': formatted_price,
        'price_range': price_range,
        'price_kvm': price_kvm,
    }
    return render(request, 'main/input.html', context)