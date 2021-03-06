import simplejson as json
from datetime import datetime
from django.contrib.auth import authenticate
from django.core import serializers
from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .project_export import export
from .departaments_scripts import get_endpoint_department, build_level_with_user

from .cabinet_scripts.cabinet import get_info_about_user
from .cabinet_scripts.reports import get_reports, get_reports_for_worker, create_reports
from .cabinet_scripts.projects import get_project, get_projects
from .cabinet_scripts.calendar import get_calendar
from .cabinet_scripts.groups import get_group, get_groups
from .cabinet_scripts.salary import change_salary_common
from django.contrib.auth.models import User

from .forms import ProjectForm, ReportForm, ActionForm, ProfileForm, \
    GroupForm, SalaryIndividualForm, RegisterForm
from .models import Profile, Project, Report, Action, Group, Logging, \
    SalaryCommon, SalaryIndividual, Department, Direction, TimeCard, GroupAction


def get_user_jwt(request):
    token = request.headers.get('Authorization')
    validated_token = JWTAuthentication().get_validated_token(token)
    user = JWTAuthentication().get_user(validated_token)
    # user = User.objects.get(username="admin")
    return user


def export_projects(request):
    export(1)
    return FileResponse(open('test.xls', 'rb'))


def get_department(subdepartment):
    if subdepartment.subdepartment_code != '0':
        print(subdepartment.subdepartment_code)
        department = Department.objects.get(department_code=subdepartment.subdepartment_code)
        return get_department(department)
    else:
        return subdepartment


def departament_new_view(request):
    user = get_user_jwt(request)
    if user:
        departments = Department.objects.filter(subdepartment_code='0')
        data = []
        date = f'{datetime.now().month}-{datetime.now().year}'
        for department in departments:
            data.append(build_level_with_user(department.id, 1, date, 1, 0))
        return HttpResponse(json.dumps(data, ensure_ascii=False).encode('utf8'))


def department_workers(request, department_id):
    user = get_user_jwt(request)
    if user:
        department = Department.objects.get(pk=department_id)
        data = build_level_with_user(department.id, 0, only_user=1)
        output = get_endpoint_department(data, [], 1)
        return HttpResponse(json.dumps(output, ensure_ascii=False).encode('utf8'))


def salary_new_view(request, department_id):
    user = get_user_jwt(request)
    if user:
        department = Department.objects.get(pk=department_id)
        if department.subdepartment_code == "0":
            date = request.GET.get("date")
            salary_flag = 1
            data = build_level_with_user(department.id, 0, date, 1, salary_flag)
            output = get_endpoint_department(data, [])
        else:
            date = request.GET.get("date")
            salary_flag = 1
            data = build_level_with_user(department.id, 0, date, 1, salary_flag)
            try:
                del data['subdepartments']
            except KeyError:
                pass
            output = get_endpoint_department(data, [])
        return HttpResponse(json.dumps(output, ensure_ascii=False).encode('utf8'))


def get_time_from_reports(profile):
    t = datetime.now()
    reports = Report.objects.filter(creator_id=profile.user.id, date__month=t.month, date__year=t.year)
    hour = 0
    hour = sum([report.hour + hour for report in reports])
    return hour


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def get_access(action_num, user):
    # try:
    #     Action.objects.get(group=user.profile.group, num=action_num)
    # except Action.DoesNotExist:
    #     return False
    return True


def logging(request, username, status, action):
    Logging.objects.create(IP=request.POST.get('IP'), login=username, status=status, action=action)


