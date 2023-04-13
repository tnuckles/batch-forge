# /Users/Trevor/Documents/Scripts/batch-forge python
# UI Script for Batch Forge

import json
import shutil
import zipfile as zf
from glob import glob
from tkinter import *
from tkinter import ttk

from wallpaperSorterFunctions import (checkForMultiQtySamplePdfs,
                                      cleanupDownloadDir, damagedPdfList,
                                      missingPdfList, moveForDueDates,
                                      otPanelUknownList, parseJSON,
                                      reportListOfPdfs,
                                      sortPackagesByOrderNumber,
                                      sortPdfsToSortedFolders,
                                      splitMultiPagePDFs, splitPdfList)
from wallpaperSorterVariables import downloadDir, sortingDir
from batch_sorting import *
import getPdfData as get_pdf_data
import batch_builder_variables as bv
from math import floor

# Set Installation Directory. Don't actually know if I'll really need this.
installation_dir = '/Users/Trevor/Documents/Scripts/batch-forge/'

# Startup sorting copy tree just to make my life easier
# while testing and developing.
caldera_path = '/Users/Trevor/Documents/Scripts/Misc/caldera/var/public/'
try:
    shutil.rmtree(caldera_path + '3 Downloaded')
    shutil.copytree(caldera_path + '3 Downloaded Copy',
                    caldera_path + '3 Downloaded')
except:
    pass

sort_results = []

# Initilize TK and main menu window
root = Tk()
app_image = Image(
    'photo',
    file=installation_dir + 'assets/batch_forge_icon.png')
root.call('wm', 'iconphoto',  root._w,  app_image)
root.title('Batch Forge')
root.geometry('300x350')
root.minsize(300, 350)
root.maxsize(300, 350)


def get_sort_results() -> list:
    '''
    Accepts nothing. Returns a list containing the results of a sort function.
    '''
    result_msg_dict = {
        'missing': 'missing PDF. Moved to needs Attention.',
        'damaged': 'damaged PDF. Moved to Needs Attention.',
        'illegible': 'couldn\'t read OT panels. Moved to Needs Attention.',
        'split': 'split into multiple files.'}

    results_list = []
    results_list.extend(reportListOfPdfs(missingPdfList,
                                         result_msg_dict['missing']))
    results_list.extend(reportListOfPdfs(damagedPdfList,
                                         result_msg_dict['damaged']))
    results_list.extend(reportListOfPdfs(otPanelUknownList,
                                         result_msg_dict['illegible']))
    results_list.extend(reportListOfPdfs(splitPdfList,
                                         result_msg_dict['split']))
    return results_list


