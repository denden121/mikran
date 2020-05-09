from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Profile, Project, Report
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication 

@csrf_exempt
def cabinet_view(request,user_id):
    token = request.headers.get('Authorization')
    validated_token = JWTAuthentication().get_validated_token(token)
    user = JWTAuthentication().get_user(validated_token)
    if user and user.id == user_id or user.is_staff:
        profile = Profile.objects.filter(user=user)
        return HttpResponse(profile.values('group', 'sex', 'subdivision', 'birth_date', 'position', 'experience', 'shift', 'part_time_job', 'lateness'))
    else:
        return HttpResponse("Fail")

@csrf_exempt
def all_report_view(request, user_id):
    token = request.headers.get('Authorization')
    validated_token = JWTAuthentication().get_validated_token(token)
    user = JWTAuthentication().get_user(validated_token)
    if request.method == "GET":
        if user_id != user.id and not user.is_staff:
            return HttpResponse("You dont have permissions")
        reports = Report.objects.filter(user=user_id)
        return HttpResponse(reports.values())
    elif request.method == "POST":
        if user_id != user.id:
            return HttpResponse("You dont have permissions")
        name = request.POST['name']
        project = request.POST['project']
        text = request.POST['text']
        hour = request.POST['hour']
        project = Project.objects.get(name=project)
        profile = Profile.objects.get(user=user)
        if project:
            new_report = Report.objects.create(name = name, project = project, text = text, hour = hour, user=profile)
            new_report.save()
            return HttpResponse("Succesfull")
        return HttpResponse("Something went wrong")
        

@csrf_exempt
def report_view(request, user_id, report_id):
    token = request.headers.get('Authorization')
    validated_token = JWTAuthentication().get_validated_token(token)
    user = JWTAuthentication().get_user(validated_token)
    if user_id != user.id and not user.is_staff:
        return HttpResponse("You dont have permissions")
    if request.method == "GET":
        report = Report.objects.get(user=user_id, id=report_id)
        return HttpResponse(report.name)
    elif request.method == "POST":
        if user_id != user.id:
            return HttpResponse("You dont have permissions")
     
        new_report = Report.objects.filter(id = report_id)
        if 'name' in request.POST:
            name = request.POST['name']
            new_report.update(name = name)
        if 'text' in request.POST:
            text = request.POST['text']
            new_report.update(text = text)
        if 'hour' in request.POST:
            hour = request.POST['hour']
            new_report.update(hour = hour)
        return HttpResponse("Succesfull")

    elif request.method == "DELETE":
        report = Report.objects.get(user=user_id, id=report_id)
        report.delete()
        return HttpResponse("Succesfull")

@csrf_exempt
def all_projects_view(request, user_id):
    token = request.headers.get('Authorization')
    validated_token = JWTAuthentication().get_validated_token(token)
    user = JWTAuthentication().get_user(validated_token)
    if request.method == "GET":
        if user_id != user.id and not user.is_staff:
            return HttpResponse("You dont have permissions")
        projects = Project.objects.filter(participants=user_id)
        return HttpResponse(projects.values())

    elif request.method == "POST":
        if user_id != user.id:
            return HttpResponse("You dont have permissions")
        name = request.POST['name']
        tasks = request.POST['tasks']
        participants = request.POST['users'].split()
        profiles = [Profile.objects.filter(user=participant) for participant in participants]
        if profiles:
            new_project = Project.objects.create(name = name, tasks = tasks)
            new_project.save()
            [new_project.participants.add(profiles[i].values('id')) for i in range(len(profiles))]
            return HttpResponse("Succesfull")
        return HttpResponse("Something went wrong")
        

@csrf_exempt
def project_view(request, user_id, project_id):
    token = request.headers.get('Authorization')
    validated_token = JWTAuthentication().get_validated_token(token)
    user = JWTAuthentication().get_user(validated_token)
    if user_id != user.id and not user.is_staff:
        return HttpResponse("You dont have permissions")
    if request.method == "GET":
        project = Project.objects.filter(participants=user_id, id=project_id)
        return HttpResponse(project.values())
    elif request.method == "POST":
        if user_id != user.id:
            return HttpResponse("You dont have permissions")
        
        new_project = Project.objects.filter(id = project_id)
        if 'name' in request.POST:
            name = request.POST['name']
            new_project.update(name = name)
        if 'tasks' in request.POST:
            tasks = request.POST['tasks']
            new_project.update(tasks = tasks)
        if 'status' in request.POST:
            status = request.POST['status']
            new_project.update(is_done = status)
        if 'users' in request.POST:
            new_project = Project.objects.get(id = project_id)
            participants = request.POST['users'].split()
            new_project.participants.set(participants)
        return HttpResponse("Succesfull")

    elif request.method == "DELETE":
        project = Project.objects.get(participants=user_id, id=project_id)
        project.delete()
        return HttpResponse("Succesfull")