@csrf_exempt
def token(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    action = 'login'
    if user:
        status = True
        token_json = get_tokens_for_user(user)
        logging(request, username=username, status=status, action=action)
        return HttpResponse(json.dumps(token_json))
    else:
        status = False
        logging(request, username=username, status=status, action=action)
        return HttpResponse("False")


@csrf_exempt
def check_view(request):
    user = get_user_jwt(request)
    print(hasattr(user, 'profile'))
    print(user)
    return HttpResponse(hasattr(user, 'profile'))


@csrf_exempt
def check_group_name(request):
    name = request.POST.get('name')
    groups = Group.objects.filter(name=name)
    return HttpResponse(bool(groups))


@csrf_exempt
def check_admin_view(request):
    user = get_user_jwt(request)
    return HttpResponse(get_access(100, user))


@csrf_exempt
def cabinet_view(request, user_id='default'):
    user = get_user_jwt(request)
    if user_id == 'default':
        data = get_info_about_user(user.id)
        return HttpResponse(json.dumps(data, ensure_ascii=False).encode('-utf8'))
    else:
        if user:
            if request.method == "GET":
                data = get_info_about_user(user_id)
                return HttpResponse(json.dumps(data, ensure_ascii=False).encode('-utf8'))
            if request.method == "POST":
                profile = Profile.objects.get(user=user_id)
                form = ProfileForm(request.POST, request.FILES, instance=profile)
                print(form.errors)
                if form.is_valid():
                    form.save()
                data = get_info_about_user(user_id)
                return HttpResponse(json.dumps(data, ensure_ascii=False).encode('-utf8'))
        return HttpResponse("Permission denied")


@csrf_exempt
def register_view(request):
    user = get_user_jwt(request)
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES, instance=user.profile)
        print(form.errors)
        if form.is_valid():
            update = form.save(commit=False)
            update.user = user
            update.save()
            return HttpResponse("Success")
        return HttpResponse("Something went wrong")
    return HttpResponse('Method not allowed')


@csrf_exempt
def all_report_view(request, user_id='default'):
    user = get_user_jwt(request)
    if user_id == 'default':
        if user:
            if request.method == "GET":
                data = get_reports(request.GET.get('month'), request.GET.get('year'), user.id)
                return HttpResponse(json.dumps(data))
            elif request.method == "POST":
                return create_reports(request, user)
            return HttpResponse("Method not allowed")
        return HttpResponse("Authentication error")
    else:
        if user:
            profile = Profile.objects.get(user=user_id)
            if request.method == "POST":
                project_pk = request.POST.get('project')
                date = request.POST.get('date')
                year, month, day = date.split('-')
                reports = Report.objects.filter(creator_id=user_id, date__year=year,
                                                date__month=month, project=project_pk)
                if reports:
                    return HttpResponse("Already have a report")
                form = ReportForm(request.POST)
                print(form.errors)
                if form.is_valid():
                    report = form.save(commit=False)
                    report.creator_id = profile
                    report.save()
                    data = {'pk': report.pk, 'project': report.project.name, 'text': report.text, 'hours': report.hour,
                            'status': report.status, 'project_pk': report.project.pk}
                    return HttpResponse(json.dumps(data, ensure_ascii=False).encode('utf8'))
                return HttpResponse("Fail")
            return HttpResponse("Method not allowed")
        return HttpResponse("Authentication error")


