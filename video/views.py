from django.shortcuts import render, redirect,HttpResponse,get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import authenticate
from . models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from .utils import get_video_duration
from django.http import JsonResponse
from django.urls import reverse

def home(request):
    
    videos=Videostore.objects.all().order_by('-date')

    

    return render(request,'home.html',{'videos':videos})



def signup(request):
    
    form=CustomUserForm()

    if request.method== 'POST':

        form=CustomUserForm(request.POST)

        

        if form.is_valid():
            
           user=form.save(commit=False) 

           password=form.cleaned_data['password']

           user.set_password(password)

           user.save()
           return redirect('login')
         
    return render(request,'signup.html',{'form':form})
 
def login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

             
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')  # Redirect to a different page after login
            else:
                form.add_error(None, 'Invalid username or password.')

    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('home')   

@login_required
def video_create(request):
    if request.method == 'POST':
        form = VideostoreForm(request.POST, request.FILES)
        if form.is_valid():
            videostore = form.save(commit=False)
            videostore.user = request.user
            videostore.save()
# Get the file path after saving the instance
            video_path = videostore.video.path
            duration = get_video_duration(video_path)
 # Update the instance with the duration
            videostore.duration=duration

            videostore.save()
            
            return redirect('home')
    else:
        form = VideostoreForm()

    return render(request, 'create.html', {'form': form})

def edit_video(request, pk):
    video = get_object_or_404(Videostore, pk=pk)
    if request.method == 'POST':
        form = EditvideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EditvideoForm(instance=video)
    return render(request, 'editvideo.html', {'video': video, 'form': form})

def videolist(request):

    video=Videostore.objects.all().order_by('-date')

    return render(request,'videolist.html',{'video':video})

def delete_video(request,pk):

    video=get_object_or_404(Videostore,pk=pk)

    video.delete()

    return redirect('home')

#session saves datas as key value pairs so values shouls be string 
def video_detail(request, pk):
    video = get_object_or_404(Videostore, pk=pk)
    comment=Comment.objects.filter(video=video)
    liked_videos = request.session.get('liked_videos', {})
    liked = str(pk) in liked_videos
    # Assuming you have a field 'like_count' in your Video model
    like_count = video.like_count
    like_url = reverse('like_video', args=[pk])
    unlike_url = reverse('unlike_video', args=[pk])
    return render(request, 'video_detail.html', {
        'video': video, 
        'liked': liked, 
        'like_count': like_count, 
        'like_url': like_url, 
        'unlike_url': unlike_url,
        'comment':comment
    })

def like_video(request, pk):
    liked_videos = request.session.get('liked_videos', {})
    #ensuring user liked or not
    if str(pk) not in liked_videos:
        #if so it stores as true so that we can count the number of true(likes count)
        liked_videos[str(pk)] = True
        request.session['liked_videos'] = liked_videos
        # Increment the like count in the database
        video = get_object_or_404(Videostore, pk=pk)
        video.like_count += 1
        video.save()
        return JsonResponse({'success': True, 'like_count': video.like_count})

def unlike_video(request, pk):
    liked_videos = request.session.get('liked_videos', {})
    if str(pk) in liked_videos:
        del liked_videos[str(pk)]
        request.session['liked_videos'] = liked_videos
        # Decrement the like count in the database
        video = get_object_or_404(Videostore, pk=pk)
        video.like_count -= 1
        video.save()
        return JsonResponse({'success': True, 'like_count': video.like_count})
 
@login_required
def edit_dashboard(request,pk):
    user=get_object_or_404(CustomUser,pk=pk)
    if request.method == 'POST':
        user_form = EditCustomUserForm(request.POST, request.FILES, instance=user)
        
        if user_form.is_valid():
            user_form.save()
            
            return redirect('dashboard', user.pk)   
    else:
        user_form = EditCustomUserForm(instance=user)
      

    return render(
        request,
        'edit_dashboard.html',
        {'user_form': user_form,
         'user':user}
    )

@login_required
def follow(request,pk):

    user_to_follow=get_object_or_404(CustomUser,pk=pk)

    if request.user!=user_to_follow:#checking both user doesnot have the same id 
        Follow.objects.get_or_create(follower=request.user,followed=user_to_follow)

    return redirect('dashboard', pk=pk)


@login_required
def unfollow_user(request,pk):
    user_to_unfollow = get_object_or_404(CustomUser,pk=pk)
    Follow.objects.filter(follower=request.user, followed=user_to_unfollow).delete()
    return redirect('dashboard',pk=pk)

 
 
@login_required
def dashboard(request,pk):
     user=get_object_or_404(CustomUser,pk=pk)
     
     is_following=Follow.objects.filter(follower=request.user,followed=user).exists()

     return render(request, 'dashboard.html', {
         'user': user,
         'is_following':is_following,
         'followers_count':user.followers_count(),
         'following_count':user.following_count()})


def followers_list(request,pk):

    user=get_object_or_404(CustomUser,pk=pk)

    followers=user.followers.all()

    return render(request, 'followers_list.html', {'user': user, 'followers': followers})


def following_list(request,pk):

    user = get_object_or_404(CustomUser, pk=pk)
    following = user.following.all()
    return render(request, 'following_list.html', {'user': user, 'following': following})


def createcomment(request,pk):

    video=get_object_or_404(Videostore,pk=pk)

    if request.method=='POST':

        form=CommentForm(request.POST)

        if form.is_valid():

            user=form.save(commit=False)

            user.user=request.user
            
            user.video=video

            user.save()

            return redirect('video_detail',video.pk)
    
    return render(request,'video_detail.html',{'user':user})


def listcomment(request):
    
    
    comment=Comment.objects.all()

    return render(request,'video_detail.html',{'comment':comment})