def sort_zipped_packages_window() -> None:
    '''
    Accepts nothing and returns nothing. Opens a window with a progress
    bar to monitor the unzipping and renaming of downloaded sort files.

    When done, cleans out the Downloads folder as well to keep things
    clean. If there are any results for the function, it will display
    them and wait for the user to close the window. Otherwise,
    automatically returns to the main menu.
    '''
    # Initialize sort window
    window = Toplevel(root)
    window.title('Sort')
    zippedPackages = sortPackagesByOrderNumber(glob(downloadDir + '*.zip'))
    snort_label_count = len(zippedPackages)
    progress_frame = LabelFrame(
        window,
        text='Progress',
        padx=10,
        pady=10,
        width=250)
    progress_frame.pack(padx=10, pady=10)

    # This is a fun easter egg for me, but is otherwise worthless.
    if snort_label_count == 67:
        snort_label = Label(progress_frame,
                            text=f'Now sorting {snort_label_count} orders.\n\n'
                            'ALL HAIL SIXTY SEVEN\nTHE 19TH AND HOLIEST PRIME')
    else:
        snort_label = Label(
            progress_frame,
            text=f'Now sorting {snort_label_count} orders.')
    snort_label.pack(padx=10, pady=10)

    # Sets progress bar
    progress_bar = ttk.Progressbar(
        progress_frame,
        orient='horizontal',
        length=200,
        mode='determinate')
    progress_bar.pack(pady=10, padx=20)

    # Sets status label
    status_label = Label(progress_frame, text='Working...')
    status_label.pack()

    progress_bar['maximum'] = snort_label_count

    # Begins unzipping, renaming, and sorting files
    for package in zippedPackages:
        status_label.config(text=package.split('/')[-1])
        try:
            package_name = package.split('/')[-1].split('_')[0]
            unzip_dir = downloadDir + (package_name) + '/'
            with zf.ZipFile(package, 'r') as zip_ref:
                zip_ref.extractall(unzip_dir)
        except:
            unzip_error_label = Label(f'| Couldn\'t unzip file: {package}')
            unzip_error_label.pack(padx=5, pady=5)
        orderJSON = str(glob(unzip_dir + '*.json')).split('\'')[1]
        with open(orderJSON) as file:
            openJSON = json.load(file)
        parseJSON(openJSON, orderJSON, unzip_dir)
        splitMultiPagePDFs(glob(unzip_dir + '*.pdf'))
        checkForMultiQtySamplePdfs(glob(unzip_dir + '*-Samp-*.pdf'))
        try:
            sortPdfsToSortedFolders(glob(unzip_dir + '*.pdf'))
        except:
            sort_results.append(
                f'| Couldn\'t properly sort PDFs in {unzip_dir}')

        progress_bar['value'] += 1
        progress_frame.update_idletasks()

    # Updates label
    status_label.config(text='Done!')
    snort_label.config(text=f'Sorted {snort_label_count} orders.')

    # Cleans out download directory of unneeded directories and folders
    cleanupDownloadDir(downloadDir)

    # Displays sort results if any exist;
    # otherwise, closes window and returns to main menu
    sort_results = get_sort_results()

    if len(sort_results) == 0:
        window.destroy()
    else:
        results_frame = LabelFrame(window,
                                   text='Results',
                                   padx=5,
                                   pady=3,
                                   width=350)
        results_frame.pack(padx=10, pady=10)

        for result in sort_results:
            if 'Needs Attention' in result:
                result_label = Label(results_frame, text=result, fg='red')
                result_label.pack(anchor='w', padx=1, pady=5)
            else:
                result_label = Label(results_frame, text=result)
                result_label.pack(anchor='w', padx=1, pady=5)

        close_btn = Button(window,
                           text='Return to Main Menu',
                           width=20,
                           height=2,
                           command=window.destroy)
        close_btn.pack(padx=10, pady=10)