@csrf_exempt
def report_view(request, report_id, user_id='default'):
    if user_id == 'default':
        user = get_user_jwt(request)
        if user:
            if request.method == "GET":
                report = Report.objects.filter(creator_id_id=user.id, id=report_id)
                data = serializers.serialize('json', report)
                return HttpResponse(data)
            elif request.method == "POST":
                project_pk = request.POST.get('project')
                date = request.POST.get('date')
                year, month, day = date.split('-')
                reports = Report.objects.filter(creator_id=user.id, date__year=year,
                                                date__month=month, project=project_pk)
                for report in reports:
                    if report.pk != report_id:
                        return HttpResponse("Already have a report")
                report = Report.objects.get(creator_id_id=user.id, id=report_id)
                form = ReportForm(request.POST, request.FILES, instance=report)
                print(form.errors)
                if form.is_valid():
                    form.save()
                    data = []
                    fields = {'project_name': report.project.name, 'text': report.text, 'hour': report.hour,
                              'status': report.status, 'project_pk': report.project.pk}
                    data.append({'pk': report.pk, 'fields': fields})
                    return HttpResponse(json.dumps(data[0], ensure_ascii=False).encode('utf8'))
                return HttpResponse("Fail")
            elif request.method == "DELETE":
                report = get_object_or_404(Report, pk=report_id)
                report.delete()
                return HttpResponse("Success")
            return HttpResponse("Method not allowed")
        return HttpResponse("Authentication error")
    else:
        user = get_user_jwt(request)
        if user:
            if request.method == "GET":
                if get_access(11, user):
                    checked_user = Profile.objects.get(pk=user_id)
                    report = Report.objects.filter(user=checked_user, id=report_id)
                    data = serializers.serialize('json', report)
                    return HttpResponse(data)
                return HttpResponse("You don't have permissions")
            elif request.method == "POST":
                project_pk = request.POST.get('project')
                date = request.POST.get('date')
                year, month, day = date.split('-')
                reports = Report.objects.filter(creator_id=user_id, date__year=year,
                                                date__month=month, project=project_pk)
                for report in reports:
                    if report.pk != report_id:
                        return HttpResponse("Already have a report")
                report = Report.objects.get(creator_id_id=user_id, id=report_id)
                form = ReportForm(request.POST, request.FILES, instance=report)
                print(form.errors)
                if form.is_valid():
                    form.save()
                    data = {'pk': report.pk, 'project': report.project.name, 'text': report.text, 'hours': report.hour,
                            'status': report.status, 'project_pk': report.project.pk}
                    return HttpResponse(json.dumps(data, ensure_ascii=False).encode('utf8'))
                return HttpResponse("Fail")
            return HttpResponse("Access error")
        return HttpResponse("Authentication error")


@csrf_exempt
def all_projects_view(request):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            data = get_projects()
            return HttpResponse(json.dumps(data))
        if request.method == "POST":  # 13 is create projects
            form = ProjectForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse("Success")
            print(form.errors)
            return HttpResponse("Something went wrong")
        return HttpResponse("Method not allowed")
    return HttpResponse("Authentication error")


@csrf_exempt
def project_view(request, project_id, user_id='default'):
    if user_id == 'default':
        user = get_user_jwt(request)
        if user:
            if request.method == "GET":
                data = get_project(project_id)
                return HttpResponse(json.dumps(data, ensure_ascii=False).encode('utf8'))
            elif request.method == "POST" and get_access(13, user):
                project = Project.objects.get(id=project_id)
                form = ProjectForm(request.POST, request.FILES, instance=project)
                if form.is_valid():
                    form.save()
                    data = get_project(project_id)
                    return HttpResponse(json.dumps(data, ensure_ascii=False).encode('utf8'))
            return HttpResponse("Method not allowed")
        return HttpResponse("Authentication error")
    else:
        user = get_user_jwt(request)
        if user:
            if request.method == "GET" or get_access(12, user):
                data = get_project(project_id)
                return HttpResponse(json.dumps(data, ensure_ascii=False).encode('utf8'))
            return HttpResponse("Method not allowed")
        return HttpResponse("Authentication error")


@csrf_exempt
def group_view(request, group_id):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            data = get_group(group_id)
            return HttpResponse(json.dumps(data))
        if request.method == "POST":
            group = GroupForm(request.POST)
            if group.is_valid():
                group.save(commit=False)
                if request.POST['actions']:
                    actions = request.POST['actions'].split()
                    actions = [Action.objects.get(pk=int(action)) for action in actions]
                    if actions and group.is_valid():
                        group = group.save()
                        [group.actions.add(actions[i]) for i in range(len(actions))]
                if request.POST['participants']:
                    participants = request.POST['participants'].split()
                    participants = [Profile.objects.get(pk=int(participant)) for participant in participants]
                    if participants:
                        [group.participants.add(participants[i]) for i in range(len(participants))]
                data = get_group(group_id)
                return HttpResponse(json.dumps(data))


