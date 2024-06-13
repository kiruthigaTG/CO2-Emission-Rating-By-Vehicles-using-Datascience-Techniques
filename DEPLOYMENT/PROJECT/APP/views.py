from django.shortcuts import render, redirect
from . models import UserPersonalModel
from . forms import UserRegisterForm, UserPersonalForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
import numpy as np

import numpy as np
import tensorflow as tf
from tensorflow import keras



def Landing_1(request):
    return render(request, '1_Landing.html')

def Register_2(request):
    form = UserRegisterForm()
    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was successfully created. ' + user)
            return redirect('Login_3')

    context = {'form':form}
    return render(request, '2_Register.html', context)


def Login_3(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('Home_4')
        else:
            messages.info(request, 'Username OR Password incorrect')

    context = {}
    return render(request,'3_Login.html', context)

def Home_4(request):
    return render(request, '4_Home.html')

def Teamates_5(request):
    return render(request,'5_Teamates.html')

def Domain_Result_6(request):
    return render(request,'6_Domain_Result.html')

def Problem_Statement_7(request):
    return render(request,'7_Problem_Statement.html')

def Per_Info_8(request):
    if request.method == 'POST':
        fieldss = ['firstname','lastname','age','address','phone','city','state','country']
        form = UserPersonalForm(request.POST)
        if form.is_valid():
            print('Saving data in Form')
            form.save()
        return render(request, '4_Home.html', {'form':form})
    else:
        print('Else working')
        form = UserPersonalForm(request.POST)    
        return render(request, '8_Per_Info.html', {'form':form})
    
loaded_model = keras.models.load_model('C:/Users/hp/Music/FINAL_PROJECT/CODE/DEPLOYMENT/PROJECT/APP/MODEL.h5')

def Deploy_9(request): 
    if request.method == "POST":
        f1 = request.POST.get('Engine_Size', 0)
        f2 = request.POST.get('Cylinders', 0)
        f3 = request.POST.get('Fuel_Type', 0)
        f4 = request.POST.get('Fuel_Consumption_City', 0)
        f5 = request.POST.get('Fuel_Consumption_Higway', 0)
        f6 = request.POST.get('Fuel_Consumption_km', 0)
        f7 = request.POST.get('Fuel_Consumption_miles', 0)
        f8 = request.POST.get('CO2_Emission_KM', 0)

        # Create a NumPy array from the input features.
        input_data = np.array([[f1,f2,f3,f4,f5,f6,f7,f8]], dtype=float)
        print(input_data)

        predicted_probabilities = loaded_model.predict(input_data)

        predicted_label = np.argmax(predicted_probabilities, axis=1)[0]

        print(f"Predicted Label: {predicted_label}")

        if predicted_label == 1:
            predicted_label = "THE LESS LEVEL OF CO2 DETECTED IN THIS CONDITIONS" 
        elif predicted_label == 2:
            predicted_label = "THE MODERATE LEVEL OF CO2 DETECTED IN THIS CONDITIONS"
        elif predicted_label == 3:
            predicted_label = "THE HIGH LEVEL OF CO2 DETECTED IN THIS CONDITIONS"
        elif predicted_label == 4:
            predicted_label = "THE VERY HIGH LEVEL OF CO2 DETECTED IN THIS CONDITIONS"

        return render(request, '9_Deploy.html', {"prediction_text":predicted_label})
    else:
        return render (request, '9_Deploy.html')

def Per_Database_10(request):
    models = UserPersonalModel.objects.all()
    return render(request, '10_Per_Database.html', {'models':models})

def Logout(request):
    logout(request)
    return redirect('Landing_1')