def batch_orders_window() -> None:
    '''
    Accepts nothing. Opens the window for batching orders.
    '''

    # Initialize Batch Window
    batch_window = Toplevel(root)
    batch_window.title('Build-A-Batch')
    batch_window.minsize(300, 350)

    # Initialize frame that contains counts of different PDF heights
    panel_count_label = Frame(batch_window,
                              padx=10,
                              pady=10,
                              relief=SUNKEN,
                              bd=5)
    panel_count_label.grid(column=0, row=0, rowspan=4)

    row_count = 1
    for height in bv.height_list:
        if height == 9:
            height = 'Samples'
        elif height == 146.25:
            height = '12\nFeet'
        else:
            height = str(int((height-4.25)/12)) + '\nFeet'
        height_label = Label(panel_count_label,
                             text=(str(height)))
        height_label.grid(row=row_count,
                          column=0,
                          padx=1,
                          pady=1)
        row_count += 1

    column_count = 1
    material_type = ('Smooth', 'Woven', 'Traditional')
    for paper in material_type:
        column_count = display_pdf_counts(panel_count_label,
                                          paper,
                                          column_count)

    '''
    Initialize Options Frame and Widgets
    '''
    # Options Frame
    options_frame = Frame(
        batch_window,
        padx=10,
        pady=10,
        bd=5,
        relief=SUNKEN)
    options_frame.grid(column=1, row=0, sticky=EW)

    # Material Selection
    material_label = Label(options_frame,
                           text='Please select a material:',
                           justify=LEFT)
    material_label.grid(row=0, column=0)

    global batch_material_var
    batch_material_var = StringVar()

    material_list = ('Smooth', 'Woven', 'Woven 2', 'Traditional')
    material_row_count = 0
    for material in material_list:
        material_btn = Radiobutton(options_frame,
                                   variable=batch_material_var,
                                   value=material,
                                   text=material,
                                   command=lambda: update_batch_specs())
        material_btn.grid(row=material_row_count, column=1, sticky=W)
        material_row_count += 1

    batch_material_var.set('Smooth')

    # Include Samples Label and Checkbutton
    sample_label = Label(options_frame,
                         text='Include Samples?',
                         justify=LEFT)
    sample_label.grid(row=4, column=0, sticky=W)

    include_samples_var = BooleanVar()
    include_samples_var.set(True)
    include_samples_checkbutton = Checkbutton(options_frame,
                                              variable=include_samples_var,
                                              onvalue=True,
                                              offvalue=False,
                                              justify=LEFT,
                                              command=lambda: update_batch_specs())
    include_samples_checkbutton.select()
    include_samples_checkbutton.grid(row=4, column=1, sticky=W)

    # Order Trouble Label and Checkbutton
    order_trouble_label = Label(options_frame,
                                text='Include Order Troubles?',
                                justify=LEFT)
    order_trouble_label.grid(row=5, column=0, sticky=W)

    global batch_ot_var
    batch_ot_var = BooleanVar()
    batch_ot_var.set(True)
    batch_ot_checkbutton = Checkbutton(options_frame,
                                       variable=batch_ot_var,
                                       onvalue=True,
                                       offvalue=False,
                                       justify=LEFT,
                                       command=lambda: update_batch_specs())
    batch_ot_checkbutton.select()
    batch_ot_checkbutton.grid(row=5, column=1, sticky=W)

    # Minimum Length Enforcement Label and Checkbutton
    '''Currently Disabled'''
    batch_minimum_label = Label(
        options_frame,
        text='Enforce minimum length?',
        justify=LEFT)
    batch_minimum_label.grid(row=6, column=0, sticky=W)

    batch_minimum_var = BooleanVar().set(True)
    batch_minimum_checkbutton = Checkbutton(options_frame,
                                            variable=batch_minimum_var,
                                            onvalue=True,
                                            offvalue=False,
                                            justify=LEFT,
                                            state=DISABLED)
    batch_minimum_checkbutton.select()
    batch_minimum_checkbutton.grid(row=6, column=1, sticky=W)

    # Length Label, Spinbox, and Reset Button
    length_label = Label(
        options_frame,
        text='Batch Length:',
        justify=LEFT)
    length_label.grid(row=7, column=0, sticky=W)

    global batch_length_var
    batch_length_var = IntVar()
    batch_length_spinbox = Spinbox(options_frame,
                                   width=5,
                                   from_=10,
                                   to=150,
                                   increment=1,
                                   textvariable=batch_length_var,
                                   command=lambda: update_batch_specs())
    batch_length_var.set(150)
    batch_length_spinbox.grid(row=7, column=1, sticky=W)

    length_reset_btn = Button(options_frame,
                              text='Reset',
                              command=lambda: update_batch_specs(reset_length=True))
    length_reset_btn.grid(row=7, column=2)

    # Number of batches with these specifications
    available_batch_label = Label(options_frame,
                                  text='Available batches:',
                                  justify=LEFT)
    available_batch_label.grid(row=8,
                               column=0,
                               sticky=W)

    global batch_qty_label
    batch_qty_label = Label(options_frame,
                            justify=LEFT,
                            text=str(get_batch_cnt(batch_material_var.get(),
                                                   batch_length_var.get(),
                                                   batch_ot_var.get())))
    batch_qty_label.grid(row=8, column=1, sticky=W)

    # Number of batches to make with current specifications
    batch_quantity_label = Label(options_frame,
                                 text='Batches to make:',
                                 justify=LEFT)

    batch_quantity_label.grid(row=9,
                              column=0,
                              sticky=W)

    global batch_quantity_var
    global batch_quantity_spinbox
    batch_quantity_var = IntVar()
    batch_quantity_spinbox = Spinbox(options_frame,
                                     width=5,
                                     from_=0,
                                     textvariable=batch_quantity_var,
                                     increment=1,
                                     to=get_batch_cnt(batch_material_var.get(),
                                                      batch_length_var.get(),
                                                      batch_ot_var.get()))

    batch_quantity_var.set(default_batch_quantity(batch_material_var.get(),
                                                  batch_length_var.get(),
                                                  batch_ot_var.get()))

    batch_quantity_spinbox.grid(row=9, column=1, sticky=W)

    # Initialize Batch Button
    batch_btn_frame = Frame(
        batch_window,
        padx=5,
        pady=10,
        bd=5,
        relief=SUNKEN)
    batch_btn_frame.grid(row=1, column=1, sticky=EW)

    batch_btn = Button(
        batch_btn_frame,
        text='Batch!',
        width=20,
        height=2,
        command=lambda: reopen_window(batch_window))
    batch_btn.pack()

    # Initialize Batch Progress Bar
    batch_progress_frame = Frame(
        batch_window,
        padx=5,
        pady=10,
        bd=5,
        relief=SUNKEN)
    batch_progress_frame.grid(row=2, column=1, sticky=EW)

    batch_progress_label = Label(
        batch_progress_frame,
        text='Test.',
        padx=2)
    batch_progress_label.pack()

    progress_bar = ttk.Progressbar(
        batch_progress_frame,
        orient='horizontal',
        length=200,
        mode='determinate')
    progress_bar.pack()

    progress_bar['maximum'] = 100000
    while progress_bar['value'] > progress_bar['maximum']:
        progress_bar['value'] += 1
        batch_progress_frame.update_idletasks()

    # Initialize Return Button
    close_btn_frame = Frame(
        batch_window,
        padx=5,
        pady=10,
        bd=5,
        relief=SUNKEN)
    close_btn_frame.grid(row=4, column=0, columnspan=2, sticky=EW)

    close_btn = Button(
        close_btn_frame,
        text='Return to Main Menu',
        width=20,
        height=2,
        command=batch_window.destroy)
    close_btn.pack()

    return


