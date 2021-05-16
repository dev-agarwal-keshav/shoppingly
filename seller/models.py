from django.db import models
from authy.models import NewUser
# Create your models here.

class Seller(models.Model):
    user=models.ForeignKey(NewUser,related_name='seller',on_delete=models.CASCADE)

    business_name=models.CharField(max_length=50)
    
    gst=models.CharField(max_length=100)
    pan=models.CharField(max_length=20)
    
    pickup_address=models.TextField()
    state=models.CharField(max_length=50)
    pin=models.CharField(max_length=6)

    bank_account_no=models.CharField(max_length=20)
    ifsc_code= models.CharField(max_length=20)