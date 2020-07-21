from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse,resolve,reverse_lazy
from django.contrib.auth import get_user_model
from . import views
from .models import PickUp,Notes,WasteBinType
from users.models import AccountType
# Create your tests here.
import datetime

class PickUpTests(TestCase):

    def test_pick_up_create(self):
        User = get_user_model()

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

        bin_type = WasteBinType.objects.create(name="test")
        pick_up = PickUp.objects.create(
            bin_type=bin_type,
            weight=150,
            scheduled_user = user,
            scheduled_date = today,
        )

        self.assertEqual(pick_up.scheduled_user,user)
        self.assertEqual(pick_up.bin_type,bin_type)
        self.assertEqual(pick_up.weight,150)
        self.assertEqual(pick_up.scheduled_date,today)

"""  
This test doesn't work because it gets redirected because there is no logged in user
class HomeViewTest(SimpleTestCase):

    def setUp(self):
        url = reverse_lazy('waste_bins:home')
        self.response=self.client.get(url)
        
    def test_home_template(self):
        self.assertEqual(self.response.status_code,302)
        self.assertTemplateUsed(self.response,'_base.html')
        self.assertContains(self.response,'DoS')
"""


    
    