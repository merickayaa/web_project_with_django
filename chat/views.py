from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import datetime
from itertools import chain
from .models import Messages,Thread
from main.models import User
import random
# Create your views here.
def chat(request):
    pass

def create_chat(request):
    pass

def dm(request,pk):
    pass
