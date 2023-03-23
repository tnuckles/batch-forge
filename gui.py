# /Users/Trevor/Documents/Scripts/batch-forge python
# UI Script for Batch Forge

import shutil
import zipfile as zf
from tkinter import *
from tkinter import ttk
from glob import glob
import json

from wallpaperSorterFunctions import *
import wallpaperSorterVariables as gv

installation_dir = '/Users/Trevor/Documents/Scripts/batch-forge/'
try:
    shutil.rmtree('/Volumes/Samsung SSD/caldera/var/public/3 Downloaded')
    shutil.copytree('/Volumes/Samsung SSD/caldera/var/public/3 Downloaded Copy',
                    '/Volumes/Samsung SSD/caldera/var/public/3 Downloaded')
except:
    pass

sort_results = []

root = Tk()
app_image = Image('photo', file=installation_dir + 'assets/batch_forge_icon.png')
root.call('wm', 'iconphoto',  root._w,  app_image)
root.title('Batch Forge')
root.geometry('300x350')
root.minsize(300, 350)
root.maxsize(300, 350)


def sort_zipped_packages_window():
    window = Toplevel(root)
    window.title('Sort')
    zippedPackages = sortPackagesByOrderNumber(glob(gv.downloadDir + '*.zip'))
    snort_label_count = len(zippedPackages)
    progress_frame = LabelFrame(window, text='Progress', padx=10, pady=10, width=250)
    progress_frame.pack(padx=10, pady=10)

    if snort_label_count == 67:
        snort_label = Label(progress_frame, text=f'Now sorting {snort_label_count} orders.\n\n'
                            'ALL HAIL SIXTY SEVEN\nTHE 19TH AND HOLIEST PRIME')
    else:
        snort_label = Label(progress_frame, text=f'Now sorting {snort_label_count} orders.')
    snort_label.pack(padx=10, pady=10)
    progress_bar = ttk.Progressbar(progress_frame, orient='horizontal', length=200, mode='determinate', )
    progress_bar.pack(pady=10, padx=20)

    status_label = Label(progress_frame, text='Working...')
    status_label.pack()

    progress_bar['maximum'] = snort_label_count

    for package in zippedPackages:
        status_label.config(text=package.split('/')[-1])
        try:
            fileToUnzipTo = gv.downloadDir + (package.split('/')[-1].split('_')[0]) + '/'
            with zf.ZipFile(package, 'r') as zip_ref:
                zip_ref.extractall(fileToUnzipTo)
        except:
            unzip_error_label = Label(f'| Couldn\'t unzip file: {package}')
            unzip_error_label.pack(padx=5, pady=5)
        orderJSON = str(glob(fileToUnzipTo + '*.json')).split('\'')[1]
        with open(orderJSON) as file:
            openJSON = json.load(file)
        parseJSON(openJSON, orderJSON, fileToUnzipTo)
        splitMultiPagePDFs(glob(fileToUnzipTo + '*.pdf'))
        checkForMultiQtySamplePdfs(glob(fileToUnzipTo + '*-Samp-*.pdf'))
        try:
            sortPdfsToSortedFolders(glob(fileToUnzipTo + '*.pdf'))
        except:
            sort_results.append((f'| Couldn\'t properly sort PDFs in {fileToUnzipTo}'))

        progress_bar['value'] += 1
        progress_frame.update_idletasks()

    status_label.config(text='Done!')
    snort_label.config(text=f'Sorted {snort_label_count} orders.')

    cleanupDownloadDir(gv.downloadDir)

    for i in range(10):
        sort_results.append(i)

    if len(sort_results) == 0:
        window.destroy()
    else:
        results_frame = LabelFrame(window, text='Results', padx=10, pady=10, width=250)
        results_frame.pack(padx=10, pady=10)
        for result in sort_results:
            result_label = Label(results_frame, text=result)
            result_label.pack(padx=2, pady=5)

        close_button = Button(window, text='Return to Main Menu', width=20, height=2, command=window.destroy)
        close_button.pack(padx=10, pady=10)


main_menu_frame = LabelFrame(root, text='Main Menu', padx=10, pady=10)
main_menu_frame.pack(padx=10, pady=10)

button_sort_orders = Button(main_menu_frame, text='Sort Orders', width=20, height=2, command=sort_zipped_packages_window)
button_batch_orders = Button(main_menu_frame, text='Build-A-Batch', width=20, height=2,)
button_caldera_importer = Button(main_menu_frame, text='Caldera Importer', width=20, height=2,)
button_drive_downloader = Button(main_menu_frame, text='Download from Drive', width=20, height=2,)
button_dates_update = Button(main_menu_frame, text='Update Sort for Due Dates', width=20, height=2, command=moveForDueDates)
button_quit = Button(main_menu_frame, text='Quit Batch Forge', width=20, height=2, command=root.quit)

button_sort_orders.pack()
button_batch_orders.pack()
button_caldera_importer.pack()
button_drive_downloader.pack()
button_dates_update.pack()
button_quit.pack()

root.mainloop()
