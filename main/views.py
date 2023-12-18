from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from .models import Post, User,LikePost, Follower, Comment
from django.contrib.auth.decorators import login_required
from datetime import datetime
from itertools import chain
import random

# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username = request.user.username)
    posts = Post.objects.all()
    user_following_list = []
    feed = []
    user_following = Follower.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user__username=usernames)
        feed.append(feed_lists)

    feed_list = Post.objects.filter(user__username__in=user_following_list)

    # user suggestions start
    all_users = User.objects.all()

    # Assuming 'follower' is the correct attribute in your Follower model
    user_following_all = [User.objects.get(username=user.user) for user in user_following]

    new_suggestions_list = [user for user in all_users if user not in user_following_all]
    current_user = User.objects.get(username=request.user.username)  # Use get instead of filter
    final_suggestions_list = [user for user in new_suggestions_list if user != current_user]

    random.shuffle(final_suggestions_list)
    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = User.objects.filter(id=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))
    return render(request, 'platform.html', {'user_profile':user_object, 'posts':feed_list,'suggestions_username_profile_list':suggestions_username_profile_list[:4]})


@login_required(login_url='signin')
def comment(request):
    if request.method == 'POST':
        # POST isteğinden yorum verilerini al
        comment_text = request.POST.get('comment')
        post_id = request.POST.get('post_id')
        # İlgili postu bul
        post = get_object_or_404(Post, id=post_id)
        print(post)

        # Yeni bir Comment nesnesi oluştur ve kaydet
        new_comment = Comment(text=comment_text, post=post, user=request.user)
        new_comment.save()

        # Başarılı bir yanıt gönder
        return JsonResponse({'status': 'success', 'message': 'Yorumunuz başarıyla eklendi.'})


@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username = request.user.username)
    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)
        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)
        
        for ids in username_profile:
            profile_list = User.objects.filter(id=ids)
            username_profile_list.append(profile_list)
        username_profile_list = list(chain(*username_profile_list))


    return render(request, 'search.html', {'user_profile':user_object, 'username_profile_list':username_profile_list})

@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')
    

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')


