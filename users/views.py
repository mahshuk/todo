import json

from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from users.forms import UserForm, ToDoTask
from tasks.models import ToDo
from main.functions import generate_form_errors


def login(request):
    if request.method == 'POST':  
        username = request.POST.get('username')
        password = request.POST.get('password')  

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect("/")
            else:
                context = {
                    "error": True,
                    "message": "Invalid username or password",
                }
                return render(request, "users/login.html", context=context)
        else:
            context = {
                "error": True,
                "message": "Invalid username or password",
            }
            return render(request, "users/login.html", context=context)

    context = {}
    return render(request, "users/login.html", context=context)


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("web:login"))


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            User.objects.create_user(
                username=instance.username,
                password=instance.password,
                email=instance.email,
                first_name=instance.first_name,
                last_name=instance.last_name,
            )

            user = authenticate(request, username=instance.username, password=instance.password)
            auth_login(request,user)

            return HttpResponseRedirect("/")
        else:
            message = generate_form_errors(form)

            form = UserForm()
            context = {
                    "title": "Sign Up",
                    "error": True,
                    "message": message,
                    "form": form,
                }
            return render(request, "users/signup.html", context=context)
    else:
        form = UserForm()
        context = {
            "title" : "Sign Up",
            "form" : form,
        }
        return render(request, "users/signup.html", context=context)



@login_required
def create_task(request):
    if request.method == "POST":
        form = ToDoTask(request.POST)
        if form.is_valid():
            user_assigned_to_task = request.user
            leader_user = form.cleaned_data['leader']  
            related_subject = form.cleaned_data['subject']
            related_exam = form.cleaned_data['exam']
            some_date = form.cleaned_data['date']

            instance = form.save(commit=False)
            instance.username = user_assigned_to_task
            instance.leader = leader_user
            instance.save()

            response_data = {
                "title": "Successfully submitted",
                "message": "Task Added successfully",
                "status": "success",
                "redirect": "yes",
                "redirect_url": "/",
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        else:
            error_message = generate_form_errors(form)
            response_data = {
                "title": "form validation error",
                "message": str(error_message),
                "status": "error",
                "stable": "yes"
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json")

    else:
        form = ToDoTask()

    return render(request, 'your_template.html', {'form': form})
        
@login_required
def edit_task(request,id):
    instance = get_object_or_404(ToDo, id=id)
    instance.delete()
    if request.method == 'POST':
        form = ToDoTask(request.POST, instance=instance)
        if instance.username == request.user:
            if form.is_valid():
                form.save()
                
            return render(request, "index.html", context=context)
        
    else:
        form = ToDoTask(instance=instance)
        username = request.user
        instances = ToDo.objects.filter(is_deleted=False,username=username,is_completed=False)
        completed_instances = ToDo.objects.filter(is_deleted=False,username=username,is_completed=True)
        context={
            "title": "Edit Task",
            "form":form,
            "instances": instances,
            "completed_instances": completed_instances
        }

        return render(request, "index.html", context=context)    


@login_required
def delete_task(request,uuid):
    instance = get_object_or_404(ToDo, id=uuid)
    instance.is_deleted=True
    instance.delete()

    response_data = {
        "title": "Successfully deleted",
        "message": "Task deleted successfully",
        "status": "success",
    }

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required
def finish_task(request,uuid):
    instance = get_object_or_404(ToDo, id=uuid)
    instance.is_completed=True
    instance.save()

    return HttpResponseRedirect(reverse('web:index'))

@login_required
def revise_task(request,uuid):
    instance = get_object_or_404(ToDo, id=uuid)
    instance.is_completed=False
    instance.save()

    return HttpResponseRedirect(reverse('web:index'))


@login_required
def exam(request):
    instances=ToDo.objects.all()
    context={
        "instances": instances
    }
    return render(request,"index.html",context=context)

