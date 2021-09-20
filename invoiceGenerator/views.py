from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def invoiceView(request):
    context={}
    return render(request,'invoiceGenerator/invoice.html',context=context)

from django.http import FileResponse
from datetime import datetime
from datetime import timedelta
def downloadInvoice(request):
    print(request.POST)
    
    # Billing Deadline and Dates 
    billDate_str=request.POST['billDate']
    billDate=datetime.strptime(billDate_str,'%Y-%m-%d')
    print(type(billDate))
    dueIn=int(request.POST['dueIn'])
    dueDate=billDate+timedelta(days=dueIn)

    # Personal Details Of Tenant 
    fname=request.POST['fname']
    lname=""
    if 'lname' in request.POST and len(request.POST['lname'])>0:
        lname=request.POST['lname']
    name=fname+" "+lname
    
    mobile="NOT AVAILABLE"
    if 'mob_num' in request.POST and len(request.POST['mob_num'])>0:
        mobile=request.POST['mob_num']
    
    # Electricity Charges 
    lastElectricityReading=float(request.POST['lastElectricityReading'])
    newElectricityReading=float(request.POST['newElectricityReading'])
    # pending task of handling image 
    # newElectricityReadingImage=request.GET['newElectricityReadingImage'] # Check 
    pricePerUnitElectricity=float(request.POST['pricePerUnitElectricity'])
    unitsConsumed=newElectricityReading-lastElectricityReading
    electricity_amount=unitsConsumed*pricePerUnitElectricity

    # Water Charges 
    waterChargePerPerson=float(request.POST['waterCharge'])
    personCount=int(request.POST['personCount'])
    water_amount=waterChargePerPerson*personCount

    # Fixed Charges 
    description_n_charges=[] # this will store all the results 
    monthlyRent=float(request.POST['monthlyRent'])
    garbageCharge=float(request.POST['garbageCharge'])
    AdditionalPaymentReason=""
    AdditionalPayment=0
    if 'AdditionalPaymentReason' in request.POST and len(request.POST['AdditionalPaymentReason'])>0:
        AdditionalPaymentReason=request.POST['AdditionalPaymentReason']
    if 'AdditionalPayment' in request.POST and len(request.POST['AdditionalPayment'])>0:
        AdditionalPayment=float(request.POST['AdditionalPayment'])
    if len(AdditionalPaymentReason) >0 and AdditionalPayment>0: 
        description_n_charges=[
                ('Monthly Rent',int(monthlyRent)),
                ('Garbage Collection',int(garbageCharge)),
                (AdditionalPaymentReason,int(AdditionalPayment))    
        ]
    # if additional charges was blank then we will not show it in the bill 
    if len(AdditionalPaymentReason)==0 or AdditionalPayment==0 :
        description_n_charges=[
            ('Monthly Rent',int(monthlyRent)),
            ('Garbage Collection',int(garbageCharge)),    
        ]

    #Discounts
    discount=0
    if 'Discounts' in request.POST and len(request.POST['Discounts'])>0:
        discount=float(request.POST['Discounts'])
    
    #Computation
    subtotal=0 
    for (desc,chrg) in description_n_charges:
        subtotal=subtotal+chrg
    subtotal=electricity_amount+water_amount+subtotal
    total=subtotal-discount 

    DATA={
        'name':name,
        'billDate':billDate,
        'mobile':mobile,
        'dueDate':dueDate,
        'lastElectricityReading':lastElectricityReading,
        'newElectricityReading':newElectricityReading,
        'pricePerUnitElectricity':pricePerUnitElectricity,
        'unitsConsumed':unitsConsumed,
        'electricity_amount':electricity_amount,
        'waterChargePerPerson':waterChargePerPerson,
        'personCount':personCount,
        'water_amount':water_amount,
        'description_n_charges':description_n_charges,
        'subtotal':subtotal,
        'discount':discount,
        'total':total,
    }
    
    filename="RENT_INVOICE_"+name+"_"+billDate_str+".pdf"
    output_dir="invoiceGenerator/invoice_outputs/"
    from invoiceGenerator.CreatePdfInvoice import generatePDF
    generatePDF(filename,output_dir,DATA)

    invoice=open(output_dir+filename,'rb')
    response=FileResponse(invoice)
    return response

'''
# Code : To Send Files 
from django.http import FileResponse
def test(request):
    img = open('images/bojnice.jpg', 'rb')
    response = FileResponse(img)
    return response
'''