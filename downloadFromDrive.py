#!usr/bin/env python

from datetime import date
import get_pdf_data as getPdf
from glob import glob
import wallpaper_sorter_variables as gv
from wallpaper_sorter_functions import try_to_move_pdf

today = date.today()
