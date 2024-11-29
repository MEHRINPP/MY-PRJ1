from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import SignupForm,LoginForm,UserUpdateForm
from .models import User
from django.contrib.auth import authenticate,login 
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q


def signup(request):
    if request.method=="POST":
        form=SignupForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=User.objects.create_user(username=username,email=email,password=password)
            user.save()
            return redirect('login')
    else:
        form=SignupForm()
    return render(request,'accounts/signup.html',{'form':form})

@never_cache
def login_view(request):
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']

            user=authenticate(request,username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    if user.is_superuser:
                        return redirect('admin_login')
                    else:
                        return redirect('user_list')
                else:
                    messages.error(request,'Your account is inactive. Please contact support.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Form is invalid. Please check the fields and try again.')
                
    else:
        form=LoginForm()
    return render(request,'accounts/login.html',{'form':form})
@login_required
@never_cache
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('user_list')
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(request,username=username,password=password)
        if user is not None and user.is_superuser:
                login(request,user)
                request.session['admin_logged_in']=True
                return redirect('user_list')
        else:
             return HttpResponse('Invalid admin  credentials.')
    return render(request,'accounts/admin_login.html')
@never_cache
@login_required
def user_list(request):
    if not request.session.get('admin_logged_in',False):
        return redirect('admin_login')
    search_query=request.GET.get('search','')
    if search_query:
        users=User.objects.filter(
            Q(username__istartswith=search_query) |Q(email__istartswith=search_query)
        )
    else:
        users=User.objects.all()
    return render(request,'accounts/user_list.html',{'users':users,'search_query':search_query})
@never_cache
@login_required
def create_user(request):
    if request.method=="POST":
        form=UserUpdateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form=UserUpdateForm()
    return render(request,'accounts/create_user.html',{'form':form})
@never_cache
@login_required
def edit_user(request,user_id):
    try:
        user=User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponse("User not found")
    if request.method=="POST":
        form=UserUpdateForm(request.POST,instance=user)
        if form.is_valid():
            new_email=form.cleaned_data.get('email')
            if User.objects.filter(email=new_email).exclude(id=user.id).exists():
                form.add_error('email','This email is already taken by another user.')
            else:
                form.save()
                return redirect('user_list')
    else:
        form=UserUpdateForm(instance=user)
    return render(request,'accounts/edit_user.html',{'form':form})


@login_required
def delete_user(request,user_id):
    user=User.objects.get(id=user_id)
    user.delete()
    return redirect('user_list')

def logout(request):
    request.session.flush()
    return redirect('login')




            
