from django.db import models


class getinvoicelist(models.Model):
    inv_no = models.IntegerField()
    inv_date = models.DateField()
    buy_name = models.CharField(max_length=50)
    inv_net_amt = models.CharField(max_length=50)


class Product(models.Model):
    name = models.CharField(max_length=50)
    mfg = models.CharField(max_length=50)
    diameter  = models.CharField(max_length=50)
    grade = models.CharField(max_length=50)
    qty = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    rate = models.CharField(max_length=50)
    taxable_amount=models.CharField(max_length=50)
    cgst = models.CharField(max_length=50)
    sgst = models.CharField(max_length=50)
    igst = models.CharField(max_length=50)
    total_amount = models.CharField(max_length=50)
    class Meta:
        db_table = 'invoice_product'
        managed = True
       
    