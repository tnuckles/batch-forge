#!usr/bin/env python

import os, shutil, glob, pikepdf
from datetime import date
from PyPDF2 import PdfFileReader, PdfFileWriter, errors

import getPdfData as getPdf
import wallpaperSorterVariables as gv
today = date.today()

def splitMultiPagePDFs(print_pdf):
    friendly_name = getPdf.friendlyName(print_pdf)
    try:
        pdf = pikepdf.Pdf.open(print_pdf)
        NumOfPages = len(pdf.pages)
    except:
        print(f'| Couldn\'t check the number of pages on {friendly_name}')
        pass
    if NumOfPages > 1:
            print(f'| {friendly_name} has more than one page in its PDF. Splitting now.')
            templateName = getPdf.templateName(print_pdf)
            namePt1 = print_pdf.split('Qty ')[0] + 'Qty '
            namePt2 = print_pdf.split(templateName)[1]
            repeat = getPdf.repeat(print_pdf) ##
            quantity = getPdf.quantity(print_pdf)
            for n, page in enumerate(pdf.pages):
                dst = pikepdf.Pdf.new()
                dst.pages.append(page)
                dst.save(namePt1 + str(quantity) + '-' + templateName + ' Panel ' + str(n + 1) + namePt2)
            try:
                os.remove(print_pdf)
                print(f'| Finished splitting {friendly_name}')
            except:
                print(f'| Split the pages of {friendly_name},\nbut couldn\'t remove the original.')

def checkRepeatSize():
    for printPDF in glob.iglob(gv.downloadDir + '*.pdf'):
        printPDFFull = printPDF.split('/')[-1].split('-')[7]
        printPDFrepeat = int(printPDF.split('/')[-1].split('-')[8].split('Rp ')[1])
        if printPDFFull == 'Full':
            if printPDFrepeat % 2 == 1:
                try:
                    shutil.move(printPDF, gv.needsAttention)
                    print('| File has an odd repeat and has been moved to 4 Needs Attention')
                    print('| File:', printPDF.split('/')[-1])
                except shutil.Error:
                    shutil.copy(printPDF, gv.needsAttention)
                    try:
                        os.remove(printPDF)
                    except OSError:
                        print('|> Could not successfully remove file.')
                        print('|> File:', printPDF)
                except FileNotFoundError:
                    print('| Couldn\'t find the following file.')
                    print('| File:', printPDF)
            elif printPDFrepeat == 2:
                continue
            elif printPDFrepeat > 2:
                try:
                    cropMultiPanelPDFs(printPDF)
                except errors.PdfReadError:
                    print('| Couldn\'t crop the panels for the following order. Please check non-repeat 2 folders.')
                    continue

    return

def checkRepeatDuringBatching(pdf, batchDir):
    printPDFFull = pdf.split('/')[-1].split('-')[7]
    printPDFrepeat = int(pdf.split('/')[-1].split('-')[8].split('Rp ')[1])
    if printPDFFull == 'Full':
        if printPDFrepeat % 2 == 1:
            try:
                shutil.move(pdf, gv.needsAttention)
                print('| File has an odd repeat and has been moved to 4 Needs Attention')
                print('| File:', pdf.split('/')[-1])
            except shutil.Error:
                shutil.copy(pdf, gv.needsAttention)
                try:
                    os.remove(pdf)
                except OSError:
                    print('|> Could not successfully remove file.')
                    print('|> File:', pdf)
                    return
            except FileNotFoundError:
                print('| Couldn\'t find the following file.')
                print('| File:', pdf)
                return
        elif printPDFrepeat == 2:
            return
        elif printPDFrepeat > 2:
            try:
                cropMultiPanelPDFs(pdf, batchDir)
            except errors.PdfReadError:
                print('| Couldn\'t crop the panels for the following pdf. Please check the batch folder')
                print('| PDF:', pdf.split('/')[-1])
                return

def determine_panel_quantity(quantity, repeat, OT=False):   
 
    quantity_per_panel_dict = {}

    quantity_counter = 0
    repeat = int(repeat / 2)
    for panel in range(repeat):
        quantity_per_panel_dict[panel + 1] = 0
    if OT != False:
        quantity_per_panel_dict[int(OT)] = quantity
    else:
        while quantity_counter < quantity:
            for panel in range(repeat):
                panel_num = panel+1
                quantity_per_panel_dict[panel_num] += 1
                quantity_counter += 1
                if quantity_counter == quantity:
                    break
                elif panel_num == repeat:
                    panel = 0

    return quantity_per_panel_dict

