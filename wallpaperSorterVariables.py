#!usr/bin/env python

import os
from datetime import date
from sqlitedict import SqliteDict

today = date.today()

#Location for Caldera's Folders
if os.path.expanduser('~').split('/')[-1] == 'Trevor':
    calderaDir = '/Volumes/Samsung SSD/caldera/var/public/'
    driveLocation = '/Volumes/GoogleDrive/Shared drives/# Production/#LvD Test Fulfillment'
else:
    calderaDir = '/opt/caldera/var/public/'
    driveLocation = '/Users/caldera/Library/CloudStorage/GoogleDrive-matthew@lovevsdesign.com/Shared Drives/# Production/#LvD Fulfillment'

lockHotfolderBatch = 5 #time in minutes to lock the batch folders in caldera so they aren't exported prematurely.

getHeader = {
    'ot': calderaDir + 'z_Storage/assets/headers/999999999-headerOt.pdf',
    'late': calderaDir + 'z_Storage/assets/headers/999999999-headerLate.pdf',
    'today': calderaDir + 'z_Storage/assets/headers/999999999-headerToday.pdf',
    'tomorrow': calderaDir + 'z_Storage/assets/headers/999999999-headerTomorrow.pdf',
    'future': calderaDir + 'z_Storage/assets/headers/999999999-headerFuture.pdf',
}

getBlankPanel = {
    '40.25': calderaDir + 'z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 3Foot-L40.75-W25-H40.25.pdf',
    '52.25': calderaDir + 'z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 4Foot-L52.75-W25-H52.25.pdf',
    '64.25': calderaDir + 'z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 5Foot-L64.75-W25-H64.25.pdf',
    '76.25': calderaDir + 'z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 6Foot-L76.75-W25-H76.25.pdf',
    '88.25': calderaDir + 'z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 7Foot-L88.75-W25-H88.25.pdf',
    '100.25': calderaDir + 'z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 8Foot-L100.75-W25-H100.25.pdf',
    '112.25': calderaDir + 'z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 9Foot-L112.75-W25-H112.25.pdf',
    '124.25': calderaDir + 'z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 10Foot-L124.75-W25-H124.25.pdf',
    '136.25': calderaDir + 'z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 11Foot-L136.75-W25-H136.25.pdf',
    '146.25': calderaDir + 'z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 12Foot-L146.75-W25-H146.25.pdf',
    '9.0': calderaDir + 'z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Samp-Rp 2-Qty 1-BlankPdf Sample-L9.5-W25-H9.pdf',
}

getUtilityFiles = {
    'colorGuide': calderaDir + 'z_Storage/assets/color guides/LvD Color Chart Rotated.pdf',
    'rollSticker': calderaDir + 'z_Storage/assets/roll stickers/LvD Roll Stickers Rotated.pdf',
}

orderdb = calderaDir + 'z_Storage/z_WallpaperDB/lvdOrderDatabase.sqlite'
ordersDict = SqliteDict(orderdb, autocommit=True)
BatchCounterDB = calderaDir + 'z_Storage/z_WallpaperDB/lvdGlobalBatchCounter.sqlite'
globalBatchCounter = SqliteDict(BatchCounterDB, autocommit=True)
#globalBatchCounter['BatchCounter'] = 1

hotfoldersDir = calderaDir + '1 Hotfolders/'
batchFoldersDir = calderaDir + '2 Batch Folders/'
downloadDir = calderaDir + '3 Downloaded/'
needsAttention = calderaDir + '4 Needs Attention/'
sortingDir = calderaDir + '5 Sorted for Print/'
pastOrdersDir = calderaDir + '# Past Orders/'

full_length_split_percentage = 0.85 #85%. This is the percentage that batching will try to fill with full, then save the rest for samples.

dirLookupDict = { #Dictionary for dynamically creating a directory path for sorting based on lookup tables
    'Sm':'Smooth/', #Smooth Folders
    'Smooth':'Smooth/',
    'Wv':'Woven/', #Woven Folders
    'Woven':'Woven/',
    'Tr':'Traditional/', #Traditional Folders
    'Full':'Full/', #Full Folders
    'Samp':'Sample/',
    'Sample':'Sample/', #Sample Folders
    'RepeatDict':{
        2:'Repeat 2/', #2 Foot Repeats
        3:'Repeat Non-2/', #Non-2 Foot Repeats
        4:'Repeat Non-2/', #Non-2 Foot Repeats
        5:'Repeat Non-2/', #Non-2 Foot Repeats
        6:'Repeat Non-2/', #Non-2 Foot Repeats
        7:'Repeat Non-2/', #Non-2 Foot Repeats
        8:'Repeat Non-2/', #Non-2 Foot Repeats
        9:'Repeat Non-2/', #Non-2 Foot Repeats
        10:'Repeat Non-2/', #Non-2 Foot Repeats
        11:'Repeat Non-2/', #Non-2 Foot Repeats
        12:'Repeat Non-2/', #Non-2 Foot Repeats
        'Rp 2':'Repeat 2/', #2 Foot Repeats
        'Rp 4':'Repeat Non-2/', #Non-2 Foot Repeats
        'Rp 6':'Repeat Non-2/', #Non-2 Foot Repeats
        'Rp 8':'Repeat Non-2/', #Non-2 Foot Repeats
        'Rp 10':'Repeat Non-2/', #Non-2 Foot Repeats
        'Rp 12':'Repeat Non-2/', #Non-2 Foot Repeats
    },
    1:'Odd Panels/',
    0:'Even Panels/',
    'MaterialLength':{ #this should reflect printable length. Smooth rolls are 150 feet, but we have 148 printable feet on each roll.
        'Smooth' : (150-6) * 12,
        'Woven' : (100-6) * 12,
        'Traditional' : (100-6) * 12,
        'Sm' : (150-6) * 12,
        'Wv' : (100-6) * 12,
        'Tr' : (100-6) * 12,
    },
}

substrate = {
    'Woven Peel and Stick':'Wv',
    'Woven':'Wv',
    'Wv':'Woven',
    'Smooth Peel and Stick':'Sm',
    'Smooth':'Sm',
    'Sm':'Smooth',
    'Traditional':'Tr'
    }

shippingMethods = {
    'Standard':'Stnd',
    'Sample Standard':'SmStnd',
    'International Standard':'InStnd',
    'Priority':'Prty',
    'International Priority':'InPrty',
    'Rush':'Rush',
    'International Rush':'InRush'
}

pdfsToRename = {
    
}

countOfRefPdfs = { #Running count of PDFs that are referenced during sample creating. If a PDF is referenced more than once, the order and PDF are printed to alert fulfillment of dual-type samples
    
}

orderItemsDict = {
}


