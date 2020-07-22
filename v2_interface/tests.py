from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse,resolve,reverse_lazy
from django.contrib.auth import get_user_model
from . import views
from .models import PickUpV2,NotesV2,WasteBinTypeV2
from users.models import AccountType
from .forms import PickUpForm
# Create your tests here.
import datetime


User = get_user_model()
class PickUpV2Tests(TestCase):

    def test_pick_up_create(self):
    
        self.type = AccountType.objects.create(value="testing")

        user = User.objects.create_user(
            username="bob",
            email="test@gmail.com",
            phone_number = "+9999999999",
            account_type=self.type,
            street="test",
            apt="test",
            state="NY",
            zipcode="12352",
        )
        today = datetime.date.today()
        time_now= datetime.time()

        bin_type = WasteBinTypeV2.objects.create(name="test")
        pick_up = PickUpV2.objects.create(
            bin_type=bin_type,
            weight=150,
            scheduled_user = user,
            scheduled_date = today,
        )

        self.assertEqual(pick_up.scheduled_user,user)
        self.assertEqual(pick_up.bin_type,bin_type)
        self.assertEqual(pick_up.weight,150)
        self.assertEqual(pick_up.scheduled_date,today)

class HomeViewTest(TestCase):

    def setUp(self):
        self.type = AccountType.objects.create(value="testing")

        self.user = User.objects.create_user(
            username="bob",
            email="test@gmail.com",
            phone_number = "+9999999999",
            account_type=self.type,
            street="test",
            apt="test",
            state="NY",
            zipcode="12352",
            password="123"
        )
        self.client.login(username="bob",password="123")
        url = reverse_lazy('v2_interface:home')
        self.response = self.client.get(url)

    def test_login(self):
        self.assertEqual(self.response.status_code,200)
        self.assertTemplateUsed(self.response,'_base.html')    
        self.assertContains(self.response,'Department of Sanitation')    
        
class CalendarViewTest(TestCase):
    def setUp(self):
        self.type = AccountType.objects.create(value="testing")

        self.user = User.objects.create_user(
            username="bob",
            email="test@gmail.com",
            phone_number = "+9999999999",
            account_type=self.type,
            street="test",
            apt="test",
            state="NY",
            zipcode="12352",
            password="123"
        )
        self.client.login(username="bob",password="123")
        url = reverse_lazy('v2_interface:schedule-list')
        self.response = self.client.get(url)

    def test_calendar_view_status_code(self):
        self.assertEqual(self.response.status_code,200)

    def test_calendar_template_used(self):
        self.assertTemplateUsed(self.response,'v2_interface/calendar.html')
    
    def test_calendar_contains(self):
        self.assertContains(self.response,"1")

    def test_view_function_name(self):
        view = resolve('/v2/home/schedule/list/')
        self.assertEqual(view.func.__name__,views.CalendarView.as_view().__name__)

class PickUpDetailViewTest(TestCase):
    def setUp(self):
        self.type = AccountType.objects.create(value="testing")

        self.user = User.objects.create_user(
            username="bob",
            email="test@gmail.com",
            phone_number = "+9999999999",
            account_type=self.type,
            street="test",
            apt="test",
            state="NY",
            zipcode="12352",
            password="123"
        )

        today = datetime.date.today()
        time_now= datetime.time()

        bin_type = WasteBinTypeV2.objects.create(name="test")
        self.pick_up = PickUpV2.objects.create(
            bin_type=bin_type,
            weight=150,
            scheduled_user = self.user,
            scheduled_date = today,
        )

        self.client.login(username="bob",password="123")
        url = reverse_lazy('v2_interface:pickup-detail',kwargs={'pk':self.pick_up.id})
        self.response = self.client.get(url)

    def test_pickup_detail_status_code(self):
        self.assertEqual(self.response.status_code,200)
        
    def test_pickup_template_used(self):
        self.assertTemplateUsed(self.response,'v2_interface/pickup_detail.html')
    
    def test_pickup_detail_contains(self):
        self.assertContains(self.response,"test")
    
    def test_pickup_detail_view(self):
        view = resolve('/v2/home/schedule/list/pickup/1/')
        self.assertEqual(view.func.__name__, views.PickUpDetailView.as_view().__name__)

    def test_pickup_detail_failed_query(self):
        url = reverse_lazy('v2_interface:pickup-detail',kwargs={'pk':self.pick_up.id + 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

class PickUpCreateView(TestCase):
    def setUp(self):
        self.type = AccountType.objects.create(value="testing")

        self.user = User.objects.create_user(
            username="bob",
            email="test@gmail.com",
            phone_number = "+9999999999",
            account_type=self.type,
            street="test",
            apt="test",
            state="NY",
            zipcode="12352",
            password="123"
        )

        self.client.login(username="bob",password="123")
        url = reverse_lazy('v2_interface:create-pickup')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code,200)

    def test_pickup_create_template_used(self):
        self.assertTemplateUsed(self.response,'v2_interface/pickup_form.html')
    
    def test_pickup_create_name(self):
        view = resolve('/v2/home/schedule/list/pickup/create/')
        self.assertEqual(view.func.__name__,views.PickUpCreateView.as_view().__name__)
    
    def test_pickup_form_used(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form,PickUpForm)
        self.assertContains(self.response,'csrfmiddlewaretoken')

