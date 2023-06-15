'''
Configuration file for Batch Forge
'''

from sqlitedict import SqliteDict

CALDERA_DIR = '/Users/Trevor/Documents/Scripts/Misc/caldera/var/public/'
DRIVE_DIR = ''

GENERAL_VARS = {
    "Printer Waste": 45 + 51, # In inches. First number is takeup waste and second number is trailing waste.
    'Full Samp Split': 0.92, # As a percentage. This is the percentage that batching will try to fill with full, then save the rest for samples.
    'Paper Types': {
        "Smooth": {
            "Name": 'Smooth',
            "Short Name": "Sm",
            "Dir Name": "Smooth/",
            "Length": 150,
        }, 
        "Woven": {
            "Name": 'Woven',
            "Short Name": "Wv",
            "Dir Name": "Woven/",
            "Length": 150,
        },
        "Traditional":{
            "Name": 'Traditional',
            "Short Name": "Tr",
            "Dir Name": "Traditional/",
            "Length": 150,
        },
    },
    'Shipping Methods':{
        "Standard": "Stnd",
        "Sample Standard": "SmStnd",
        "International Standard": "InStnd",
        "Priority": "Prty",
        "International Priority": "InPrty",
        "Rush": "Rush",
        "International Rush": "InRush",
    },
}

