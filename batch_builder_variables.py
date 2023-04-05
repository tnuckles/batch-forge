#!usr/bin/env python

import os
from datetime import date
from sqlitedict import SqliteDict
from wallpaperSorterVariables import getHeader, getUtilityFiles

# Global Variables

min_length = 0.8  # minimum length as a percent

height_list = (9,
               40.25,
               52.25,
               64.25,
               76.25,
               88.25,
               100.25,
               112.25,
               124.25,
               136.25,
               146.25
               )

currentBatchDict = {
        'batchDetails':  {
            'ID': '',
            'material': '',
            'priority': 0,
            'length': 2,
            'materialLength': 0,
            'careAboutminLength': True,
            'includeOTs': False,
            'colorGuides': {
                'default': getUtilityFiles['colorGuide'],
                'uniqueFilename': ''
            },
            'rollStickers': {
                'default': getUtilityFiles['rollSticker'],
                'uniqueFilename': ''
            },
        },
        'OT': {
            'full': {
                'batchLength': 0,
                'batchList': [],
                'header': getHeader['ot']
            },
            'sample': {
                'batchLength': 0,
                'batchList': [],
                'header': getHeader['ot']
            },
            'header': '',
        },
        'Late': {
            'full': {
                'batchLength': 0,
                'batchList': [],
                'header': getHeader['late']
            },
            'sample': {
                'batchLength': 0,
                'batchList': [],
                'header': getHeader['late']
            },
            'header': '',
        },
        'Today': {
            'full': {
                'batchLength': 0,
                'batchList': [],
                'header': getHeader['today']
            },
            'sample': {
                'batchLength': 0,
                'batchList': [],
                'header': getHeader['today']
            },
            'header': '',
        },
        'Tomorrow': {
            'full': {
                'batchLength': 0,
                'batchList': [],
                'header': getHeader['tomorrow']
            },
            'sample': {
                'batchLength': 0,
                'batchList': [],
                'header': getHeader['tomorrow']
            },
            'header': '',
        },
        'Future': {
            'full': {
                'batchLength': 0,
                'batchList': [],
                'header': getHeader['future']
            },
            'sample': {
                'batchLength': 0,
                'batchList': [],
                'header': getHeader['future']
            },
            'header': '',
        },
    }

availablePdfs = {
        'OT': {
            'full': {
                'batchLength': 0,
                'batchList': [],
            },
            'sample': {
                'batchLength': 0,
                'batchList': [],
            },
        },
        'Late': {
            'full': {
                'batchLength': 0,
                'batchList': [],
            },
            'sample': {
                'batchLength': 0,
                'batchList': [],
            },
        },
        'Today': {
            'full': {
                'batchLength': 0,
                'batchList': [],
            },
            'sample': {
                'batchLength': 0,
                'batchList': [],
            },
        },
        'Tomorrow': {
            'full': {
                'batchLength': 0,
                'batchList': [],
            },
            'sample': {
                'batchLength': 0,
                'batchList': [],
            },
        },
        'Future': {
            'full': {
                'batchLength': 0,
                'batchList': [],
            },
            'sample': {
                'batchLength': 0,
                'batchList': [],
            },
        },
    }
