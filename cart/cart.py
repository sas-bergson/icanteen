from decimal import Decimal
from django.conf import settings
from gallery.models import Product

class Cart(object):
      def __init__(self, request): # here a cart object is initialized with the request object
          self.session = request.session # inorder to store the session
          cart = self.session.get(settings.CART_SESSION_ID) # here i try to get the cart from the available session
          if not cart:   # if no cart is available when you enter the gallery a new cart is initilized
              cart = self.session[settings.CART_SESSION_ID] = {}
          self.cart = cart


      def add(self, product, quantity=1, update_quantity=False):
         product_id = str(product.id)  #json is used to store session data and json accepts on string reason why product_id is converted to string
         if product_id not in self.cart:
             self.cart[product_id] = {'quantity' : 0, 'price' : str(product.price)}
         if update_quantity:
             self.cart[product_id]['quantity'] = quantity
         else:
             self.cart[product_id]['quantity'] += quantity
         self.save()


      def save(self): # this method tracks changes in the cart and marks sessions as modidied using what is written on line 27
         #self.session[settings.CART_SESSION_ID] = self.cart
         self.session.modified = True

      def remove(self, product):
         product_id = str(product.id)
         if product_id in self.cart:
             del self.cart[product_id]
             self.save()

      def __iter__(self):   #a method to iterate through items in the cart and get related product instances
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

      def __len__(self):
          return sum(item['quantity'] for item in self.cart.values())

      def get_total_price(self):
          return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

      def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
        #self.session.modified = True