@csrf_exempt
def change_group_view(request, group_id):
    user = get_user_jwt(request)
    if user:
        if request.method == "POST":
            group_obj = Group.objects.get(pk=group_id)
            group = GroupForm(request.POST, instance=group_obj)
            if group.is_valid():
                group.save()
                if 'actions' in request.POST:
                    print(request.POST.get('actions'))
                    actions = json.loads(request.POST.get('actions'))
                    for key, value in actions.items():
                        if value:
                            action = Action.objects.get(pk=int(key))
                            group_obj.actions.add(action)
                        if not value:
                            action = Action.objects.get(pk=int(key))
                            group_obj.actions.remove(action)
                # if 'participants' in request.POST:
                #     participants = request.POST['participants'].split()
                #     participants = [Profile.objects.get(pk=int(participant)) for participant in participants]
                #     if participants:
                #         group_obj.participants.clear()
                #         [group_obj.participants.add(participants[i]) for i in range(participants)]
                # else:
                #     group_obj.participants.clear()
                actions_group = group_obj.actions.all()
                participants = group_obj.participants.all()
                users = []
                actions = []
                for action in actions_group:
                    actions.append(action.action + ' ' + str(action.num))
                for profile in participants:
                    users.append({'name': profile.first_name + ' ' + profile.last_name + ' ' + profile.middle_name})
                fields = {'name': group_obj.name, 'description': group_obj.description,
                          'users': users, 'actions': actions}
                data = {'pk': group_obj.pk, 'fields': fields}
                return HttpResponse(json.dumps(data, ensure_ascii=False).encode("utf8"))


@csrf_exempt
def action_view(request):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            actions = Action.objects.all()
            data = []
            for action in actions:
                data.append({'pk': action.pk, 'name': action.action})
            return HttpResponse(json.dumps(data))
        if request.method == "POST":
            action = ActionForm(request.POST)
            if action.is_valid():
                action.save()
                return HttpResponse("Success")


@csrf_exempt
def available_actions(request):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            group = user.profile.group
            data = serializers.serialize('json', group.available_actions.all())
            return HttpResponse(data)


@csrf_exempt
def groups_with_permission(request):
    user = get_user_jwt(request)
    if request.method == "GET":
        if user and get_access(101, user):
            data = get_groups()
            return HttpResponse(json.dumps(data))
    if request.method == "POST":
        pk = request.POST.get('pk')
        group_obj = Group.objects.get(pk=pk)
        group = GroupForm(request.POST, instance=group_obj)
        if group.is_valid():
            update = group.save(commit=False)
            if request.POST.get('actions'):
                actions = request.POST['actions'].split()
                try:
                    actions = [Action.objects.get(pk=int(action)) for action in actions]
                except Action.DoesNotExist:
                    pass
                if actions:
                    [group_obj.available_actions.add(actions[i]) for i in range(len(actions))]
            if group.is_valid():
                group.save()
                return HttpResponse("Success")
            return HttpResponse("Something went wrong")


@csrf_exempt
def logs_with_range(request):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            logs = Logging.objects.filter(date__gt=start_date,
                                          date__lte=end_date)
            data = serializers.serialize('json', logs)
            return HttpResponse(data)


@csrf_exempt
def logs(request):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            year = request.GET.get('year')
            month = request.GET.get('month')
            logs = Logging.objects.filter(date__month=month, date__year=year)
            data = serializers.serialize('json', logs)
            return HttpResponse(data)


@csrf_exempt
def salary_norm(request):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            date = request.GET.get('date')
            month, year = date.split('-')
            salary_common, cr = SalaryCommon.objects.get_or_create(date=f'{year}-{month}-1')
            data = {'days_norm': salary_common.days_norm_common, 'time_norm': salary_common.time_norm_common}
            return HttpResponse(json.dumps(data))


@csrf_exempt
def change_salary(request):
    user = get_user_jwt(request)
    if user:
        if request.method == "POST":
            person = request.POST.get('person')
            person = Profile.objects.get(pk=person)
            year = request.POST.get('year')
            month = request.POST.get('month')
            hour = get_time_from_reports(person)
            date = f'{year}-{month}-1'
            salary_common, created = SalaryCommon.objects.get_or_create(date=date)
            salary, created = SalaryIndividual.objects.get_or_create(person=person, date=date)
            form = SalaryIndividualForm(request.POST, instance=salary)
            if form.is_valid():
                form.save()
                salary.time_from_report = hour
                salary.calculate(salary_common)
                salary.save()
                return HttpResponse("Success")
            return HttpResponse(form.errors.as_data())


