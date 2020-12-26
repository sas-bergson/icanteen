import unittest
from django.core.urlresolvers import reverse
from django.test import Client
from .models import Product, Category
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType

# Create your tests here.

def create_django_contrib_auth_models_user(**kwargs):
    defaults = {}
    defaults["username"] = "username"
    defaults["email"] = "username@tempurl.com"
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_django_contrib_auth_models_group(**kwargs):
    defaults = {}
    defaults["name"] = "group"
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_django_contrib_contenttypes_models_contenttype(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_product(**kwargs):
    defaults = {}
    defaults["designation"] = "designation"
    defaults["slug"] = "slug"
    defaults["description"] = "description"
    defaults["packaging"] = "packaging"
    defaults["price"] = "price"
    defaults["views"] = "views"
    defaults["image"] = "image"
    defaults.update(**kwargs)
    if "category" not in defaults:
        defaults["category"] = create_category()
    return Product.objects.create(**defaults)


def create_category(**kwargs):
    defaults = {}
    defaults["name"] = "name"
    defaults["slug"] = "slug"
    defaults["image"] = "image"
    defaults["views"] = "views"
    defaults.update(**kwargs)
    return Category.objects.create(**defaults)


class ProductViewTest(unittest.TestCase):
    '''
    Tests for Product
    '''
    def setUp(self):
        self.client = Client()

    def test_list_product(self):
        url = reverse('gallery_product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_product(self):
        url = reverse('gallery_product_create')
        data = {
            "designation": "designation",
            "slug": "slug",
            "description": "description",
            "packaging": "packaging",
            "price": "price",
            "views": "views",
            "image": "image",
            "category": create_category().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_product(self):
        product = create_product()
        url = reverse('gallery_product_detail', args=[product.slug,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_product(self):
        product = create_product()
        data = {
            "designation": "designation",
            "slug": "slug",
            "description": "description",
            "packaging": "packaging",
            "price": "price",
            "views": "views",
            "image": "image",
            "category": create_category().pk,
        }
        url = reverse('gallery_product_update', args=[product.slug,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class CategoryViewTest(unittest.TestCase):
    '''
    Tests for Category
    '''
    def setUp(self):
        self.client = Client()

    def test_list_category(self):
        url = reverse('gallery_category_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_category(self):
        url = reverse('gallery_category_create')
        data = {
            "name": "name",
            "slug": "slug",
            "image": "image",
            "views": "views",
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_category(self):
        category = create_category()
        url = reverse('gallery_category_detail', args=[category.slug,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_category(self):
        category = create_category()
        data = {
            "name": "name",
            "slug": "slug",
            "image": "image",
            "views": "views",
        }
        url = reverse('gallery_category_update', args=[category.slug,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