def button_state_check(value: bool):
    '''
    Accepts a true/false and returns Normal/Disabled for button configurations.
    '''
    if value is True:
        return NORMAL
    else:
        return DISABLED


def get_batch_cnt(material: StringVar,
                  batch_length: int,
                  ot_status: bool) -> int:
    '''
    Accepts a material, batch_length, and OT inclusiong as a bool. Calls
    length_of_available_full_pdfs and returns a specific value as an int.
    '''

    batch_count = length_of_available_full_pdfs(material,
                                                batch_length,
                                                include_OT=ot_status)[1]
    return batch_count


def reopen_window(window) -> None:
    '''
    Accepts a window name. Closes and reopens that window when called.
    '''
    window.destroy()
    batch_orders_window()
    return


def default_batch_quantity(material: str,
                           batch_length: int,
                           include_OT: bool) -> int:
    '''
    Accepts material as a string, batch_length as an int, and whether or not
    to include OTs as a bool.
    When the batch window is open, sets the default batch quantity to 3 if more
    than 3 batches are available, or to the number of batches available if
    less than 3 are available.
    '''
    batch_count = get_batch_cnt(material, batch_length, include_OT)
    if batch_count >= 3:
        return 3
    else:
        return batch_count


def update_batch_specs(reset_length=False) -> None:
    '''
    Single function to call to update all other options based on related
    options changes. Optionally accepts a True/False value to reset the
    default batch length.
    '''
    if reset_length is True:
        batch_length_var.set(150)

    material = batch_material_var.get()
    batch_length = batch_length_var.get()
    include_OT = batch_ot_var.get()

    available_batches = get_batch_cnt(material,
                                      batch_length,
                                      include_OT)

    default_batches_to_make = default_batch_quantity(material,
                                                     batch_length,
                                                     include_OT)

    batch_qty_label.config(text=str(available_batches))
    batch_quantity_spinbox.config(textvariable=default_batches_to_make,
                                  to=available_batches)

    return


