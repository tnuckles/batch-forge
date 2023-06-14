# /Users/Trevor/Documents/Scripts/batch-forge python
# UI Script for Batch Forge

import json
import zipfile as zf
from glob import glob
from tkinter import *
from tkinter import ttk

from batch_sorting import *
from wallpaper_sorter_functions import (
    checkForMultiQtySamplePdfs,
    cleanupDownloadDir,
    missing_pdf_list,
    damaged_pdf_list,
    split_pdf_list,
    parseJSON,
    reportListOfPdfs,
    sortPackagesByOrderNumber,
    sortPdfsToSortedFolders,
    splitMultiPagePDFs,
    ot_panel_unknown_list,
)
from batch_forge_config import GENERAL_VARS_HIDDEN as GVH

DOWNLOAD_DIR = GVH["Caldera Dirs"]["Downloads"]


SORT_RESULTS = []


def get_sort_results() -> list:
    """
    Accepts nothing. Returns a list containing the results of a sort function.
    """
    result_msg_dict = {
        "missing": "missing PDF. Moved to needs Attention.",
        "damaged": "damaged PDF. Moved to Needs Attention.",
        "illegible": "couldn't read OT panels. Moved to Needs Attention.",
        "split": "split into multiple files.",
    }

    results_list = []
    results_list.extend(reportListOfPdfs(missing_pdf_list, result_msg_dict["missing"]))
    results_list.extend(reportListOfPdfs(damaged_pdf_list, result_msg_dict["damaged"]))
    results_list.extend(reportListOfPdfs(split_pdf_list, result_msg_dict["split"]))
    results_list.extend(
        reportListOfPdfs(ot_panel_unknown_list, result_msg_dict["illegible"])
    )
    return results_list


def sort_zipped_packages_window(root) -> None:
    """
    Accepts nothing and returns nothing. Opens a window with a progress
    bar to monitor the unzipping and renaming of downloaded sort files.

    When done, cleans out the Downloads folder as well to keep things
    clean. If there are any results for the function, it will display
    them and wait for the user to close the window. Otherwise,
    automatically returns to the main menu.
    """

    SORT_RESULTS = []

    # Initialize sort window
    window = Toplevel(root)
    window.title("Sort")
    zippedPackages = sortPackagesByOrderNumber(glob(DOWNLOAD_DIR + "*.zip"))
    snort_label_count = len(zippedPackages)
    progress_frame = LabelFrame(window, text="Progress", padx=10, pady=10, width=250)
    progress_frame.pack(padx=10, pady=10)

    # This is a fun easter egg for me, but is otherwise worthless.
    if snort_label_count == 67:
        snort_label = Label(
            progress_frame,
            text=f"Now sorting {snort_label_count} orders.\n\n"
            "ALL HAIL SIXTY SEVEN\nTHE 19TH AND HOLIEST PRIME",
        )
    else:
        snort_label = Label(
            progress_frame, text=f"Now sorting {snort_label_count} orders."
        )
    snort_label.pack(padx=10, pady=10)

    # Sets progress bar
    progress_bar = ttk.Progressbar(
        progress_frame, orient="horizontal", length=200, mode="determinate"
    )
    progress_bar.pack(pady=10, padx=20)

    # Sets status label
    status_label = Label(progress_frame, text="Working...")
    status_label.pack()

    progress_bar["maximum"] = snort_label_count

    # Begins unzipping, renaming, and sorting files
    for package in zippedPackages:
        status_label.config(text=package.split("/")[-1])
        try:
            package_name = package.split("/")[-1].split("_")[0]
            unzip_dir = DOWNLOAD_DIR + (package_name) + "/"
            with zf.ZipFile(package, "r") as zip_ref:
                zip_ref.extractall(unzip_dir)
        except:
            unzip_error_label = Label(f"| Couldn't unzip file: {package}")
            unzip_error_label.pack(padx=5, pady=5)
        orderJSON = str(glob(unzip_dir + "*.json")).split("'")[1]
        with open(orderJSON) as file:
            openJSON = json.load(file)
        parseJSON(openJSON, orderJSON, unzip_dir)
        splitMultiPagePDFs(glob(unzip_dir + "*.pdf"))
        checkForMultiQtySamplePdfs(glob(unzip_dir + "*-Samp-*.pdf"))
        try:
            sortPdfsToSortedFolders(glob(unzip_dir + "*.pdf"))
        except:
            SORT_RESULTS.append(f"| Couldn't properly sort PDFs in {unzip_dir}")

        progress_bar["value"] += 1
        progress_frame.update_idletasks()

    # Updates label
    status_label.config(text="Done!")
    snort_label.config(text=f"Sorted {snort_label_count} orders.")

    # Cleans out download directory of unneeded directories and folders
    cleanupDownloadDir(DOWNLOAD_DIR)

    # Displays sort results if any exist;
    # otherwise, closes window and returns to main menu
    SORT_RESULTS = get_sort_results()

    if len(SORT_RESULTS) == 0:
        window.destroy()
    else:
        results_frame = LabelFrame(window, text="Results", padx=5, pady=3, width=350)
        results_frame.pack(padx=10, pady=10)

        for result in SORT_RESULTS:
            if "Needs Attention" in result:
                result_label = Label(results_frame, text=result, fg="red")
                result_label.pack(anchor="w", padx=1, pady=5)
            else:
                result_label = Label(results_frame, text=result)
                result_label.pack(anchor="w", padx=1, pady=5)

        close_btn = Button(
            window,
            text="Return to Main Menu",
            width=20,
            height=2,
            command=window.destroy,
        )
        close_btn.pack(padx=10, pady=10)
