from django.test import TestCase, RequestFactory, Client
#from gallery.models import Product
from django.contrib.auth.models import User, AnonymousUser
import datetime
from decimal import Decimal
from .cart import Cart


class CartAndProductTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.request = RequestFactory()
        self.request.user = AnonymousUser()
        self.request.session = {}

    def _create_cart_in_database(self, creation_date=datetime.datetime.now(),
            checked_out=False):
        cart = Cart
        product = Product
        product.created = creation_date
        cart.checked_out = False
        cart.save()
        return cart

    def _create_item_in_database(self, cart, product, quantity=1,
            unit_price=Decimal("100")):
        product = Product
        cart = Cart
        product.quantity = quantity
        product.unit_price = unit_price
        cart.save()

        return product

    def _create_user_in_database(self):
        user = User(username="user", password="user",
                email="example@example.com")
        user.save()
        return user

    def test_cart_creation(self):
        creation_date = datetime.datetime.now()
        cart = self._create_cart_in_database(creation_date)
        id = cart.id

        #cart_from_database =
        #self.assertEquals(cart, cart_from_database)

    def test_total_item_price(self):

        user = self._create_user_in_database()
        cart = self._create_cart_in_database()

        item_with_unit_price_as_integer = self._create_item_in_database(cart, product=user, quantity=3, unit_price=100)

        self.assertEquals(item_with_unit_price_as_integer.total_price, 300)



