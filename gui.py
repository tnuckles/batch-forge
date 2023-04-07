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
import getPdfData as get_pdf_data
import batch_builder_variables as bv

# Set Installation Directory. Don't actually know if I'll really need this.
installation_dir = '/Users/Trevor/Documents/Scripts/batch-forge/'

# Startup sorting copy tree just to make my life easier
# while testing and developing.
caldera_path = '/Users/Trevor/Documents/Scripts/Misc/caldera/var/public/'
try:
    shutil.rmtree(
        caldera_path + '3 Downloaded'
        )
    shutil.copytree(
        caldera_path + '3 Downloaded Copy',
        caldera_path + '3 Downloaded'
        )
except:
    pass

sort_results = []

# Initilize TK and main menu window
root = Tk()
app_image = Image(
    'photo',
    file=installation_dir + 'assets/batch_forge_icon.png'
    )
root.call('wm', 'iconphoto',  root._w,  app_image)
root.title('Batch Forge')
root.geometry('300x350')
root.minsize(300, 350)
root.maxsize(300, 350)


def get_sort_results() -> list:
    '''
    Accepts nothing. Returns a list containing the results of a sort function.
    '''

    results_list = []
    results_list.extend(reportListOfPdfs(
            missingPdfList,
            'missing PDF. Moved to needs Attention.'
            ))
    results_list.extend(reportListOfPdfs(
            damagedPdfList,
            'damaged PDF. Moved to Needs Attention.'
            ))
    results_list.extend(reportListOfPdfs(
            otPanelUknownList,
            'couldn\'t read OT panels. Moved to Needs Attention.'
            ))
    results_list.extend(reportListOfPdfs(
            splitPdfList,
            'split into multiple files.'
            ))
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
        width=250
        )
    progress_frame.pack(padx=10, pady=10)

    # This is a fun easter egg for me, but is otherwise worthless.
    if snort_label_count == 67:
        snort_label = Label(
            progress_frame,
            text=f'Now sorting {snort_label_count} orders.\n\n'
            'ALL HAIL SIXTY SEVEN\nTHE 19TH AND HOLIEST PRIME',
                )
    else:
        snort_label = Label(
            progress_frame,
            text=f'Now sorting {snort_label_count} orders.'
            )
    snort_label.pack(padx=10, pady=10)

    # Sets progress bar
    progress_bar = ttk.Progressbar(
        progress_frame,
        orient='horizontal',
        length=200,
        mode='determinate',
        )
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
                f'| Couldn\'t properly sort PDFs in {unzip_dir}'
                )

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
        results_frame = LabelFrame(
            window,
            text='Results',
            padx=5,
            pady=3,
            width=350
            )

        results_frame.pack(padx=10, pady=10)

        for result in sort_results:
            if 'Needs Attention' in result:
                result_label = Label(results_frame, text=result, fg='red')
                result_label.pack(anchor='w', padx=1, pady=5)
            else:
                result_label = Label(results_frame, text=result)
                result_label.pack(anchor='w', padx=1, pady=5)

        close_button = Button(
            window,
            text='Return to Main Menu',
            width=20,
            height=2,
            command=window.destroy
            )
        close_button.pack(padx=10, pady=10)


