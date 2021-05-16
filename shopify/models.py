'''from django.db import models
from authy.models import NewUser, Address
from seller.models import Seller

# Create your models here.

STATUS = (
    ('1', 'Order Placed'),
    ('2', 'Packed'),
    ('3', 'Shipped'),
    ('4', 'Out for delivery'),
    ('5', 'Delivered')
)
GENDER = (
    ('1', 'Male'),
    ('2', 'Female')
)


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    gender = models.CharField(max_length=50, choices=GENDER, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    category = models.ForeignKey(Category, related_name='Product', on_delete=models.CASCADE)
    desc = models.TextField()
    mrp = models.FloatField()
    price = models.FloatField()
    image = models.TextField()
    slug = models.SlugField(max_length=200, db_index=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # seller=models.ForeignKey(Seller, related_name='seller',on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='cart')
    complete = models.BooleanField(default=False)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cartitem', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_item")
    quantity = models.IntegerField(default=0)
    amt = models.FloatField(default=0)


class Order(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='order')
    address = models.ForeignKey(Address, related_name='delivery_address', on_delete=models.CASCADE)

    date = models.DateTimeField(auto_now_add=True)
    amt = models.FloatField(default=0.0)
    status = models.CharField(max_length=100, choices=STATUS)
    active = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)


class Order_Product(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_id")
    qty = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_item")
    amt = models.FloatField()


class Payment(models.Model):
    order = models.ForeignKey(Order, related_name='payment_method', on_delete=models.CASCADE)

    payment_id = models.CharField(max_length=100)
    successful = models.BooleanField(default=False)


class Size(models.Model):
    item = models.ForeignKey(Product, related_name='clothes_size', on_delete=models.CASCADE)
    xxs = models.BooleanField(default=False)
    xs = models.BooleanField(default=False)
    s = models.BooleanField(default=False)
    m = models.BooleanField(default=False)
    l = models.BooleanField(default=False)
    xl = models.BooleanField(default=False)
    xxl = models.BooleanField(default=False)


class Review(models.Model):
    item = models.ForeignKey(Product, related_name='review', on_delete=models.CASCADE)
    rate = models.IntegerField()
    comment = models.TextField()
    image = models.TextField(blank=True)


class Wishlist(models.Model):
    user = models.ForeignKey(NewUser, related_name="wishlist_user", on_delete=models.CASCADE)
    item = models.ForeignKey(Product, related_name="wishlist_item", on_delete=models.CASCADE)


class Prod_Media(models.Model):
    media_link = models.TextField()
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image set')
'''