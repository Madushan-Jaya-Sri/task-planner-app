from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task, Label, BackgroundImage
from .forms import TaskForm
import datetime
import random
from .gemini_request import send_gemini_request

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task, Label, BackgroundImage
from .forms import TaskForm
import datetime
import random
from .gemini_request import send_gemini_request

label_list = ['sleep', 'gym', 'study', 'play']
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from tasks.models import Task, Label
import datetime
import random


from django.utils import timezone

from django.utils import timezone
import datetime
import random
from datetime import datetime

import pytz

from datetime import datetime
import pytz
from django.utils import timezone


def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form})



@login_required
def edit_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.delete()
    return redirect('dashboard')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            print(form.errors)
            return render(request, 'tasks/register.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'tasks/register.html', {'form': form})



@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render, get_object_or_404
from .models import Label, BackgroundImage
from .gemini_request import send_gemini_request


label_list =['sleep','gym','study','play']





@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    
    # Set the Sri Lanka timezone
    sri_lanka_tz = pytz.timezone('Asia/Colombo')
    
    # Get the current time in Sri Lanka
    current_time = datetime.now(sri_lanka_tz)  # This is timezone-aware with Sri Lanka time
    print("this is current time $$$$$$$$$",current_time)
    # Initialize the default background image
    background_image = 'default_background.jpg'

    if tasks.exists():
        smallest_difference = None
        closest_task = None

        for task in tasks:
            # Combine date and time to create a timezone-aware datetime
            task_datetime = timezone.make_aware(
                timezone.datetime.combine(task.date, task.time),
                sri_lanka_tz
            )

            # Calculate the time difference
            time_difference = abs(task_datetime - current_time)

            if smallest_difference is None or time_difference < smallest_difference:
                smallest_difference = time_difference
                closest_task = task

        if closest_task:
            # Get the predicted label for the closest task
            predicted_label = get_predicted_label(closest_task.title, closest_task.description)
            
            # Set the background image based on the predicted label
            if predicted_label == 'gym':
                background_image = 'bg1.png'
            elif predicted_label == 'sleep':
                background_image = 'sleep1.jpeg'
            elif predicted_label == 'play':
                background_image = 'play2.jpeg'
            # Add more conditions for other predictions here
            else:
                background_image = 'default_background.jpg'

    # Fallback background image based on the time of day if no specific image is set
    if current_time.hour < 11 and background_image == 'default_background.jpg':
        background_image = 'backgroundimg1.jpg'
    elif background_image == 'default_background.jpg':
        background_image = 'bg1.png'

    return render(request, 'tasks/dashboard.html', {
        'tasks': tasks,
        'background_image': background_image,
    })

def get_predicted_label(task_title, task_description):

    print(task_title)
    print(task_description)
    prompt = (f"Given the following task details:\n"
              f"Title: {task_title}\n"
              f"Description: {task_description}\n"
              f"What is the most appropriate label?\n"
              f"The answer should be one of the following label list: {label_list}")

    response_json = send_gemini_request(prompt)
    print("Response JSON:", response_json)  # Log the entire response for debugging

    if response_json:
        candidates = response_json.get('candidates', [])
        if candidates:
            predicted_label = candidates[0]['content']['parts'][0]['text']
            print("Predicted Label:", predicted_label)
            return predicted_label.strip()

    print("No valid prediction found.")
    return None



