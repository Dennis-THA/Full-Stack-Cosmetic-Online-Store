from django.test import TestCase
from django.urls import reverse
from .models import Member, Item
from .forms import Memberform, LoginForm

class MemberModelTest(TestCase):

    def setUp(self):
        Member.objects.create(
            fname="John",
            lname="Doe",
            email="john.doe@example.com",
            password="password123",
            age=30,
            phone="1234567890"
        )

    def test_member_str(self):
        member = Member.objects.get(email="john.doe@example.com")
        self.assertEqual(str(member), "John Doe")

class ItemModelTest(TestCase):

    def setUp(self):
        Item.objects.create(
            title="Test Item",
            price=100.00,
            old_price=120.00,
            discount_label="20% OFF",
            image="path/to/image.jpg",
            image_hover="path/to/image_hover.jpg"
        )

    def test_item_str(self):
        item = Item.objects.get(title="Test Item")
        self.assertEqual(str(item), "Test Item")

class SignupViewTest(TestCase):

    def test_signup_view_get(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_view_post(self):
        data = {
            'fname': 'John',
            'lname': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'age': 30,
            'phone': '1234567890'
        }
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 200)  # Check if it redirects to success page
        self.assertTemplateUsed(response, 'success.html')
        self.assertTrue(Member.objects.filter(email='john.doe@example.com').exists())

class LoginViewTest(TestCase):

    def setUp(self):
        self.member = Member.objects.create(
            fname="John",
            lname="Doe",
            email="john.doe@example.com",
            password="password123",
            age=30,
            phone="1234567890"
        )

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post(self):
        data = {
            'email': 'john.doe@example.com',
            'password': 'password123'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)  # Check if it redirects to home
        self.assertRedirects(response, reverse('home'))

class HomeViewTest(TestCase):

    def setUp(self):
        Item.objects.create(
            title="Test Item 1",
            price=100.00,
            old_price=120.00,
            discount_label="20% OFF",
            image="path/to/image1.jpg",
            image_hover="path/to/image_hover1.jpg"
        )
        Item.objects.create(
            title="Test Item 2",
            price=150.00,
            old_price=170.00,
            discount_label="15% OFF",
            image="path/to/image2.jpg",
            image_hover="path/to/image_hover2.jpg"
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertEqual(len(response.context['items']), 2)

class MemberFormTest(TestCase):

    def test_member_form_valid(self):
        form = Memberform(data={
            'fname': 'John',
            'lname': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'age': 30,
            'phone': '1234567890'
        })
        self.assertTrue(form.is_valid())

    def test_member_form_invalid(self):
        form = Memberform(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)  # Ensure all fields are required

class LoginFormTest(TestCase):

    def test_login_form_valid(self):
        form = LoginForm(data={
            'email': 'john.doe@example.com',
            'password': 'password123'
        })
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)  # Ensure both fields are required

