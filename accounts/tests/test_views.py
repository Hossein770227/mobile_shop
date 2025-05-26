from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from accounts.forms import UserRegisterForm, VerifyCodeForm
from accounts.models import MyUser


class UserRegisterViewTest(TestCase):

    def setUp(self):
        self.client =Client()
     
    def test_user_register_GET(self):
        response = self.client.get(reverse('accounts:user_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/user_register.html')
        self.assertTrue(response.context['form'], UserRegisterForm)
    
    def test_user_register_POST_valid(self):
        response = self.client.post(reverse("accounts:user_register"), data={'phone':'09211234567','full_name': 'hossein hadi amani', 'password1':'password', 'password2':'password' })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:verify_code'))

    def test_user_register_POST_invalid(self):
        response = self.client.post(reverse('accounts:user_register'),data={'phone':'14528','full_name': 'hossein hadi amani', 'password1':'password', 'password2':'password' })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(form=response.context['form'], field='phone', errors='Enter a valid Iranian cellphone number.')

class USerRegisterCodeViewTest(TestCase):
    def setUp(self):
        self.client= Client()

    def test_User_register_code_GET(self):
        response = self.client.get(reverse('accounts:verify_code'))
        self.assertEqual(response.status_code,200 )
        self.assertTemplateUsed(response, "accounts/verify_code.html")
        self.assertTrue(response.context['form'], VerifyCodeForm)