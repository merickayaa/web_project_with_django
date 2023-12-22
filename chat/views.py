from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import datetime
from itertools import chain
from .models import Message,Thread
from main.models import User
import random
# Create your views here.

def messagesView(request):
    return render(request, 'messages.html')

def new_message(request):
    if request.method == 'POST':
        pass

def dm(request):
    return render(request, 'dm.html')