def batch_orders_window() -> None:
    '''
    Accepts nothing. Opens the window for batching orders.

    Warning: Still in development.
    '''

    # Initialize Batch Window
    batch_window = Toplevel(root)
    batch_window.title('Build-A-Batch')
    batch_window.minsize(300,350)

    # column_count = 1
    # new_label = Label(
    #     material_frame,
    #     text = 'Material:',
    #     )
    # new_label.grid(
    #     column=column_count,
    #     padx=2,
    #     pady=2
    #     )
    # column_count += 1
    # material_frame = Frame(
    #     batch_window,
    #     relief=RIDGE,
    # ).pack(side=LEFT)

    # Initialize frame that contains counts of different PDF heights
    panel_count_label = Frame(
        batch_window,
        padx=10,
        pady=10,
        relief=SUNKEN,
        bd=5,
    )
    panel_count_label.grid(column=0, row=0, rowspan=5)

    row_count = 1
    for height in bv.height_list:
        if height == 9:
            height = 'Samples'
        elif height == 146.25:
            height = '12\nFeet'
        else:
            height = str(int((height-4.25)/12)) + '\nFeet'
        height_label = Label(
            panel_count_label,
            text = (str(height)),
            )
        height_label.grid(
            row=row_count,
            column=0,
            padx=1,
            pady=1
            )
        row_count += 1

    column_count = 1
    column_count = display_pdf_counts(panel_count_label, 'Smooth', column_count)
    column_count = display_pdf_counts(panel_count_label, 'Woven', column_count)
    column_count = display_pdf_counts(panel_count_label, 'Traditional', column_count)

    '''
    Initialize Material Frame and Combobox
    '''
    material_frame = Frame(
        batch_window,
        padx=10,
        pady=10,
        bd=5,
        relief=SUNKEN,
    )
    material_frame.grid(column=1, row=0, sticky=EW)

    material_label = Label(
        material_frame,
        text='Please select a material:',
        justify=LEFT
    )
    material_label.grid(row=0, column=0)

    batch_material_var = StringVar().set(0)
    batch_material_combobox = ttk.Combobox(
        material_frame,
        state='readonly',
        textvariable=batch_material_var,
        width=8,
        values=('Smooth', 'Woven', 'Woven 2', 'Traditional'),
    )
    batch_material_combobox.current(0)
    batch_material_combobox.grid(row=0, column=1)
   

    '''
    Initialize Options Frame and Buttons
    '''
    # Frame
    options_frame = Frame(
        batch_window,
        padx=10,
        pady=10,
        bd=5,
        relief=SUNKEN,
    )
    options_frame.grid(column=1, row=2, sticky=EW)

    # Order Trouble Label and Checkbutton
    order_trouble_label = Label(
        options_frame,
        text='Include Order Troubles?',
        justify=LEFT
    )
    order_trouble_label.grid(row=0, column=0, sticky=W)

    batch_ot_var = BooleanVar().set(True)
    batch_ot_checkbutton = Checkbutton(options_frame, variable=batch_ot_var, onvalue=True, offvalue=False, justify=LEFT)
    batch_ot_checkbutton.select()
    batch_ot_checkbutton.grid(row=0, column=1, sticky=W)

    # Minimum Length Enforcement Label and Checkbutton
    batch_minimum_label = Label(
        options_frame,
        text='Enforce minimum length?',
        justify=LEFT
    )
    batch_minimum_label.grid(row=1, column=0, sticky=W)

    batch_minimum_var = BooleanVar().set(True)
    batch_minimum_checkbutton = Checkbutton(options_frame, variable=batch_minimum_var, onvalue=True, offvalue=False, justify=LEFT)
    batch_minimum_checkbutton.select()
    batch_minimum_checkbutton.grid(row=1, column=1, sticky=W)

    # Custom Length Label and Spinbox
    custom_length_label = Label(
        options_frame,
        text = 'Custom Length:',
        justify=LEFT
    )
    custom_length_label.grid(row=3, column=0, sticky=W)

    batch_length_var = IntVar()
    batch_length_spinbox = Spinbox(options_frame,
                                   width=3,
                                   from_=1,
                                   to=150,
                                   increment=1,
                                   textvariable=batch_length_var,
                                   state=DISABLED)
    batch_length_var.set(150)
    batch_length_spinbox.grid(row=3, column=1, sticky=W)

    # Custom Length Check Label and Checkbutton
    custom_length_check_label = Label(
        options_frame,
        text='Use Custom Length?',
        justify=LEFT
    )
    custom_length_check_label.grid(row=2, column=0, sticky=W)

    batch_min_var = BooleanVar()
    batch_min_checkbutton = Checkbutton(options_frame,
                                        variable=batch_min_var,
                                        offvalue=FALSE,
                                        onvalue=TRUE,
                                        justify=LEFT,
                                        command=lambda: batch_length_spinbox.config(state = checked(batch_min_var.get())))
    batch_min_checkbutton.grid(row=2, column=1, sticky=W)

    # Initialize Return Button
    batch_button_frame = Frame(
        batch_window,
        padx=5,
        pady=10,
        bd=5,
        relief=SUNKEN,
    )
    batch_button_frame.grid(row=3, column=1, sticky=EW)

    batch_button = Button(
        batch_button_frame,
        text='Batch!',
        width=20,
        height=2,
        command=batch_window.destroy
        )
    batch_button.pack()

    close_button_frame = Frame(
        batch_window,
        padx=5,
        pady=10,
        bd=5,
        relief=SUNKEN
    )
    close_button_frame.grid(row=4, column=1, sticky=EW)
    
    close_button = Button(
        close_button_frame,
        text='Return to Main Menu',
        width=20,
        height=1,
        command=batch_window.destroy
        )
    close_button.pack()

    return

