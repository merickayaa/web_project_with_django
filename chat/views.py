from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.views import View
from django.views.generic.edit import UpdateView,DeleteView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import datetime
from itertools import chain
from .models import Message,Thread
from main.models import User
import random
from .forms import ThreadForm,MessageForm
# Create your views here.
class ListThread(View):
    def get(self, request, *args, **kwargs):
        user_object = User.objects.get(username = request.user.username)
        threads = Thread.objects.filter(Q(user=request.user) | Q(receiver=request.user))
        form =ThreadForm()
        context = {
            'threads':threads,
            'form':form,
            'user_profile':user_object
        }
        return render(request, 'messages.html', context)
    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            try:
                receiver = User.objects.get(username=username)
                if Thread.objects.filter(user=request.user, receiver=receiver).exists():
                    thread = Thread.objects.filter(user=request.user, receiver=receiver)[0]
                    return redirect('thread', pk=thread.pk)
                elif Thread.objects.filter(user=receiver, receiver=request.user).exists():
                    thread = Thread.objects.filter(user=receiver, receiver=request.user)[0]
                    return redirect('thread', pk=thread.pk)

                new_thread = Thread(user=request.user, receiver=receiver)
                new_thread.save()
                return redirect('thread', pk=new_thread.pk)
            except User.DoesNotExist:
                print("Kullanıcı bulunamadı")
                return redirect('messages')

        else:
            print("Form geçerli değil")
            return redirect('messages')

class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        user_object = User.objects.get(username = request.user.username)
        thread = Thread.objects.get(pk=pk)
        message_list = Message.objects.filter(thread__pk__contains=pk)
        context= {
            'thread':thread,
            'form':form,
            'message_list':message_list,
            'user_profile':user_object
        }
        return render(request,'dm.html', context)
    
class CreateMessage(View):
    def post(self,request,pk,*args,**kwargs):
        thread = Thread.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        message = Message(thread=thread,sender_user=request.user,receiver_user=receiver,body=request.POST.get('message'))
        message.save()
        return redirect('thread', pk=pk)