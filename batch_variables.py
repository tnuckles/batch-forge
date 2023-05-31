#!usr/bin/env python

import os
from datetime import date
from sqlitedict import SqliteDict
from wallpaper_sorter_variables import CALDERA_DIR

# Global Variables

MIN_LNGTH = 0.8  # minimum length as a percent

SAMPLE_SIZE = 9.5  # Size of a sample

height_list = (
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
)

PRIORITY_OPTIONS = ("OT", "Late", "Today", "Tomorrow", "Future")


PRINTER_WASTE_LENGTH = 45

"""
Removing these pesky headers
"""
# HEADER_DICT = {
#     'ot': CALDERA_DIR + 'z_Storage/assets/headers/999999999-headerOt.pdf',
#     'late': CALDERA_DIR + 'z_Storage/assets/headers/999999999-headerLate.pdf',
#     'today': CALDERA_DIR + 'z_Storage/assets/headers/999999999-headerToday.pdf',
#     'tomorrow': CALDERA_DIR + 'z_Storage/assets/headers/999999999-headerTomorrow.pdf',
#     'future': CALDERA_DIR + 'z_Storage/assets/headers/999999999-headerFuture.pdf',
# }


batch_content_options = ((0, "Standard"), (1, "Full Panels Only"), (2, "Samples Only"))

blank_panels = {
    "9.0": CALDERA_DIR
    + "z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Samp-Rp 2-Qty 1-BlankPdf Sample-L9.5-W25-H9.pdf",
    "40.25": CALDERA_DIR
    + "z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 3Foot-L40.75-W25-H40.25.pdf",
    "52.25": CALDERA_DIR
    + "z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 4Foot-L52.75-W25-H52.25.pdf",
    "64.25": CALDERA_DIR
    + "z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 5Foot-L64.75-W25-H64.25.pdf",
    "76.25": CALDERA_DIR
    + "z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 6Foot-L76.75-W25-H76.25.pdf",
    "88.25": CALDERA_DIR
    + "z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 7Foot-L88.75-W25-H88.25.pdf",
    "100.25": CALDERA_DIR
    + "z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 8Foot-L100.75-W25-H100.25.pdf",
    "112.25": CALDERA_DIR
    + "z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 9Foot-L112.75-W25-H112.25.pdf",
    "124.25": CALDERA_DIR
    + "z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 10Foot-L124.75-W25-H124.25.pdf",
    "136.25": CALDERA_DIR
    + "z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 11Foot-L136.75-W25-H136.25.pdf",
    "146.25": CALDERA_DIR
    + "z_Storage/assets/blank pdfs/999999999-1-(2022-01-01)-Stnd-Sm-Full-Rp 2-Qty 1-BlankPdf 12Foot-L146.75-W25-H146.25.pdf",
}

utility_files = {
    "color_guide": CALDERA_DIR
    + "z_Storage/assets/color guides/LvD Color Chart Rotated.pdf",
    "roll_sticker": CALDERA_DIR
    + "z_Storage/assets/roll stickers/LvD Roll Stickers Rotated.pdf",
}

order_db = CALDERA_DIR + "z_Storage/z_WallpaperDB/lvdOrderDatabase.sqlite"
orders_dict = SqliteDict(order_db, autocommit=True)
batch_counter_db = CALDERA_DIR + "z_Storage/z_WallpaperDB/lvdGlobalBatchCounter.sqlite"
global_batch_counter = SqliteDict(batch_counter_db, autocommit=True)
# global_batch_counter['batchCounter'] = 1


def get_batch_id() -> int:
    """
    Returns batch ID and increments batchCounter by 1
    """
    currentID = global_batch_counter["batchCounter"]
    global_batch_counter["batchCounter"] += 1
    return currentID


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
                "default": utility_files["color_guide"],
                "unique_filename": "",
            },
            "roll_stickers": {
                "default": utility_files["roll_sticker"],
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