def checked(value):
    if value == True:
        return NORMAL
    else:
        return DISABLED


def display_pdf_counts(frame, material, column) -> int:
    '''
    Accepts a frame name and material name. Displays counts of
    panels on screen, returns a row count for the succeeding rows.
    '''

    row_count = 0
    if row_count == 0:
        material_label = Label(
            frame,
            text = material
        )
        material_label.grid(column=column, row=row_count, padx=1, pady=1)
        row_count += 1
    for height in bv.height_list:
        height_count = Label(
            frame,
            text=(str(batch_get_qty_counts(material, height)))
            )
        height_count.grid(column=column, row = row_count, padx=1, pady=1, sticky=EW)
        row_count += 1
    column += 1
    return column


def batch_get_qty_counts(material, height) -> int:
    '''
    Accepts a material type and panel height, then uses glob to find and return
    an integer of the quantity.
    '''
    # If looking for a sample
    if height == 9:
        pdf_list = glob(sortingDir + '*/' + material + '/Sample/*.pdf')
        count = len(pdf_list)
        return count
    else:
        count = 0
        pdf_list = glob(sortingDir + '*/' + material + '/Full/*/*/*-Full-*H' + str(height) + '.pdf')
        for print_pdf in pdf_list:
            count += get_pdf_data.quantity(print_pdf)
        return count


def test_stats_bar():
    # Initialize Batch Window
    test_window = Toplevel(root)
    test_window.title('Build-A-Batch')

    # Initialize Return Button
    close_button = Button(
        test_window,
        text='Return to Main Menu',
        width=20,
        height=2,
        command=test_window.destroy
        )
    close_button.grid(row=0, padx=10, pady=10)

    status = Label(test_window, text='Test', relief=SUNKEN, bd=1)
    status.grid(row=1, sticky='EW')

    return



main_menu_frame = LabelFrame(
    root,
    text='Main Menu',
    padx=10,
    pady=10
    )

main_menu_frame.pack(padx=10, pady=10)

button_sort_orders = Button(
    main_menu_frame,
    text='Sort Orders',
    width=20,
    height=2,
    command=sort_zipped_packages_window
    ).pack()

button_batch_orders = Button(
    main_menu_frame,
    text='Build-A-Batch',
    width=20,
    height=2,
    command=batch_orders_window
    ).pack()

button_caldera_importer = Button(
    main_menu_frame,
    text='Caldera Importer',
    width=20,
    height=2,
    ).pack()

button_drive_downloader = Button(
    main_menu_frame,
    text='Download from Drive',
    width=20,
    height=2,
    command=test_stats_bar
    ).pack()

button_dates_update = Button(
    main_menu_frame,
    text='Update Sort for Due Dates',
    width=20,
    height=2,
    command=moveForDueDates
    ).pack()

button_quit = Button(
    main_menu_frame,
    text='Quit Batch Forge',
    width=20,
    height=2,
    command=root.quit
    ).pack()

root.mainloop()
