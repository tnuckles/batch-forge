#!usr/bin/env python

import os
from datetime import date
from sqlitedict import SqliteDict
from wallpaper_sorter_variables import caldera_dir

# Global Variables

standard_min_length = 0.8  # minimum length as a percent

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

batch_content_options = (
    (0, 'Standard'),
    (1, 'Full Panels Only'),
    (2, 'Samples Only')
)

utility_files = {
    'color_guide': caldera_dir + 'z_Storage/assets/color guides/LvD Color Chart Rotated.pdf',
    'roll_sticker': caldera_dir + 'z_Storage/assets/roll stickers/LvD Roll Stickers Rotated.pdf',
}

order_db = caldera_dir + 'z_Storage/z_WallpaperDB/lvdOrderDatabase.sqlite'
orders_dict = SqliteDict(order_db, autocommit=True)
batch_counter_db = caldera_dir + 'z_Storage/z_WallpaperDB/lvdGlobalBatchCounter.sqlite'
global_batch_counter = SqliteDict(batch_counter_db, autocommit=True)
global_batch_counter['batchCounter'] = 1

def get_batch_id() -> int:
    '''
    Returns batch ID and increments batchCounter by 1
    '''
    currentID = global_batch_counter['batchCounter']
    global_batch_counter['batchCounter'] += 1
    return currentID


def reset_available_pdfs():
    '''
    Sets available_pdfs to empty/default values.
    '''

    available_pdfs = {
            'OT': {
                'full': {
                    'batch_length': 0,
                    'batch_list': [],
                },
                'sample': {
                    'batch_length': 0,
                    'batch_list': [],
                },
            },
            'late': {
                'full': {
                    'batch_length': 0,
                    'batch_list': [],
                },
                'sample': {
                    'batch_length': 0,
                    'batch_list': [],
                },
            },
            'today': {
                'full': {
                    'batch_length': 0,
                    'batch_list': [],
                },
                'sample': {
                    'batch_length': 0,
                    'batch_list': [],
                },
            },
            'tomorrow': {
                'full': {
                    'batch_length': 0,
                    'batch_list': [],
                },
                'sample': {
                    'batch_length': 0,
                    'batch_list': [],
                },
            },
            'future': {
                'full': {
                    'batch_length': 0,
                    'batch_list': [],
                },
                'sample': {
                    'batch_length': 0,
                    'batch_list': [],
                },
            },
        }
    return available_pdfs


def reset_batch_dict() -> dict:
    '''
    Sets batch_dict to default/empty values.
    '''

    batch_dict = {
        'batch_details': {
            'ID':'',
            'material':'',
            'priority':0,
            'length':2,
            'material_length':0,
            'care_about_minimum_length':True,
            'include_OTs':False,
            'contents': 0,
            'color_guides':{
                'default':utility_files['color_guide'],
                'uniqure_filename':''
            },
            'roll_stickers':{
                'default':utility_files['roll_sticker'],
                'uniqure_filename':''
            },
        },
        'ot':{
            'full':{
                'batch_length':0,
                'batch_list':[],
            },
            'sample':{
                'batch_length':0,
                'batch_list':[],
            },
        },
        'late':{
            'full':{
                'batch_length':0,
                'batch_list':[],
            },
            'sample':{
                'batch_length':0,
                'batch_list':[],
            },
        },
        'today':{
            'full':{
                'batch_length':0,
                'batch_list':[],
            },
            'sample':{
                'batch_length':0,
                'batch_list':[],
            },
        },
        'tomorrow':{
            'full':{
                'batch_length':0,
                'batch_list':[],
            },
            'sample':{
                'batch_length':0,
                'batch_list':[],
            },
        },
        'future':{
            'full':{
                'batch_length':0,
                'batch_list':[],
            },
            'sample':{
                'batch_length':0,
                'batch_list':[],
            },
        },
    }
    return batch_dict
