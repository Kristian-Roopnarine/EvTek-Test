from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import CustomUser,Address,AccountType
from .forms import CustomUserCreationForm,AddressForm
# Create your tests here.

class CustomUserTests(TestCase):

    def test_create_user(self):

        User = get_user_model()
        self.type = AccountType.objects.create(value="testing")
        user = User.objects.create_user(
            username="bob",
            email="test@gmail.com",
            phone_number = "+9999999999",
            account_type=self.type
        )

        self.assertEqual(user.email,"test@gmail.com")
        self.assertEqual(user.username,"bob")
        self.assertEqual(user.phone_number,"+9999999999")
        self.assertEqual(user.account_type.value,"testing")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

class AddressTests(TestCase):

    def test_create_address(self):
        User = get_user_model()

        self.type = AccountType.objects.create(value="testing")

        user = User.objects.create_user(
            username="bob",
            email="test@gmail.com",
            phone_number = "+9999999999",
            account_type=self.type
        )

        user_address = Address.objects.create(
            street="test",
            apt="test",
            state="NY",
            zipcode="12352",
            user=user
        )

        self.assertEqual(user_address.user, user)
        self.assertEqual(user_address.user.username,user.username)
        self.assertEqual(user_address.street,"test")
        self.assertEqual(user_address.apt,"test")
        self.assertEqual(user_address.state,"NY")
        self.assertEqual(user_address.zipcode,"12352")



