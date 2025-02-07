from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.
class City(models.Model):
    city = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.city

class Status(models.Model):
    status = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.status

class ID_Card(models.Model):
    card = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.card

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    image = models.FileField(null=True)

    def __str__(self):
        return self.user.first_name


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.IntegerField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_addressed = models.BooleanField(default=False)

    def __str__(self):
        return f"Feedback from {self.name}"
    

class ServiceManSlot(models.Model):
    service_man = models.ForeignKey('Service_Man', on_delete=models.CASCADE, related_name='slots')
    date = models.DateField()
    available_slots = models.IntegerField(default=5)
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('service_man', 'date')

    def __str__(self):
        return f"{self.service_man.user.first_name} - {self.date} - {self.available_slots} slots"

class Service_Man(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    doj = models.DateField(null=True)
    dob = models.DateField(null=True)
    id_type = models.CharField(max_length=100, null=True)
    service_name = models.CharField(max_length=100, null=True)
    experience = models.CharField(max_length=100, null=True)
    id_card = models.FileField(upload_to='id_cards/', null=True)
    image = models.FileField(upload_to='service_man_images/', null=True)

    def __str__(self):
        return self.user.first_name if self.user else "Unnamed Service Man"

    def get_available_slots(self, date):
        slot, created = ServiceManSlot.objects.get_or_create(
            service_man=self,
            date=date,
            defaults={'available_slots': 5, 'is_booked': False}
        )
        return 0 if slot.is_booked else slot.available_slots

    def book_slot(self, date):
        slot, created = ServiceManSlot.objects.get_or_create(
            service_man=self,
            date=date,
            defaults={'available_slots': 5, 'is_booked': False}
        )
        if not slot.is_booked:
            slot.is_booked = True
            slot.available_slots = 0
            slot.save()
            return True
        return False

    def reset_past_slots(self):
        today = timezone.now().date()
        ServiceManSlot.objects.filter(service_man=self, date__lt=today).delete()

    def is_available(self, date):
        slot = ServiceManSlot.objects.filter(service_man=self, date=date).first()
        return not slot or not slot.is_booked

    def get_total_available_slots(self):
        today = timezone.now().date()
        return ServiceManSlot.objects.filter(
            service_man=self, 
            date__gte=today, 
            is_booked=False
        ).count()


class Service_Category(models.Model):
    category = models.CharField(max_length=30, null=True)
    desc = models.CharField(max_length=100, null=True)
    image = models.FileField(null=True)
    total=models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.category

class Service(models.Model):
    category = models.ForeignKey(Service_Category,on_delete=models.CASCADE,null=True)
    service = models.ForeignKey(Service_Man, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.service.user.first_name

class Contact(models.Model):
    status = models.ForeignKey(Status,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100, null=True)
    message1 = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    def __str__(self):
        return self.name

class Total_Man(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.service.user.first_name

class Order(models.Model):
    report_status = models.CharField(max_length=100, null=True)
    status = models.ForeignKey(Status,on_delete=models.CASCADE,null=True)
    service = models.ForeignKey(Service_Man, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    book_date = models.DateField(null=True)
    book_days = models.CharField(max_length=100, null=True)
    book_hours = models.CharField(max_length=100, null=True)
    refunded = models.BooleanField(default=False)
    def __str__(self):
        return self.service.user.first_name+" "+self.customer.user.first_name
