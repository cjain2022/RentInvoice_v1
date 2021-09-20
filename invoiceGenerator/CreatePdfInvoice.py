# This code will provide a function to generate a pdf file 
# Reference Link : https://stackabuse.com/creating-pdf-invoices-in-python-with-borb/


# Helper Functions 
# New imports
import enum
from os import cpu_count
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable as Table
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.layout.layout_element import Alignment
from datetime import datetime
import random

HEADING_COLOR="ce93d8" #"016934" (green)
ROWS_COLOR="f3e5f5" # initially "BBBBBB"
TEXT_COLOR="000000" # initially white

def _build_invoice_overview_info(name,billDate,mobile,dueDate,total):    
    table_001 = Table(number_of_rows=3, number_of_columns=4)
	
    table_001.add(Paragraph("Name", font="Helvetica-Bold"))
    table_001.add(Paragraph(name))    
    table_001.add(Paragraph("Billing Date", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))        
    table_001.add(Paragraph("%d/%d/%d" % (billDate.day, billDate.month, billDate.year)))
	
    table_001.add(Paragraph("MobileNumber:", font="Helvetica-Bold"))    
    table_001.add(Paragraph(mobile))
    table_001.add(Paragraph("Due Date", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table_001.add(Paragraph("%d/%d/%d" % (dueDate.day, dueDate.month, dueDate.year)))   
	
    table_001.add(Paragraph("Total Amount:", font="Helvetica-Bold"))    
    table_001.add(Paragraph("%d" % (total), font="Helvetica-Bold"))
    table_001.add(Paragraph(" "))
    table_001.add(Paragraph(" "))

    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))    		
    table_001.no_borders()
    return table_001

# New imports
from borb.pdf.canvas.color.color import HexColor, X11Color

# New import
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable as Table
from borb.pdf.canvas.layout.table.table import TableCell

def _electricity_charges(lastElectricityReading,newElectricityReading,pricePerUnitElectricity,unitsConsumed,electricity_amount):  
    table_001 = Table(number_of_rows=3, number_of_columns=5)  
    table_001.add(TableCell(Paragraph('ELECTRICITY CHARGES',font_size=Decimal(14),font_color=HexColor(TEXT_COLOR)),col_span=5,background_color=HexColor(HEADING_COLOR)))
    for h in ["Prev Reading", "New Reading","Units Consumed","Unit Price","Charges" ]:  
        table_001.add(  
            TableCell(  
                Paragraph(h, font_color=HexColor(TEXT_COLOR),font_size=Decimal(10)),  
                background_color=HexColor(HEADING_COLOR),  
            )  
        )  
    c = HexColor(ROWS_COLOR)
    table_001.add(TableCell(Paragraph(str(lastElectricityReading)), background_color=c))  
    table_001.add(TableCell(Paragraph(str(newElectricityReading)), background_color=c))
    table_001.add(TableCell(Paragraph(str(unitsConsumed)), background_color=c))
    table_001.add(TableCell(Paragraph("Rs " + str(pricePerUnitElectricity)), background_color=c))  
    table_001.add(TableCell(Paragraph("Rs " + str(electricity_amount)), background_color=c))
    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))  
    table_001.no_borders()  
    return table_001

def _water_charges(waterChargePerPerson,personCount,water_amount):  
    table_001 = Table(number_of_rows=3, number_of_columns=5)  
    table_001.add(TableCell(Paragraph('WATER CHARGES',font_size=Decimal(14),font_color=X11Color("White")),col_span=5,background_color=HexColor(HEADING_COLOR)))
    for colNum, h in enumerate( ["# Of Person", "Per Person Charge","Charges"] ):  
        cspan = 3 if colNum==1 else 1
        table_001.add(  
            TableCell(  
                Paragraph(h, font_color=HexColor(TEXT_COLOR),font_size=Decimal(10)),
                col_span=cspan,  
                background_color=HexColor(HEADING_COLOR),  
            )  
        )  
    c = HexColor(ROWS_COLOR)
    table_001.add(TableCell(Paragraph(str(personCount)), background_color=c))  
    table_001.add(TableCell(Paragraph("Rs "+str(waterChargePerPerson)),col_span=3,background_color=c))
    table_001.add(TableCell(Paragraph("Rs " + str(water_amount)), background_color=c))
    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))  
    table_001.no_borders()  
    return table_001

