from datetime import date

TODAY = date.today()

PRINTER_DICT = {
    "1": ["Ichi", "1 Ichi/"],
    "2": ["Ni", "2 Ni/"],
    "3": ["San", "3 San/"],
    "4": ["Shi", "4 Shi/"],
    "5": ["Go", "5 Go/"],
}

# Time in minutes to lock a batch inside of a hotfolder
LOCK_IMPORTING_BATCH = 5

# Sets whether or not to compress and zip hotfolders when exported
COMPRESS_EXPORTED_BATCHES = False
