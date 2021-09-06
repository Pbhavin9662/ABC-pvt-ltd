from django.urls import path
from invoice.views import *
urlpatterns = [
    path('',invoiceList,name="invoiceList"),
    path('create/invoice/',invoiceCreate,name="invoice-create"),
    path('create/product/',createProduct,name="product-create"),
    path('create/tc/',tc,name="tc-create"),
    path('update/product/<int:pk>/',updateProduct,name="update-product"),
    path('delete/product/<int:pk>/',deleteProduct,name="delete-product")

]
