from django.urls import path
from invoiceGenerator import views
urlpatterns = [
    path('downloadInvoice/',views.downloadInvoice,name='downloadInvoice'),
    path('',views.invoiceView, name="invoiceView"),
]