@csrf_exempt
def salary_individual(request):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            person = Profile.objects.get(user=user)
            year = request.GET.get('year')
            month = request.GET.get('month')
            salary = get_object_or_404(SalaryIndividual, person=person, date__year=year, date__month=month)
            data = {'salary_hand': salary.salary_hand, 'day_off': salary.day_off, 'award': salary.award,
                    'days_worked': salary.days_worked, 'is_penalty': salary.is_penalty,
                    'vacation': salary.vacation, 'sick_leave': salary.sick_leave,
                    'time_from_report': salary.time_from_report,
                    'time_orion': salary.time_orion, 'time_norm': salary.time_norm, 'time_off': salary.time_off,
                    'plan_salary': salary.plan_salary}
            return HttpResponse(json.dumps(data))


@csrf_exempt
def workers_department(request, department_id):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            workers = Profile.objects.filter(department=department_id)
            data = []
            for worker in workers:
                data.append(
                    {'pk': worker.pk, 'name': " ".join([worker.last_name, worker.first_name, worker.middle_name])})
            return HttpResponse(json.dumps(data))


@csrf_exempt
def departament_simple_view(request):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            departments = Department.objects.filter(subdepartment_code=0)
            data = []
            for department in departments:
                data.append({'pk': department.pk, 'fields': {'code': department.department_code,
                                                             'name': department.department_name}})
            return HttpResponse(json.dumps(data))


@csrf_exempt
def workers_info(request):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            persons = Profile.objects.all().order_by('pk')
            data = []
            group_field = []
            for person in persons:
                groups = Group.objects.filter(participants=person)
                for group in groups:
                    group_field.append(group.name)
                field = {'full_name': person.last_name + ' ' + person.first_name + ' ' + person.middle_name,
                         'position': person.position, 'SRI_SAS': person.SRI_SAS,
                         'shift': person.shift, 'date': "2009-01-01",
                         'part_time_job': person.part_time_job,
                         'experience': person.experience, 'lateness': person.lateness,
                         '№ db': "321", '№ 1c': "3059", "sex": person.sex,
                         'birth_date': str(person.birth_date),
                         'oklad': person.oklad,
                         'groups': group_field}
                group_field = []
                data.append({'pk': person.pk, 'person': field})
            print(data)
            return HttpResponse(json.dumps(data))


@csrf_exempt
def workers_info_simple(request):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            persons = Profile.objects.all()
            data = []
            for person in persons:
                data.append({'pk': person.pk,
                             'full_name': person.last_name + ' ' + person.first_name + ' ' + person.middle_name})
            return HttpResponse(json.dumps(data))


@csrf_exempt
def managers(request):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            workers = Profile.objects.filter(position="Top")
            data = serializers.serialize('json', workers)
            return HttpResponse(data)


@csrf_exempt
def projects_for_reports(request):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            projects = Project.objects.all()
            data = []
            for project in projects:
                data.append({'pk': project.pk, 'project_name': project.name})
            return HttpResponse(json.dumps(data))


@csrf_exempt
def change_common_salary(request):
    user = get_user_jwt(request)
    if user:
        if change_salary_common(request):
            return HttpResponse("Success")
        return HttpResponse("Fail")


@csrf_exempt
def workers_project(request):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            workers = Profile.objects.all()
            data = serializers.serialize('json', workers, fields=('first_name', 'last_name', 'middle_name'))
            return HttpResponse(data)


@csrf_exempt
def managers_project(request):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            workers = Profile.objects.all()
            data = serializers.serialize('json', workers, fields=('first_name', 'last_name', 'middle_name'))
            return HttpResponse(data)


@csrf_exempt
def subdepartment_view(request):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            subdepartments = Department.objects.filter(subdepartment_code__exact=0)
            data = serializers.serialize('json', subdepartments)
            return HttpResponse(data)