def length_of_available_full_pdfs(material: str,
                                  batch_length: int,
                                  include_OT=True) -> int:
    '''
    Accepts a material type as a string, batch_length as an integer, and
    include_OT as a boolean. Returns the length of all available PDFs for a
    given papertype.
    '''
    sort_dir_path = caldera_path + '5 Sorted for Print/'

    batch_length = batch_length * 12  # Change batch length from feet to inches

    list_to_calculate = []

    if include_OT is True:
        ot_full_path = sort_dir_path + '1 - OT/' + material + '/Full/'
        ot_full_list = glob(ot_full_path + '**/*.pdf', recursive=True)
        list_to_calculate.extend(ot_full_list)
    late_full_path = sort_dir_path + '2 - Late/' + material + '/Full/'
    late_full_list = glob(late_full_path + '**/*.pdf', recursive=True)
    list_to_calculate.extend(late_full_list)
    today_full_path = sort_dir_path + '3 - Today/' + material + '/Full/'
    today_full_list = glob(today_full_path + '**/*.pdf', recursive=True)
    list_to_calculate.extend(today_full_list)
    tomorrow_full_path = sort_dir_path + '4 - Tomorrow/' + material + '/Full/'
    tomorrow_full_list = glob(tomorrow_full_path + '**/*.pdf', recursive=True)
    list_to_calculate.extend(tomorrow_full_list)
    future_full_path = sort_dir_path + '5 - Future/' + material + '/Full/'
    future_full_list = glob(future_full_path + '**/*.pdf', recursive=True)
    list_to_calculate.extend(future_full_list)

    potential_length = calculate_full_length(sort_pdf_list(list_to_calculate))

    potential_batch_count = floor(potential_length / batch_length)

    return potential_length, potential_batch_count


def display_pdf_counts(frame, material, column) -> int:
    '''
    Accepts a frame name and material name. Displays counts of
    panels on screen, returns a row count for the succeeding rows.
    '''

    row_count = 0
    if row_count == 0:
        material_label = Label(frame,
                               text=material)
        material_label.grid(column=column, row=row_count, padx=1, pady=1)
        row_count += 1
    for height in bv.height_list:
        height_count = Label(
            frame,
            text=(str(batch_get_qty_counts(material, height))))
        height_count.grid(column=column,
                          row=row_count,
                          padx=1,
                          pady=1,
                          sticky=EW)
        row_count += 1
    column += 1
    return column


def batch_get_qty_counts(material, height) -> int:
    '''
    Accepts a material type and panel height, then uses glob to find and return
    an integer of the quantity.
    '''

    # Change height to ht for readability below
    ht = height

    # Specify first part of glob path
    mtrl_path = sortingDir + '*/' + material + '/'

    # If looking for a sample
    if height == 9:
        pdf_list = glob(mtrl_path + 'Sample/*.pdf')
        count = len(pdf_list)
        return count
    else:
        count = 0
        pdf_list = glob(mtrl_path + 'Full/*/*/*-Full-*H' + str(ht) + '.pdf')
        for print_pdf in pdf_list:
            count += get_pdf_data.quantity(print_pdf)
        return count


main_menu_frame = LabelFrame(root,
                             text='Main Menu',
                             padx=10,
                             pady=10)

main_menu_frame.pack(padx=10, pady=10)

button_sort_orders = Button(main_menu_frame,
                            text='Sort Orders',
                            width=20,
                            height=2,
                            command=sort_zipped_packages_window).pack()

button_batch_orders = Button(main_menu_frame,
                             text='Build-A-Batch',
                             width=20,
                             height=2,
                             command=batch_orders_window).pack()

button_caldera_importer = Button(main_menu_frame,
                                 text='Caldera Importer',
                                 width=20,
                                 height=2).pack()

button_drive_downloader = Button(main_menu_frame,
                                 text='Download from Drive',
                                 width=20,
                                 height=2).pack()

button_dates_update = Button(main_menu_frame,
                             text='Update Sort for Due Dates',
                             width=20,
                             height=2,
                             command=moveForDueDates).pack()

button_quit = Button(main_menu_frame,
                     text='Quit Batch Forge',
                     width=20,
                     height=2,
                     command=root.quit).pack()

root.mainloop()