def signup(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        userno = request.POST['userno']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        slug = request.POST['username']
        if len(userno) == 12:
            fifth_value =[int(userno[4]),int(userno[5]),int(userno[6])]
            num_str = ''.join(map(str,fifth_value))
            print(fifth_value)
            print(num_str)
            if num_str == "114" or num_str == "214":
                if password == password2:
                    if User.objects.filter(email=email).exists():
                        messages.info(request, "Email Zaten Kullanılıyor!")
                        return redirect('signup')
                    elif User.objects.filter(username=username).exists():
                        messages.info(request, "Kullanıcı Adı Zaten Kullanılıyor!")
                        return redirect('signup')
                    else:
                        user = User.objects.create_user(first_name=firstname,last_name=lastname,username=username, student_no=userno, email=email, password=password, slug=slug)
                        user.save()

                        user_login = authenticate(username=username,password=password)
                        login(request, user_login)
                        return redirect('signin')
                else:
                    messages.info(request, "Şifre Eşleşmiyor!")
                    return redirect('signup')
            else:
                messages.info(request, "Bu Siteye Kaydolmak İçin Bilgisayar Programcılığı Öğrencisi Olmalısınız!")
                return redirect('signup')
        else:
            messages.info(request, "Öğrenci Numaranız 11 Karakterden Oluşmalı!")
            return redirect('signup')
    else:
        return render(request, 'register.html')
    

def signin(request):
    if request.method == 'POST':
        # İki Seçenek Var. Ya username ile giriş alacağız ya da yeni bir user modeli oluşturcağız.
        student_no = request.POST.get('student_no')
        password = request.POST.get('password')

        user = authenticate(request, student_no=student_no, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Girilen Bilgiler Yanlış!")
            return redirect('signin')
    else:
        return render(request, 'signin.html')
    
    
@login_required(login_url='signin')
def Logout(request):
    logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def dashboard(request, user_slug):
    profile = User.objects.get(slug=user_slug)
    posts = Post.objects.filter(user=profile)
    follower = request.user.username
    user = user_slug
    followerCount = len(Follower.objects.filter(user=user_slug))
    postCount = len(posts)
    followingCount = len(Follower.objects.filter(follower=user_slug))
    if Follower.objects.filter(follower=follower, user=user):
        button_text = 'Takibi Birak'
    else:
        button_text = 'Takip Et'
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = profile.profileimg
            job = request.POST['job']
            company_name = request.POST['company_name']
            type_of_work = request.POST['types_work']
            colloge = request.POST['college']
            country = request.POST['country']
            city = request.POST['city']
            phone_number = request.POST['phone_number']
            birthday = request.POST['birthday']
            
            # Doğru tarih formatını kontrol etmek ve işlemek için datetime kullanın
            try:
                birthday_date = datetime.strptime(birthday, '%Y-%m-%d').date()
                profile.birthday = birthday_date
            except ValueError:
                messages.info(request, "Geçerli Bir Tarih Giriniz!")

            profile.profileimg = image
            profile.job = job
            profile.company_name = company_name
            profile.type_of_work = type_of_work
            profile.college = colloge
            profile.country = country
            profile.city = city
            profile.phone_number = phone_number
            profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            job = request.POST['job']
            company_name = request.POST['company_name']
            type_of_work = request.POST['types_work']
            colloge = request.POST['college']
            country = request.POST['country']
            city = request.POST['city']
            phone_number = request.POST['phone_number']
            birthday = request.POST['birthday']
            try:
                birthday_date = datetime.strptime(birthday, '%d-%m-%Y').date()
                profile.birthday = birthday_date
            except ValueError:
                messages.info(request, "Geçerli Bir Tarih Giriniz!")

            profile.profileimg = image
            profile.job = job
            profile.company_name = company_name
            profile.type_of_work = type_of_work
            profile.college = colloge
            profile.country = country
            profile.city = city
            profile.phone_number = phone_number
            profile.save()
        return redirect('dashboard',user_slug)
    user_following_list = []
    feed = []
    user_following = Follower.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user__username=usernames)
        feed.append(feed_lists)

    feed_list = Post.objects.filter(user__username__in=user_following_list)
    # user suggestions start
    all_users = User.objects.all()

    # Assuming 'follower' is the correct attribute in your Follower model
    user_following_all = [User.objects.get(username=user.user) for user in user_following]

    new_suggestions_list = [user for user in all_users if user not in user_following_all]
    current_user = User.objects.get(username=request.user.username)  # Use get instead of filter
    final_suggestions_list = [user for user in new_suggestions_list if user != current_user]

    random.shuffle(final_suggestions_list)
    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = User.objects.filter(id=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(request, 'dashboard.html', {'user_profile':profile, 'posts':posts, 'button_text':button_text,'followerCount':followerCount,'postCount':postCount, 'followingCount':followingCount,'suggestions_username_profile_list':suggestions_username_profile_list})


@login_required(login_url='signin')
def posts(request,user_slug):
    profile = User.objects.get(slug=user_slug)
    posts = Post.objects.filter(user=profile)
    user_following_list = []
    feed = []
    user_following = Follower.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user__username=usernames)
        feed.append(feed_lists)

    feed_list = Post.objects.filter(user__username__in=user_following_list)
    # user suggestions start
    all_users = User.objects.all()

    # Assuming 'follower' is the correct attribute in your Follower model
    user_following_all = [User.objects.get(username=user.user) for user in user_following]

    new_suggestions_list = [user for user in all_users if user not in user_following_all]
    current_user = User.objects.get(username=request.user.username)  # Use get instead of filter
    final_suggestions_list = [user for user in new_suggestions_list if user != current_user]

    random.shuffle(final_suggestions_list)
    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = User.objects.filter(id=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))
    context = {
        'user_profile':profile,
        'posts':posts,
        'suggestions_username_profile_list':suggestions_username_profile_list
    }
    return render(request,'posts.html', context)


@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        print("1: ",follower)
        print("2: ",user)
        if Follower.objects.filter(follower=follower, user=user).first():
            delete_follower = Follower.objects.get(follower=follower, user=user)
            print("3: ",delete_follower)
            delete_follower.delete()
            return redirect('/dashboard/'+user)
        else:
            new_follower = Follower.objects.create(follower=follower,user=user)
            print("4: ",new_follower)
            new_follower.save()
            return redirect('/dashboard/'+user)
    else:
        return redirect('/')
