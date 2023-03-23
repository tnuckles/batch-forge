 #!usr/bin/env python
# Series of functions that break apart the name of a PDF and return a specific value

import math, datetime, os
from datetime import datetime

def name(pdf):
    return pdf.split('/')[-1].split('.pdf')[0]

def friendlyName(pdf):
    friendlyPdfName = orderNumber(pdf) + ' ' +  orderItem(pdf) + ' ' + templateName(pdf)
    return friendlyPdfName

def orderNumber(pdf):
    return name(pdf).split('-')[0]

def orderItem(pdf):
    return name(pdf).split('-')[1]

def dueDate(pdf):
    fileName = name(pdf)
    return datetime.date(datetime.strptime(fileName.split('(')[1].split(')')[0], '%Y-%m-%d')) 

def shipMethod(pdf):
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

def oddOrEven(pdf):
    return int(name(pdf).split('-')[9].split('Qty ')[1]) % 2

def templateName(pdf):
    return name(pdf).split('-')[10]

def length(pdf):
    return float(name(pdf).split('-')[11].split('L')[1])

def width(pdf):
    return int(name(pdf).split('-')[12].split('W')[1])

def height(pdf):
    return float(name(pdf).split('-')[13].split('H')[1])

def calculateLength(quantity, height):
    quantity = int(quantity)
    height = float(height)

    first = math.floor(quantity / 2) #quantity divided by two, rounded down, to get the number of panels we can fit side by side
    second = first + (quantity % 2) #quantity + 1 for any odd-quantitied items
    third = height + .5 # height + .5 because there's a .5" gap between each row
    length = second * third
    return length

def getAll(pdf):
    pdfDict = {
        'orderNumber': orderNumber(pdf),
        'orderItem': orderItem(pdf),
        'dueDate': dueDate(pdf),
        'shipMethod': shipMethod(pdf),
        'material': material(pdf),
        'orderSize': size(pdf),
        'orderRepeat': repeat(pdf),
        'orderQuantity': quantity(pdf),
        'templateName': templateName(pdf),
        'orderLength': length(pdf),
        'orderWidth': width(pdf),
        'orderHeight': height(pdf),
    }
    return pdfDict
