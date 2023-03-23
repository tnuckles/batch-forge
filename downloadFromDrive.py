#!usr/bin/env python

from datetime import date
import getPdfData as getPdf
from glob import glob
import wallpaperSorterVariables as gv
from batchCreate import tryToMovePDF

today = date.today()

def transferFilesFromDrive():
    # New name convention: 300013884-1-(2022-02-02)-Stnd-Wv-Samp-Rp 2-Qty 1-Watercolor Herringbone-L9.5-W25-H9

    pdfDict = gv.dirLookupDict
    list_to_transfer = glob(gv.driveLocation + '/*.pdf')
    if len(list_to_transfer) < 1:
        print('\n| No files to transfer from Google Drive.')
        return
    for print_pdf in list_to_transfer:
        pdf_name = getPdf.name(print_pdf)
        pdf_friendly_name = getPdf.friendlyName(pdf_name)
        pdf_material = pdfDict[getPdf.material(pdf_name)]
        pdf_order_size = pdfDict[getPdf.size(pdf_name)]
        pdf_repeat = pdfDict['RepeatDict'][getPdf.repeat(pdf_name)]
        even_or_odd = pdfDict[getPdf.oddOrEven(pdf_name)]
        if pdf_order_size == 'Full':
            dest_path = gv.sortingDir + '3 - Today/' + pdf_material + pdf_order_size + pdf_repeat + even_or_odd + pdf_name + '.pdf'
        else:
            dest_path = gv.sortingDir + '3 - Today/' + pdf_material + pdf_order_size + pdf_name + '.pdf'
        print(f'\n| Trying to move {pdf_friendly_name}.')
        tryToMovePDF(print_pdf, dest_path, pdf_friendly_name, verbose=False)
    print('\n| Finished transferring files from Google Drive.')

    return