@csrf_exempt
def subdepartment_from_departments_view(request, department_id):
    user = get_user_jwt(request)
    date = 'default'
    if user:
        if request.method == "GET":
            data = build_level_with_user(department_id, 0, date, only_user=0, salary_flag=0)
            data = get_endpoint_department(data, [])
            return HttpResponse(json.dumps(data, ensure_ascii=False).encode('utf8'))


@csrf_exempt
def direction_view(request):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            directions = Direction.objects.all()
            data = serializers.serialize('json', directions)
            return HttpResponse(data)


@csrf_exempt
def time_control_view(request):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            date = request.GET.get('date')
            user_id = request.GET.get('user_id')
            times_cards = TimeCard.objects.filter(user=user_id, date=date)
            data = serializers.serialize('json', times_cards)
            return HttpResponse(data)


@csrf_exempt
def time_control_view_detail(request):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            fields = []
            for i in range(5):
                if i % 2 == 0:
                    fields.append(
                        {'num': i, 'date': '2020-01-01', 'time': f'1{i}:20', 'commentary': 'Вершинина: Микран вход'})
                else:
                    fields.append(
                        {'num': i, 'date': '2020-01-01', 'time': f'1{i}:20', 'commentary': 'Вершинина: Микран выход'})
            return HttpResponse(json.dumps(fields))


@csrf_exempt
def calendar_control_view(request):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            data = get_calendar(request.GET.get('subdepartment'),
                                request.GET.get('current_date'), request.GET.get('range'))
            return HttpResponse(json.dumps(data))


@csrf_exempt
def workers_subdepartment(request, subdepartment_id):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            workers = Profile.objects.filter(department=subdepartment_id)
            data = serializers.serialize('json', workers, fields=('first_name', 'last_name', 'middle_name'))
            return HttpResponse(data)


@csrf_exempt
def workers_for_reports(request, department_id):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            date = request.GET.get('date')
            data = build_level_with_user(department_id, 0, date, 1)
            output = get_endpoint_department(data, [])
            return HttpResponse(json.dumps(output, ensure_ascii=False).encode('utf8'))


@csrf_exempt
def all_reports_for_person(request, person_id):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            data = get_reports_for_worker(request.GET.get('date'), person_id)
            return HttpResponse(json.dumps(data))
        elif request.method == "POST":
            date = request.POST.get('date')
            action = request.POST.get('action')
            month, year = date.split('-')
            profile = Profile.objects.get(pk=person_id)
            reports = Report.objects.filter(creator_id=profile, date__month=month, date__year=year)
            for report in reports:
                if action == 'ban':
                    report.status = True
                    report.ban_id = user.profile
                if action == 'unlock':
                    report.status = False
                    report.ban_id = None
                if action == 'check':
                    report.check = True
                    report.check_id = user.profile
                if action == 'uncheck':
                    report.check = False
                    report.check_id = None
                report.save()
            data = get_reports_for_worker(request.GET.get('date'), person_id)
            return HttpResponse(json.dumps(data))


@csrf_exempt
def all_projects_simple_view(request):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            projects = Project.objects.all()
            data = []
            for project in projects:
                data.append({'pk': project.pk, 'name': project.name})
            return HttpResponse(json.dumps(data))


@csrf_exempt
def get_department_view(request):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            department = user.profile.department
            department = get_department(department)
            data = {'pk': department.pk, 'name': department.department_name, 'code': department.department_code}
            return HttpResponse(json.dumps(data, ensure_ascii=False).encode('utf8'))


@csrf_exempt
def action_with_group_view(request):
    user = get_user_jwt(request)
    if user:
        if request.method == "GET":
            action_groups = GroupAction.objects.all()
            data = []
            for action_group in action_groups:
                fields = []
                actions = action_group.available_actions.all()
                for action in actions:
                    fields.append({'action': action.action, 'code': action.num, 'pk': action.pk})
                data.append({'pk': action_group.pk, 'group_name': action_group.name, 'actions': fields})
            return HttpResponse(json.dumps(data, ensure_ascii=False).encode('utf8'))
