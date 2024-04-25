from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
import numpy as np

from .serializers import carSerializer
from rest_framework import status
import os
from django.conf import settings
# Construct the absolute file path within the Docker container
file_path = os.path.join(settings.BASE_DIR, 'cardata.csv')
# Load the dataset
d = pd.read_csv(file_path)
d=d.drop('Owner',axis=1)
from sklearn.preprocessing import LabelEncoder
l=LabelEncoder()
d['Car_Name']=l.fit_transform(d['Car_Name'])
d['Fuel_Type']=l.fit_transform(d['Fuel_Type'])
d['Seller_Type']=l.fit_transform(d['Seller_Type'])
d['Transmission']=l.fit_transform(d['Transmission'])
x=d.drop('Selling_Price',axis=1)
y=d['Selling_Price']
from sklearn.model_selection import train_test_split
xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.2,random_state=1)
from sklearn.linear_model import LinearRegression
le=LinearRegression()
le.fit(xtrain,ytrain)

@api_view(['POST'])
def predict(request):
    if request.method == 'POST':
        serializer = carSerializer(data=request.data)
        if serializer.is_valid():
            input_data = tuple(serializer.validated_data.values())
            input_numpy = np.asarray(input_data).reshape(1, -1)
            out = le.predict(input_numpy)
            # Handle the case where 'out' is not assigned in all execution paths
            prediction = out
            return Response({'prediction': prediction}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)