from django.shortcuts import render
from .models import *
from django.db import connection
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def invoiceList(request):
    cursor=connection.cursor()
    # cursor.execute(call 'Getinvoicelist()')    
    cursor.execute('call Getinvoicelist()')    
    
    result = cursor.fetchall()     
    print("---------------",result)
    context= {'invoices':result}    
    return render(request,"invoice/invoicelist.html",context)


def invoiceCreate(request):
    cursor=connection.cursor()
    cursor.execute('call invoiceDetail()')
    result = cursor.fetchall()   
    sub_total=0
    net_amount=0
    cursor=connection.cursor()
    cursor.execute('call tc()')
    tc = cursor.fetchall()
    product = Product.objects.all()
    
    for i in product:
        sub_total+= float(i.total_amount)
        net_amount= round(sub_total,2)

    cursor.execute('call getProductList()')
    products = cursor.fetchall()   
    context= {'invoices':result,'products':products,'tc':tc,'product':product,'sub_total':sub_total,'net_amount':net_amount}    
    return render(request,"invoice/createinvoice.html",context)




def createProduct(request):
    tag=False
    qty=None
    amt=None
    cgst=None
    sgst=None
    igst=0
    total_amount=None
    context={}
    cursor=connection.cursor()

    cursor.execute('call products()')
    products = cursor.fetchall()
    
    cursor.execute('call mfg()')
    mfg = cursor.fetchall()

    cursor.execute('call diameter()')
    diameter = cursor.fetchall()

    cursor.execute('call grade()')
    grade = cursor.fetchall()


    if request.method=="POST":
        tag=True
        qty= int(request.POST.get("qty"))
        amount=int(request.POST.get("rate"))
        amt=amount*qty
        cgst=((amount*9)/100)*qty
        sgst=((amount*9)/100)*qty
        
        total_amount=cgst+amt+sgst+igst
        name=request.POST.get('product')
        mfg=request.POST.get('mfg')
        diameter=request.POST.get('diameter')
        grade=request.POST.get('grade')
        quantity=request.POST.get('qty')
        unit=request.POST.get('unit')
        rate=request.POST.get('rate')
        Product(name=name,mfg=mfg,diameter=diameter,grade=grade,qty=quantity,unit=unit,rate=rate,taxable_amount=amt,cgst=cgst,sgst=sgst,igst=igst,total_amount=total_amount).save()
        print("----------Data Save-----------")

    context={'products':products,'mfg':mfg,'diameter':diameter,'grade':grade,'tag':tag,'qty':qty,'amount':amt,'cgst':cgst,'total_amount':total_amount}
    return render(request,"invoice/product.html",context)


def updateProduct(request,pk):
    Products=Product.objects.get(id=pk)
    context={'p':Products}
    if request.method=="POST":
        Products.igst=0
        total_amount=0
        name=request.POST.get('product')
        Products.mfg=request.POST.get('mfg')
        Products.diameter=request.POST.get('diameter')
        Products.grade=request.POST.get('grade')
        # Products.quantity=request.POST.get('qty')
        Products.unit=request.POST.get('unit')
        Products.rate=request.POST.get('rate')
        Products.qty= int(request.POST.get("qty"))
        Products.rate=int(request.POST.get("rate"))
        Products.taxable_amount=Products.rate*Products.qty
        Products.cgst=((Products.rate*9)/100)*Products.qty
        Products.sgst=((Products.rate*9)/100)*Products.qty
        Products.total_amount=Products.taxable_amount+Products.sgst+Products.cgst+Products.igst
        Products.save()
       
        return HttpResponseRedirect(reverse("invoice-create"))
            
    return render(request,"invoice/editproduct.html",context)


def deleteProduct(request,pk):
    Products=Product.objects.get(id=pk)
    Products.delete()
    
    return HttpResponseRedirect(reverse("invoice-create"))


def tc(request):
    cursor=connection.cursor()
    cursor.execute('call tc()')
    msg=None
    tc = cursor.fetchall()

    if request.POST:
        msg="terms and conditions satisfy..."
    context={'tc':tc,'msg':msg}
    return render(request,"invoice/tc.html",context)