GENERAL_VARS_HIDDEN = {
    'Caldera Dirs': {
        'Hotfolders': CALDERA_DIR + "1 Hotfolders/",
        'Batches': CALDERA_DIR + "2 Batch Folders/",
        'Downloads': CALDERA_DIR + "3 Downloaded/",
        'Attention': CALDERA_DIR + "4 Needs Attention/",
        'Sorting': CALDERA_DIR + "5 Sorted for Print/",
        'Past Batches': CALDERA_DIR + "# Past Orders/",
        },
    'Lookups': {  # Dictionary for dynamically creating a directory path for sorting based on lookup tables
        'Paper Dirs': {
            "Sm": GENERAL_VARS['Paper Types']['Smooth']['Dir Name'],  # Smooth Folders
            "Smooth": GENERAL_VARS['Paper Types']['Smooth']['Dir Name'],
            "Wv": GENERAL_VARS['Paper Types']['Woven']['Dir Name'],  # Woven Folders
            "Woven": GENERAL_VARS['Paper Types']['Woven']['Dir Name'],
            "Tr": GENERAL_VARS['Paper Types']['Traditional']['Dir Name'],  # Traditional Folders
            "Traditional": GENERAL_VARS['Paper Types']['Traditional']['Dir Name']
        },
        'Size Dirs': {
            "Full": "Full/",  # Full Folders
            "Samp": "Sample/",
            "Sample": "Sample/",  # Sample Folders
        },
        "Repeats": {
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
        "Odds Dirs": {
            1: "Odd Panels/",
            0: "Even Panels/",
        },
        "Material Length": {  # Determines printable length. Rolls are ~150 feet, but 45 inches are lost for printer waste.
            "Smooth": (GENERAL_VARS['Paper Types']['Smooth']['Length']* 12 - GENERAL_VARS["Printer Waste"]),
            "Sm": (GENERAL_VARS['Paper Types']['Smooth']['Length']* 12 - GENERAL_VARS["Printer Waste"]),
            "Woven": (GENERAL_VARS['Paper Types']['Woven']['Length']* 12 - GENERAL_VARS["Printer Waste"]),
            "Wv": (GENERAL_VARS['Paper Types']['Woven']['Length']* 12 - GENERAL_VARS["Printer Waste"]),
            "Traditional": (GENERAL_VARS['Paper Types']['Traditional']['Length']* 12 - GENERAL_VARS["Printer Waste"]),
            "Tr": (GENERAL_VARS['Paper Types']['Traditional']['Length']* 12 - GENERAL_VARS["Printer Waste"]),
        },
        "Substrate": {
            "Smooth Peel and Stick": GENERAL_VARS['Paper Types']['Smooth']['Short Name'],
            "Smooth": GENERAL_VARS['Paper Types']['Smooth']['Short Name'],
            "Sm": GENERAL_VARS['Paper Types']['Smooth']['Name'],
            "Woven Peel and Stick": GENERAL_VARS['Paper Types']['Woven']['Short Name'],
            "Woven": GENERAL_VARS['Paper Types']['Woven']['Short Name'],
            "Wv": GENERAL_VARS['Paper Types']['Woven']['Name'],
            "Traditional": GENERAL_VARS['Paper Types']['Traditional']['Short Name'],
            "Tr": GENERAL_VARS['Paper Types']['Traditional']['Name']
        },
    },
    # Running count of PDFs that are referenced during sample creating. If a PDF is referenced more than once, the order and PDF are printed to alert fulfillment of dual-type samples
    'Count of Refd PDFs': (
        {}
    ),
    'PDFs to rename':{},
    'Order Items Dicts': {}
}

GENERAL_BLANK_DICTS_HIDDEN = {

}

BATCHING_VARS = {
    "Minimum Length": 0.8, #Minimum Batch Length as a percent
    "Sample Size": 9.5, # Size of a sample in inches
    "Height List": (
        9,
        40.25,
        52.25,
        64.25,
        76.25,
        88.25,
        100.25,
        112.25,
        124.25,
        136.25,
        146.25,
        ),
    "Priorities": {
        1: "OT",
        2: "Late",
        3: "Today",
        4: "Tomorrow",
        5: "Future"
    }, 
}

BATCHING_VARS_HIDDEN = {
    "Batch Content Options": {
        0: "Standard",
        1: "Full Panels Only",
        2: "Samples Only"
    },
    "Blank Panels": {
        "9.0": CALDERA_DIR + "z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Samp-Rp 2-Qty 1-BlankPdf Sample-L9.5-W25-H9.pdf",
        "40.25": CALDERA_DIR + "z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 3Foot-L40.75-W25-H40.25.pdf",
        "52.25": CALDERA_DIR + "z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 4Foot-L52.75-W25-H52.25.pdf",
        "64.25": CALDERA_DIR + "z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 5Foot-L64.75-W25-H64.25.pdf",
        "76.25": CALDERA_DIR + "z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 6Foot-L76.75-W25-H76.25.pdf",
        "88.25": CALDERA_DIR + "z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 7Foot-L88.75-W25-H88.25.pdf",
        "100.25": CALDERA_DIR + "z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 8Foot-L100.75-W25-H100.25.pdf",
        "112.25": CALDERA_DIR + "z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 9Foot-L112.75-W25-H112.25.pdf",
        "124.25": CALDERA_DIR + "z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 10Foot-L124.75-W25-H124.25.pdf",
        "136.25": CALDERA_DIR + "z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 11Foot-L136.75-W25-H136.25.pdf",
        "146.25": CALDERA_DIR + "z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 12Foot-L146.75-W25-H146.25.pdf",
    },
    "Utility Files": {
        "Color Guide": CALDERA_DIR
        + "z_Storage/assets/color guides/LvD Color Chart Rotated.pdf",
        "Roll Sticker": CALDERA_DIR
        + "z_Storage/assets/roll stickers/LvD Roll Stickers Rotated.pdf",
    }
}

DATABASE_VARS = {
    "Order Database": CALDERA_DIR + "z_Storage/z_WallpaperDB/lvdOrderDatabase.sqlite",
    "Batch Counter": CALDERA_DIR + "z_Storage/z_WallpaperDB/lvdGlobalBatchCounter.sqlite"
}


IMPORTER_VARS = {
    "Printers": {
        "1": ["Ichi", "1 Ichi/"],
        "2": ["Ni", "2 Ni/"],
        "3": ["San", "3 San/"],
        "4": ["Shi", "4 Shi/"], # This will always be skipped.
        "5": ["Go", "5 Go/"],
    },
    "Import Batch Lock Time": 20,
    "Compress Exported Batches": False,
}

IMPORTER_VARS_HIDDEN = {}


'''
Various Config Functions
'''

# Database Functions
orders_dict = SqliteDict(DATABASE_VARS["Order Database"], autocommit=True)
global_batch_counter = SqliteDict(DATABASE_VARS["Batch Counter"], autocommit=True)

def get_batch_id() -> int:
    """
    Accepts nothing. Returns a batch ID and increments Batch Counter by 1
    """
    current_ID = global_batch_counter['batchCounter']
    global_batch_counter['batchCounter'] += 1
    return current_ID


# Batch Dictionary Functions

def reset_available_pdfs() -> dict:
    """
    Sets available_pdfs to empty/default values.
    """

    available_pdfs = {
        "OT": {
            "full": {
                "batch_length": 0,
                "batch_list": [],
            },
            "sample": {
                "batch_length": 0,
                "batch_list": [],
            },
        },
        "Late": {
            "full": {
                "batch_length": 0,
                "batch_list": [],
            },
            "sample": {
                "batch_length": 0,
                "batch_list": [],
            },
        },
        "Today": {
            "full": {
                "batch_length": 0,
                "batch_list": [],
            },
            "sample": {
                "batch_length": 0,
                "batch_list": [],
            },
        },
        "Tomorrow": {
            "full": {
                "batch_length": 0,
                "batch_list": [],
            },
            "sample": {
                "batch_length": 0,
                "batch_list": [],
            },
        },
        "Future": {
            "full": {
                "batch_length": 0,
                "batch_list": [],
            },
            "sample": {
                "batch_length": 0,
                "batch_list": [],
            },
        },
    }
    return available_pdfs

def reset_batch_dict() -> dict:
    """
    Sets batch_dict to default/empty values.
    """

    batch_dict = {
        "batch_details": {
            "ID": "",
            "material": "",
            "priority": 0,
            "length": 2,
            "material_length": 0,
            "care_about_minimum_length": True,
            "include_OTs": False,
            "contents": 0,
            "color_guides": {
                "default": BATCHING_VARS_HIDDEN["Utility Files"]["Color Guide"],
                "unique_filename": "",
            },
            "roll_stickers": {
                "default": BATCHING_VARS_HIDDEN["Utility Files"]["Roll Sticker"],
                "unique_filename": "",
            },
        },
        "OT": {
            "full": {
                "batch_length": 0,
                "batch_list": [],
            },
            "sample": {
                "batch_length": 0,
                "batch_list": [],
            },
        },
        "Late": {
            "full": {
                "batch_length": 0,
                "batch_list": [],
            },
            "sample": {
                "batch_length": 0,
                "batch_list": [],
            },
        },
        "Today": {
            "full": {
                "batch_length": 0,
                "batch_list": [],
            },
            "sample": {
                "batch_length": 0,
                "batch_list": [],
            },
        },
        "Tomorrow": {
            "full": {
                "batch_length": 0,
                "batch_list": [],
            },
            "sample": {
                "batch_length": 0,
                "batch_list": [],
            },
        },
        "Future": {
            "full": {
                "batch_length": 0,
                "batch_list": [],
            },
            "sample": {
                "batch_length": 0,
                "batch_list": [],
            },
        },
    }
    return batch_dict
