#!usr/bin/env python

import os
from datetime import date

TODAY = date.today()

# Location for Caldera's Folders
if os.path.expanduser("~").split("/")[-1] == "Trevor":
    CALDERA_DIR = "/Users/Trevor/Documents/Scripts/Misc/caldera/var/public/"
    DRIVE_DIR = "/Volumes/GoogleDrive/Shared drives/# Production/#LvD Test Fulfillment"
else:
    CALDERA_DIR = "/opt/caldera/var/public/"
    DRIVE_DIR = "/Users/caldera/Library/CloudStorage/GoogleDrive-matthew@lovevsdesign.com/Shared Drives/# Production/#LvD Fulfillment"

"""
Removing those pesky headers
"""
# batch_headers = {
#     'ot': CALDERA_DIR + 'z_Storage/assets/headers/999999999-headerOt.pdf',
#     'late': CALDERA_DIR + 'z_Storage/assets/headers/999999999-headerLate.pdf',
#     'today': CALDERA_DIR + 'z_Storage/assets/headers/999999999-headerToday.pdf',
#     'tomorrow': CALDERA_DIR + 'z_Storage/assets/headers/999999999-headerTomorrow.pdf',
#     'future': CALDERA_DIR + 'z_Storage/assets/headers/999999999-headerFuture.pdf',
# }

HOTFOLDERS_DIR = CALDERA_DIR + "1 Hotfolders/"
BATCH_FOLDERS_DIR = CALDERA_DIR + "2 Batch Folders/"
DOWNLOAD_DIR = CALDERA_DIR + "3 Downloaded/"
NEEDS_ATTENTION_DIR = CALDERA_DIR + "4 Needs Attention/"
SORTING_DIR = CALDERA_DIR + "5 Sorted for Print/"
PAST_ORDERS_DIR = CALDERA_DIR + "# Past Orders/"

full_length_split_percentage = 0.85  # 85%. This is the percentage that batching will try to fill with full, then save the rest for samples.

PAPER_TYPES = ("Smooth", "Woven", "Woven 2", "Traditional")

DIR_LOOKUP = {  # Dictionary for dynamically creating a directory path for sorting based on lookup tables
    "Sm": "Smooth/",  # Smooth Folders
    "Smooth": "Smooth/",
    "Wv": "Woven/",  # Woven Folders
    "Woven": "Woven/",
    "Tr": "Traditional/",  # Traditional Folders
    "Full": "Full/",  # Full Folders
    "Samp": "Sample/",
    "Sample": "Sample/",  # Sample Folders
    "RepeatDict": {
        2: "Repeat 2/",  # 2 Foot Repeats
        3: "Repeat Non-2/",  # Non-2 Foot Repeats
        4: "Repeat Non-2/",  # Non-2 Foot Repeats
        5: "Repeat Non-2/",  # Non-2 Foot Repeats
        6: "Repeat Non-2/",  # Non-2 Foot Repeats
        7: "Repeat Non-2/",  # Non-2 Foot Repeats
        8: "Repeat Non-2/",  # Non-2 Foot Repeats
        9: "Repeat Non-2/",  # Non-2 Foot Repeats
        10: "Repeat Non-2/",  # Non-2 Foot Repeats
        11: "Repeat Non-2/",  # Non-2 Foot Repeats
        12: "Repeat Non-2/",  # Non-2 Foot Repeats
        "Rp 2": "Repeat 2/",  # 2 Foot Repeats
        "Rp 4": "Repeat Non-2/",  # Non-2 Foot Repeats
        "Rp 6": "Repeat Non-2/",  # Non-2 Foot Repeats
        "Rp 8": "Repeat Non-2/",  # Non-2 Foot Repeats
        "Rp 10": "Repeat Non-2/",  # Non-2 Foot Repeats
        "Rp 12": "Repeat Non-2/",  # Non-2 Foot Repeats
    },
    1: "Odd Panels/",
    0: "Even Panels/",
    "MaterialLength": {  # this should reflect printable length. Smooth rolls are 150 feet, but we have 148 printable feet on each roll.
        "Smooth": (150 - 6) * 12,
        "Woven": (100 - 6) * 12,
        "Traditional": (100 - 6) * 12,
        "Sm": (150 - 6) * 12,
        "Wv": (100 - 6) * 12,
        "Tr": (100 - 6) * 12,
    },
}

SUBSTRATE = {
    "Woven Peel and Stick": "Wv",
    "Woven": "Wv",
    "Wv": "Woven",
    "Smooth Peel and Stick": "Sm",
    "Smooth": "Sm",
    "Sm": "Smooth",
    "Traditional": "Tr",
}

SHIP_METHODS = {
    "Standard": "Stnd",
    "Sample Standard": "SmStnd",
    "International Standard": "InStnd",
    "Priority": "Prty",
    "International Priority": "InPrty",
    "Rush": "Rush",
    "International Rush": "InRush",
}

pdfs_to_rename = {}

COUNT_OF_REF_PDFS = (
    {}  # Running count of PDFs that are referenced during sample creating. If a PDF is referenced more than once, the order and PDF are printed to alert fulfillment of dual-type samples
)

ORDER_ITEMS_DICT = {}
