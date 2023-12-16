from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from itertools import chain
import random
# Create your views here.
def chat(request):
    return render(request, 'messages.html')
