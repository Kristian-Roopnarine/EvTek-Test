from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import CustomUser,AccountType
from .forms import CustomUserCreationForm
# Create your tests here.

class CustomUserTests(TestCase):

    def test_create_user(self):

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

        self.assertEqual(user.email,"test@gmail.com")
        self.assertEqual(user.username,"bob")
        self.assertEqual(user.phone_number,"+9999999999")
        self.assertEqual(user.account_type.value,"testing")
        self.assertEqual(user.street,"test")
        self.assertEqual(user.apt,"test")
        self.assertEqual(user.state,"NY")
        self.assertEqual(user.zipcode,"12352")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


        



