import datetime
import uuid
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from django.forms import ModelForm, TextInput, Textarea
from django.utils import timezone


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Name", max_length=255)
    subject = models.CharField("Subject", max_length=255, null=True)
    email = models.CharField("email", max_length=255, null=True)
    body = models.TextField("Body", max_length=255, null=True)
    create_date = models.DateTimeField("Create Date", default=timezone.now)
    deleted = models.BooleanField("Deleted", default=False)

    def __str__(self):
        return "{}".format(self.subject)

    class Meta:
        db_table = 'message'
        ordering = ('-id',)


class Contact(models.Model):
    id = models.BigAutoField(primary_key=True)
    linkedin = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    whastapp = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    gmail = models.URLField(null=True, blank=True)
    yahoo = models.URLField(null=True, blank=True)
    telegram = models.URLField(null=True, blank=True)
    skype = models.URLField(null=True, blank=True)

    def __str__(self):
        return '{0}'.format(self.linkedin)


class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    name = models.CharField(blank=True, max_length=20)
    email = models.CharField(blank=True, max_length=50)
    subject = models.CharField(blank=True, max_length=50)
    message = models.TextField(blank=True, max_length=255)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': TextInput(attrs={'class': 'input', 'placeholder': 'Name & Surname'}),
            'subject': TextInput(attrs={'class': 'input', 'placeholder': 'Subject'}),
            'email': TextInput(attrs={'class': 'input', 'placeholder': 'Email Address'}),
            'message': Textarea(attrs={'class': 'input', 'placeholder': 'Your Message', 'rows': '5'}),
        }


class Slide(models.Model):
    caption1 = models.CharField(max_length=100)
    caption2 = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    image = models.ImageField(help_text="Size: 1920x570")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.caption1, self.caption2)


class Service(models.Model):
    titles = models.CharField(max_length=70)
    images = ProcessedImageField(upload_to='albums', processors=[ResizeToFit(700)], format='JPEG',
                                 options={'quality': 1000})
    description = models.TextField(max_length=500, null=True)
    is_visibles = models.BooleanField(default=True)

    def __str__(self):
        return self.titles


class Actualites(models.Model):
    titles = models.CharField(max_length=70)
    actu_type = models.CharField(max_length=10)
    images = ProcessedImageField(upload_to='albums', processors=[ResizeToFit(700)], format='JPEG',
                                 options={'quality': 1000})
    description = models.TextField(max_length=500, null=True)
    pub_dates = models.DateTimeField(verbose_name=" date", default=datetime.datetime.today)
    slugs = models.SlugField(max_length=70, default=uuid.uuid4, editable=False)
    is_visibles = models.BooleanField(default=True)

    def __str__(self):
        return self.titles


class Image(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    picture = ProcessedImageField(upload_to='albums', processors=[ResizeToFit(700)], format='JPEG',
                                  options={'quality': 1000})

    def __str__(self):
        return '{0}'.format(self.name)


class Pro(models.Model):
    name = models.CharField(max_length=150, null=True)
    description = models.TextField(max_length=500, null=True)
    tools = models.CharField(max_length=100)

    picture = ProcessedImageField(upload_to='albums', processors=[ResizeToFit(700)], format='JPEG',
                                  options={'quality': 1000})
    # source_code = models.URLField(null=True, blank=True)
    # live_url = models.URLField(null=True, blank=True)
    # when = models.DateField()

    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Aboutus(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    lien = models.URLField(null=True, blank=True)
    file = models.FileField(null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0}'.format(self.title)


class Gallery(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    image = models.ManyToManyField(Image)

    dateCreated = models.DateTimeField(auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0}'.format(self.name)


class Homeimg(models.Model):
    id = models.BigAutoField(primary_key=True)
    picture = ProcessedImageField(upload_to='albums', processors=[ResizeToFit(700)], format='JPEG',
                                  options={'quality': 1000})

    def __str__(self):
        return '{0}'.format(self.picture)


LABEL_CHOICES = (
    ('S', 'sale'),
    ('N', 'new'),
    ('P', 'promotion')
)


class Category(models.Model):
    title = models.CharField(max_length=100)
    # parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()
    is_active = models.BooleanField(default=True)

    # class MPTTMeta:
    #     order_insertion_by = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("category", kwargs={
            'slug': self.slug
        })


class Item(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    # stock = models.CharField(max_length=10)
    description_short = models.CharField(max_length=50)
    description_long = models.TextField()
    image = models.ImageField()
    file = models.FileField(null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'item'
        ordering = ('-id',)


class Criteria(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("criteria", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    ref_code = models.CharField(max_length=20)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a BillingAddress
    (Failed Checkout)
    3. Payment
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.ref_code

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class CartItems(models.Model):
    ORDER_STATUS = (
        ('Active', 'Active'),
        ('Delivered', 'Delivered')
    )
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    ordered_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Active')
    delivery_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.item.title

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'pk': self.pk
        })

    def update_status_url(self):
        return reverse("update_status", kwargs={
            'pk': self.pk
        })
