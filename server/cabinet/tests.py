from .models import Report
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Profile, Report, Action, Group, GroupAction, Project, Direction, Department, SalaryIndividual, \
    SalaryCommon, CalendarMark
from datetime import datetime, date
from json import loads


class AllModelTests(TestCase):

    def setUp(self) -> None:
        user = User.objects.create_user(password='admin', username='admin')
        self.client = Client()
        user_1 = User.objects.create_user(password='admin_1', username='admin_1')
        departament = Department.objects.create(department_code='1', department_name='First', subdepartment_code='0')
        profile = Profile.objects.create(user=user, first_name='Vanya', last_name='Ivanov', middle_name='Ivanovich')
        profile_2 = Profile.objects.create(user=user_1, first_name='Inna', last_name='Ivanova',
                               middle_name='Ivanovich', department=departament)
        common_part = SalaryCommon.objects.create(date=datetime.now())
        SalaryIndividual.objects.create(common_part=common_part, person=profile_2, date=datetime.now(), plan_salary=10000)
        SalaryIndividual.objects.create(common_part=common_part, person=profile, date=datetime.now(), plan_salary=10000)
        profiles = Profile.objects.all()
        Report.objects.create(creator_id=profile, text='Ivanovich Ivanovich Ivanovich Ivanovich Ivanovich',
                              hour=5, status=True, ban_id=profile, check=True, check_id=profile, date = datetime.now())
        Action.objects.create(action='Eat', num='10')
        direction = Direction.objects.create(name="Direction", code="228")
        Project.objects.create(name="Of", direction=direction, manager=profile, client="Ya", chief_designer=profile,
                               deputy_chief_designer=profile, contract="2228")
        Action.objects.create(action='Drink', num='11')
        Action.objects.create(action='Cry', num='12')
        Action.objects.create(action='Sleep', num='13')
        actions = Action.objects.all()
        group_action = GroupAction.objects.create(name='Common_things')
        group_action.available_actions.set(actions)
        group = Group.objects.create(name='Commoners')
        group.actions.set(actions)
        group.participants.set(profiles)
        CalendarMark.objects.create(person=profile, type="undefined", end_date=date(year=2020, month=9, day=1),
                                    start_date=datetime.now())
        CalendarMark.objects.create(person=profile, type="undefined", end_date=date(year=2020, month=10, day=11),
                                    start_date=date(year=2020, month=10, day=1))
        Department.objects.create(department_code='2', department_name='Second', subdepartment_code='1')
        Department.objects.create(department_code='3', department_name='Third', subdepartment_code='1')
        Department.objects.create(department_code='4', department_name='Fourth', subdepartment_code='2')



    def test_profile_and_report(self):
        user = User.objects.get(username='admin')
        profile = Profile.objects.get(user=user)
        report = Report.objects.get(creator_id=profile)
        self.assertEqual(profile.middle_name, 'Ivanovich')
        self.assertEqual(profile.first_name, 'Vanya')
        self.assertEqual(report.creator_id, profile)
        self.assertEqual(report.status, True)
        self.assertEqual(report.ban_id, profile)
        self.assertEqual(report.check, True)
        self.assertEqual(report.check_id, profile)

    # def test_actions_and_groups(self):
    #     group_actions = GroupAction.objects.all()
    #     for group_action in group_actions:
    #         for action in group_action.available_actions.all():
    #             print(action.action)
    #             print(action.num)

    def test_authenticate(self):
        response = self.client.post('/token/', data={
            'username': 'admin',
            'password': 'admin',
            'IP': '102.42.23.56'
        })
        token = response.content.decode('utf8')
        token = loads(token)
        self.token = token['access']

    def test_cabinet_info(self):
        request = self.client.get('/cabinet/')
        self.assertEqual(request.status_code, 200)
        self.assertEqual({'pk': 3, 'fine_late': '09:15:00',
                          'oklad': False, 'last_name': 'Ivanov',
                          'first_name': 'Vanya', 'middle_name': 'Ivanovich',
                          'employment_date': '2010-01-01', 'SRI_SAS': False, 'sex': '',
                          'birth_date': 'None', 'experience': 0.0, 'position': '', 'department': ''},
                         loads(request.content.decode("utf8")))

    def test_reports_info(self):
        request = self.client.get('/cabinet/reports/')
        self.assertEqual(request.status_code, 200)
        self.assertEqual({'time_system': 0, 'reports': [], 'status': False, 'time_report': 0, 'time_norm': ''},
               loads(request.content.decode("utf8")))

    def test_projects_info(self):
        request = self.client.get('/cabinet/projects/')
        self.assertEqual(request.status_code, 200)
        pk = loads(request.content.decode("utf8"))[0]['pk']
        self.assertEqual([{'pk': pk, 'fields': {'name': 'Of', 'direction': 'Direction',
                                               'manager': 'Ivanov Vanya Ivanovich',
                                               'deputy_chief_designer': 'Ivanov Vanya Ivanovich',
                                               'chief_designer': 'Ivanov Vanya Ivanovich',
                                               'production_order': '', 'comment_for_employees': '', 'contract': '2228',
                                               'type': False, 'status': False, 'client': 'Ya',
                                               'report_availability': False, 'acceptance_vp': False}}],
                         loads(request.content.decode("utf8")))

    def test_groups_info(self):
        request = self.client.get('/admin/groups_admin/')
        self.assertEqual(request.status_code, 200)
        pk = loads(request.content.decode("utf8"))[0]['pk']
        self.assertEqual([{'pk': pk, 'fields': {'name': 'Commoners', 'users': ['Vanya Ivanov Ivanovich', 'Inna Ivanova Ivanovich'],
                              'description': '', 'actions': ['Eat 10', 'Drink 11', 'Cry 12', 'Sleep 13']}}],
                        loads(request.content.decode("utf8")))

    def test_logs(self):
        request = self.client.get('/admin/logs/')
        self.assertEqual(request.status_code, 200)
        self.assertEqual([], loads(request.content.decode("utf8")))

    def test_departments(self):
        request = self.client.get('/departments/')
        self.assertEqual(request.status_code, 200)
        # first_pk = loads(request.content.decode("utf8"))[0]['pk']
        # second_pk = loads(request.content.decode("utf8"))[0]['subdepartments'][0]['pk']
        # third_pk = loads(request.content.decode("utf8"))[0]['subdepartments'][1]['pk']
        # fourth_pk = loads(request.content.decode("utf8"))[0]['subdepartments'][0]['subdepartments'][0]['pk']
        # self.assertEqual([{"name": "First", "code": "1", "pk": first_pk, "users": [{'name': 'Inna Ivanova Ivanovich',
        #     'SRI_SAS': False, 'pk': 6, 'has_report': False, 'banned': '',
        #     'checker': '', 'time_report': 0, 'time_system': 0, 'time_norm': 0}], "subdepartments": [
        #     {"name": "Second", "code": "2", "pk": second_pk, "users": [],
        #      "subdepartments": [{"name": "Fourth", "code": "4", "pk": fourth_pk, "users": []}]},
        #     {"name": "Third", "code": "3", "pk": third_pk, "users": []}]}], loads(request.content.decode("utf8")))

    def test_salary(self):
        request = self.client.get('/departments/')
        self.assertEqual(request.status_code, 200)
        first_pk = loads(request.content.decode("utf8"))[0]['pk']
        date = f'{datetime.now().month}-{datetime.now().year}'
        request_2 = self.client.get(f'/salary/new/{first_pk}/?date={date}')
        self.assertEqual(request_2.status_code, 200)
        print(request_2.content)
        # self.assertEqual([{"pk": 33, "code": "1", "name": "First", "users": [
        #     {"name": "Inna Ivanova Ivanovich", "SRI_SAS": False, "pk": 18, "position": "", "work_days": 0.0,
        #      "hours_worked": 0.0, "time_norm_individual": 0.0, "penalty": 0.0, "is_penalty": False, "time_off": 0.0,
        #      "plan_salary": 10000.0, "award": 0.0, "salary_hand": 0.0, "days_norm": 0.0, "time_norm": 0.0}]},
        #  {"pk": 34, "code": "2", "name": "Second", "users": []}, {"name": "Fourth", "code": "4", "pk": 36, "users": []},
        #  {"name": "Third", "code": "3", "pk": 35, "users": []}], loads(request_2.content.decode("utf8")))

    def test_calendar(self):
        request = self.client.get('/departments/')
        self.assertEqual(request.status_code, 200)
        first_pk = loads(request.content.decode("utf8"))[0]['pk']
        request = self.client.get(f'/cabinet/calendar/?range=year&&current_date=10-2020&&subdepartment={first_pk}')
        self.assertEqual(request.status_code, 200)