def _fixed_charges(description_n_charges):  
    rows_needed=len(description_n_charges)+2 # (as 2 rows used for heading )
    table_001 = Table(number_of_rows=rows_needed, number_of_columns=5)  
    table_001.add(TableCell(Paragraph('FIXED CHARGES',font_size=Decimal(14),font_color=HexColor(TEXT_COLOR)),col_span=5,background_color=HexColor(HEADING_COLOR)))
    for colNum, h in enumerate( ["Description","Charges"] ):  
        cspan = 4 if colNum==0 else 1
        table_001.add(  
            TableCell(  
                Paragraph(h, font_color=HexColor(TEXT_COLOR),font_size=Decimal(10)),
                col_span=cspan,  
                background_color=HexColor(HEADING_COLOR),  
            )  
        )  
    
    odd_color = HexColor(ROWS_COLOR)  
    even_color = HexColor(ROWS_COLOR) #HexColor("FFFFFF")  
    for row_number, item in enumerate(description_n_charges):  
        c = even_color if row_number % 2 == 0 else odd_color  
        table_001.add(TableCell(Paragraph(item[0]),col_span=4 ,background_color=c))  
        table_001.add(TableCell(Paragraph("Rs "+str(item[1])), background_color=c))  

    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))  
    table_001.no_borders()  
    return table_001


def _build_itemized_summary_table(subtotal,discount,total):  
    table_001 = Table(number_of_rows=3, number_of_columns=5)    
    table_001.add(TableCell(Paragraph("Sub Total ", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT,), col_span=4,))  
    table_001.add(TableCell(Paragraph("Rs "+str(subtotal))))  
    table_001.add(TableCell(Paragraph("Discounts", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT,),col_span=4,))  
    table_001.add(TableCell(Paragraph("Rs "+str(discount))))  
    table_001.add(TableCell(Paragraph("Total", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT  ), col_span=4,))  
    table_001.add(TableCell(Paragraph("Rs "+str(total))))  
    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))  
    table_001.no_borders()  
    return table_001
    
# Actual Work Begins 

from borb.pdf.document import Document
from borb.pdf.page.page import Page
# New imports
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from decimal import Decimal
# New import
from borb.pdf.canvas.layout.image.image import Image

# TO finally generate pdf 
from borb.pdf.pdf import PDF

def generatePDF(filename,output_dir,DATA):
    
    # Create document
    pdf = Document()

    # Add page
    page = Page()
    pdf.append_page(page)

    page_layout = SingleColumnLayout(page)
    page_layout.vertical_margin = page.get_page_info().get_height() * Decimal(0.02)

    t1=Paragraph("RENT INVOICE", font="Helvetica-Bold",font_size=Decimal(20),font_color=X11Color("Black"),horizontal_alignment=Alignment.CENTERED)
    page_layout.add(t1)
    # Invoice information table 
    page_layout.add(_build_invoice_overview_info(DATA['name'],DATA['billDate'],DATA['mobile'],DATA['dueDate'],DATA['total']))  
    
    # Empty paragraph for spacing  
    page_layout.add(Paragraph(" "))

    # Electricty Charges 
    page_layout.add(_electricity_charges(DATA['lastElectricityReading'],DATA['newElectricityReading'],DATA['pricePerUnitElectricity'],DATA['unitsConsumed'],DATA['electricity_amount']))

    # Water Charges 
    page_layout.add(_water_charges(DATA['waterChargePerPerson'],DATA['personCount'],DATA['water_amount']))
    
    # Fixed CHarges 
    page_layout.add(_fixed_charges(DATA['description_n_charges']))
    
    # Empty paragraph for spacing  
    page_layout.add(Paragraph(" "))

    # Itemized description
    page_layout.add(_build_itemized_summary_table(DATA['subtotal'],DATA['discount'],DATA['total']))

    # New import

    with open(output_dir+filename, "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, pdf)


if __name__=='__main__':
    generatePDF(filename="output.pdf",output_dir="",DATA={})