def cropMultiPanelPDFs(printPDFToSplit, batchDir):
    storageDir = gv.calderaDir + '# Past Orders/Original Files/'   
    shutil.copy(printPDFToSplit, storageDir)
    
    orderDict = {
        'fileName':printPDFToSplit.split('.pdf')[0],
        'orderNumber': getPdf.orderNumber(printPDFToSplit),
        'orderItem': getPdf.orderItem(printPDFToSplit),
        'orderDueDate': getPdf.dueDate(printPDFToSplit),
        'shipVia': getPdf.shipMethod(printPDFToSplit),
        'material': getPdf.material(printPDFToSplit),
        'orderSize': getPdf.size(printPDFToSplit),
        'repeat': getPdf.repeat(printPDFToSplit),
        'repeatPanels': int(getPdf.repeat(printPDFToSplit) / 2),
        'quantity': getPdf.quantity(printPDFToSplit),
        'oddOrEven': getPdf.oddOrEven(printPDFToSplit),
        'templateName': getPdf.templateName(printPDFToSplit),
        'orderLength': getPdf.length(printPDFToSplit),
        'orderWidth': getPdf.width(printPDFToSplit),
        'orderHeight': getPdf.height(printPDFToSplit),
        'multiPagePDFs' : [],
        'PDFPanelsToCombine' : [],
        }
    
    orderDict['CroppedPDFName'] = orderDict['fileName'].split(orderDict['templateName'])[0] + orderDict['templateName'] + ' Split' + orderDict['fileName'].split(orderDict['templateName'])[1] + '.pdf'
    
    if '(OTP' in getPdf.name(orderDict['templateName']):
        OTPanel = getPdf.name(orderDict['templateName']).split('(OTP')[1].split(')')[0]
        quantity_per_panel_dict = determine_panel_quantity(orderDict['quantity'], orderDict['repeat'], OTPanel)
    else:
        quantity_per_panel_dict = determine_panel_quantity(orderDict['quantity'], orderDict['repeat'])

    os.chdir(batchDir)
    for page in range(orderDict['repeatPanels']):
        writer = PdfFileWriter()
        inputPDF = open(printPDFToSplit,'rb')
        cropPDF = PdfFileReader(inputPDF)
        page = cropPDF.getPage(0)
        lowerLeftX = 0
        lowerLeftY = 0
        upperRightX = 1800
        upperRightY = cropPDF.getPage(0).cropBox.getUpperRight()[1]
        for cropCount in range(orderDict['repeatPanels']):
            page.trimBox.lowerLeft = (lowerLeftX, lowerLeftY)
            page.trimBox.upperRight = (upperRightX, upperRightY)
            page.bleedBox.lowerLeft = (lowerLeftX, lowerLeftY)
            page.bleedBox.upperRight = (upperRightX, upperRightY)
            page.cropBox.lowerLeft = (lowerLeftX, lowerLeftY)
            page.cropBox.upperRight = (upperRightX, upperRightY)
            writer.addPage(page)
            lowerLeftX += 1728
            upperRightX += 1728
            printPDFName = batchDir + '/' + orderDict['orderNumber'] + '-' + orderDict['orderItem'] + '-' + str(cropCount + 1) + '.pdf'
            if printPDFName in orderDict['multiPagePDFs']:
                continue
            else:
                orderDict['multiPagePDFs'].append(printPDFName)
            with open(printPDFName, "wb") as outputPDF:
                writer.write(outputPDF)
        inputPDF.close()

    for PDF in orderDict['multiPagePDFs']:
        writer = PdfFileWriter()
        try:
            printPDF = PdfFileReader(open(PDF, "rb"))
        except errors.PdfReadError:
            print('| Couldn\'t fix file. Skipping.\n| File:', PDF)
            continue
        numOfPages = printPDF.getNumPages()

        for pageNum in range(numOfPages):
            if (pageNum + 1) < numOfPages:
                continue
            else:
                writer.addPage(printPDF.getPage(pageNum))

        newNamePt1 = orderDict['fileName'].split(orderDict['templateName'])[0]
        newNamePt2 = orderDict['fileName'].split(orderDict['templateName'])[1]
        panelNum = orderDict['templateName'] + ' TQ' + str(orderDict['quantity']) + ' P' + str(pageNum + 1)
        newName = newNamePt1 + panelNum + newNamePt2 + '.pdf'
        
        new_quantity_name_pt1 = newName.split('Qty ' + str(orderDict['quantity']))[0] + 'Qty '
        new_quantity_name_pt2 = newName.split('Qty ' + str(orderDict['quantity']))[1]
        adjusted_quantity = str(quantity_per_panel_dict[pageNum + 1])
        final_name = new_quantity_name_pt1 + adjusted_quantity + new_quantity_name_pt2

        if final_name in orderDict['PDFPanelsToCombine']:
            continue
        else:
            orderDict['PDFPanelsToCombine'].append(final_name)

        with open(final_name, 'wb') as outputPDF:
            writer.write(outputPDF)
    
    # splitAndCombinedPDF = combineSplitPDFS(orderDict['PDFPanelsToCombine'], orderDict['CroppedPDFName'])

    for PDF in orderDict['multiPagePDFs']:
        os.remove(PDF)
    os.remove(printPDFToSplit)

    for print_pdf in glob.glob(batchDir + '/*-Qty 0-*'):
        os.remove(print_pdf)