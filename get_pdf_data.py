 #!usr/bin/env python
# Series of functions that break apart the name of a PDF and return a specific value

import math, datetime, os
from datetime import datetime

def name(pdf):
    return pdf.split('/')[-1].split('.pdf')[0]

def friendly_name(pdf):
    friendly_pdf_name = order_number(pdf) + ' ' +  order_item(pdf) + ' ' + template_name(pdf)
    return friendly_pdf_name

def order_number(pdf):
    return name(pdf).split('-')[0]

def order_item(pdf):
    return name(pdf).split('-')[1]

def due_date(pdf):
    file_name = name(pdf)
    return datetime.date(datetime.strptime(file_name.split('(')[1].split(')')[0], '%Y-%m-%d')) 

def ship_method(pdf):
    return name(pdf).split('-')[5]

def material(pdf):
    return name(pdf).split('-')[6]

def size(pdf):
    return name(pdf).split('-')[7]

def repeat(pdf):
    try:
        return int(name(pdf).split('-')[8].split('Rp ')[1])
    except IndexError:
        first_half = pdf.split(')-')[0]
        second_half = pdf.split(')-')[1]
        shipping = ')-Stnd-'
        pdf = os.rename(pdf, first_half + shipping + second_half)
        return int(name(pdf).split('-')[8].split('Rp ')[1])
        
def quantity(pdf):
    return int(name(pdf).split('-')[9].split('Qty ')[1])

def odd_or_even(pdf):
    return int(name(pdf).split('-')[9].split('Qty ')[1]) % 2

def template_name(pdf):
    return name(pdf).split('-')[10]

def length(pdf):
    return float(name(pdf).split('-')[11].split('L')[1])

def width(pdf):
    return int(name(pdf).split('-')[12].split('W')[1])

def height(pdf):
    return float(name(pdf).split('-')[13].split('H')[1])

def calculate_length(quantity, height):
    quantity = int(quantity)
    height = float(height)

    first = math.floor(quantity / 2) #quantity divided by two, rounded down, to get the number of panels we can fit side by side
    second = first + (quantity % 2) #quantity + 1 for any odd-quantitied items
    third = height + .5 # height + .5 because there's a .5" gap between each row
    length = second * third
    return length

def get_all(pdf) -> dict:
    pdf_dict = {
        'order_number': order_number(pdf),
        'order_item': order_item(pdf),
        'due_date': due_date(pdf),
        'ship_method': ship_method(pdf),
        'material': material(pdf),
        'order_size': size(pdf),
        'order_repeat': repeat(pdf),
        'order_quantity': quantity(pdf),
        'template_name': template_name(pdf),
        'order_length': length(pdf),
        'order_width': width(pdf),
        'order_height': height(pdf),
    }
    return pdf_dict
