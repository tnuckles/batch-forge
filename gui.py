# /Users/Trevor/Documents/Scripts/batch-forge python
# UI Script for Batch Forge

import json
import shutil
import zipfile as zf
from glob import glob
from tkinter import *
from tkinter import ttk

<<<<<<< HEAD
from wallpaperSorterFunctions import (checkForMultiQtySamplePdfs,
                                      cleanupDownloadDir, damagedPdfList,
                                      missingPdfList, moveForDueDates,
                                      otPanelUknownList, parseJSON,
                                      reportListOfPdfs,
                                      sortPackagesByOrderNumber,
                                      sortPdfsToSortedFolders,
                                      splitMultiPagePDFs, splitPdfList)
from wallpaperSorterVariables import downloadDir
=======
from wallpaperSorterFunctions import *
import wallpaperSorterVariables as gv
>>>>>>> displaying_results

installation_dir = '/Users/Trevor/Documents/Scripts/batch-forge/'
try:
    shutil.rmtree('/Volumes/Samsung SSD/caldera/var/public/3 Downloaded')
<<<<<<< HEAD
    shutil.copytree(
        '/Volumes/Samsung SSD/caldera/var/public/3 Downloaded Copy',
        '/Volumes/Samsung SSD/caldera/var/public/3 Downloaded'
        )
=======
    shutil.copytree('/Volumes/Samsung SSD/caldera/var/public/3 Downloaded Copy',
                    '/Volumes/Samsung SSD/caldera/var/public/3 Downloaded')
>>>>>>> displaying_results
except:
    pass

sort_results = []

root = Tk()
<<<<<<< HEAD
app_image = Image(
    'photo',
    file=installation_dir + 'assets/batch_forge_icon.png'
    )
=======
app_image = Image('photo', file=installation_dir + 'assets/batch_forge_icon.png')
>>>>>>> displaying_results
root.call('wm', 'iconphoto',  root._w,  app_image)
root.title('Batch Forge')
root.geometry('300x350')
root.minsize(300, 350)
root.maxsize(300, 350)

<<<<<<< HEAD
def get_sort_results():
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
=======
>>>>>>> displaying_results

def sort_zipped_packages_window():
    window = Toplevel(root)
    window.title('Sort')
    zippedPackages = sortPackagesByOrderNumber(glob(downloadDir + '*.zip'))
    snort_label_count = len(zippedPackages)
<<<<<<< HEAD
    progress_frame = LabelFrame(
        window,
        text='Progress',
        padx=10,
        pady=10,
        width=250
        )
    progress_frame.pack(padx=10, pady=10)

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
    progress_bar = ttk.Progressbar(
        progress_frame,
        orient='horizontal',
        length=200,
        mode='determinate',
        )
=======
    progress_frame = LabelFrame(window, text='Progress', padx=10, pady=10, width=250)
    progress_frame.pack(padx=10, pady=10)

    if snort_label_count == 67:
        snort_label = Label(progress_frame, text=f'Now sorting {snort_label_count} orders.\n\n'
                            'ALL HAIL SIXTY SEVEN\nTHE 19TH AND HOLIEST PRIME')
    else:
        snort_label = Label(progress_frame, text=f'Now sorting {snort_label_count} orders.')
    snort_label.pack(padx=10, pady=10)
    progress_bar = ttk.Progressbar(progress_frame, orient='horizontal', length=200, mode='determinate', )
>>>>>>> displaying_results
    progress_bar.pack(pady=10, padx=20)

    status_label = Label(progress_frame, text='Working...')
    status_label.pack()

    progress_bar['maximum'] = snort_label_count

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
<<<<<<< HEAD
        orderJSON = str(glob(unzip_dir + '*.json')).split('\'')[1]
        with open(orderJSON) as file:
            openJSON = json.load(file)
        parseJSON(openJSON, orderJSON, unzip_dir)
        splitMultiPagePDFs(glob(unzip_dir + '*.pdf'))
        checkForMultiQtySamplePdfs(glob(unzip_dir + '*-Samp-*.pdf'))
=======
        orderJSON = str(glob(fileToUnzipTo + '*.json')).split('\'')[1]
        with open(orderJSON) as file:
            openJSON = json.load(file)
        parseJSON(openJSON, orderJSON, fileToUnzipTo)
        splitMultiPagePDFs(glob(fileToUnzipTo + '*.pdf'))
        checkForMultiQtySamplePdfs(glob(fileToUnzipTo + '*-Samp-*.pdf'))
>>>>>>> displaying_results
        try:
            sortPdfsToSortedFolders(glob(unzip_dir + '*.pdf'))
        except:
            sort_results.append(
                f'| Couldn\'t properly sort PDFs in {unzip_dir}'
                )

        progress_bar['value'] += 1
        progress_frame.update_idletasks()

    status_label.config(text='Done!')
    snort_label.config(text=f'Sorted {snort_label_count} orders.')
<<<<<<< HEAD

    cleanupDownloadDir(downloadDir)

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


main_menu_frame = LabelFrame(
    root,
    text='Main Menu',
    padx=10,
    pady=10
    )
=======

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

>>>>>>> displaying_results

main_menu_frame.pack(padx=10, pady=10)

<<<<<<< HEAD
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
=======
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
>>>>>>> displaying_results

root.mainloop()
