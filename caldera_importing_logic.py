"""
Logic for importing batches.
"""

from glob import glob
from math import ceil, floor
from os import path
from shutil import move
from time import sleep


import batch_sorting as bs
import get_pdf_data as get_pdf
from batch_logic import try_to_move_pdf
from batch_forge_config import GENERAL_VARS_HIDDEN as GVH

HOTFOLDERS_DIR = GVH["Caldera Dirs"]["Hotfolders"]


def sort_batches_by_ID(batchList: list) -> list:
    """
    Accepts a list of pathsToBatches and sorts them by batch ID, from least to greatest.
    """

    listToSort = []
    sortedList = []
    for batch in batchList:
        batchID = int(batch.split("/")[-1].split(" ")[1].split("#")[1])
        listToSort.append((batchID, batch))
    listToSort.sort(reverse=False, key=lambda batchDir: batchDir[0])
    newBatchList = listToSort
    listToSort = []
    for printPdf in newBatchList:
        sortedList.append(printPdf[1])
    batchList = sortedList
    sortedList = []
    return batchList


def sort_samples_for_cutting(pdf_list: list) -> list:
    """
    Accepts a list of samples, then sorts them by by every-other. That way the
    samples print from top to bottom instead of right to left.

    Returns a list.
    """

    if len(pdf_list) == 0:
        return

    half_list_len = ceil(len(pdf_list) / 2)
    second_list_len = floor(len(pdf_list) / 2)

    firstList = []
    secondList = []

    counter = 0

    for printPdf in pdf_list:
        if counter < half_list_len:
            firstList.append(printPdf)
            counter += 1
        else:
            secondList.append(printPdf)

    sortedList = []

    counter = 0
    for current_count in range(half_list_len):
        sortedList.append(firstList[counter])
        try:
            sortedList.append(secondList[counter])
        except IndexError:
            break
        counter += 1

    return sortedList


def move_to_hotfolder(
    pdf_list: list, receiving_hotfolder: str, progress_dict: dict
) -> None:
    """
    Accepts pdf_list as a list, receiving_hotfolder as a str, and a dict of a
    tkinter frame, label, and progress bar. Iterates through the list of pdfs
    and moves them into the receiving hotfolder for printing.
    """

    for printPdf in pdf_list:
        friendly_name = get_pdf.friendly_name(printPdf)
        progress_dict["label"].config(text=f"Moving {friendly_name}")
        progress_dict["frame"].update()
        try_to_move_pdf(printPdf, receiving_hotfolder, friendly_name)
        sleep(0.25)
        progress_dict["bar"]["value"] += 1
        progress_dict["frame"].update()
    return


def import_to_caldera(batch: str, printer: str, progress_dict: dict) -> None:
    """
    Accepts a batch file path, printer file path as a string, and dict with a
    tkinter frame, label, and progress bar. Loops through the batch's contents
    in reverse order. Moves each print pdf to a specified printer's hotfolder
    based on material type.

    Returns nothing.
    """

    # Sets progress bar maximum
    progress_bar = progress_dict["bar"]
    pdfs_in_batch = len(glob(batch + "/**/*.pdf", recursive=True))
    progress_bar["maximum"] = pdfs_in_batch

    # get material type for currently importing hotfolder
    material = batch.split("/")[-1].split(" ")[2]

    # move batch to the correct currently importing hotfolder
    batch_name = batch.split("/")[-1]
    progress_dict["label"].config(text=f"Moving {batch_name}")
    progress_dict["frame"].update()
    move(batch, HOTFOLDERS_DIR + printer + "z_Currently Importing " + material + "/")
    # wait(2)

    # Creates variables for the batch
    batch = batch.split("/")[-1]
    receiving_hotfolder = HOTFOLDERS_DIR + printer + material + "/"
    batch = (
        HOTFOLDERS_DIR
        + printer
        + "z_Currently Importing "
        + material
        + "/"
        + batch
        + "/"
    )
    batch_num = batch.split("Batch #")[1].split(" ")[0]
    # batch = /Users/Trevor/Documents/Scripts/Misc/caldera/var/public/1 Hotfolders/BATCH_NAME_VARIABLE/

    batch_dirs_list = (
        batch + "5 - Future/",
        batch + "4 - Tomorrow/",
        batch + "3 - Today/",
        batch + "2 - Late/",
        batch + "1 - OT/",
        batch + "6 - Utility/",
    )

    for priority in batch_dirs_list:
        pri_dir_name = priority.split("/")[-2].split(" ")[2]
        progress_dict["label"].config(text=f"Checking for {pri_dir_name}")
        progress_dict["frame"].update()
        if path.exists(priority):
            progress_dict["label"].config(text=f"{pri_dir_name} exists.")
            progress_dict["frame"].update()
            if "6 - Utility" not in priority:
                samples_list = glob(priority + "Samples/*.pdf")
                full_list = glob(priority + "Full/*.pdf")
                if len(samples_list) != 0:
                    progress_dict["label"].config(text="Organizing samples...")
                    progress_dict["frame"].update()
                    sort_by_item_num = bs.sort_pdfs_by_item_number(samples_list)
                    sort_by_order_num = bs.sort_pdfs_by_order_number(sort_by_item_num)
                    ready_list = sort_samples_for_cutting(sort_by_order_num)
                    move_to_hotfolder(ready_list, receiving_hotfolder, progress_dict)
                if len(full_list) != 0:
                    progress_dict["label"].config(text="Organizing full panels...")
                    progress_dict["frame"].update()
                    sort_by_item_num = bs.sort_pdfs_by_item_number(full_list)
                    ready_list = bs.sort_pdfs_by_order_number(sort_by_item_num)
                    move_to_hotfolder(ready_list, receiving_hotfolder, progress_dict)
            else:
                if "6 - Utility" in priority:
                    utility_list = glob(priority + "*.pdf")
                    move_to_hotfolder(utility_list, receiving_hotfolder, progress_dict)

    progress_dict["bar"]["value"] = progress_dict["bar"]["maximum"]
    progress_dict["label"].config(text=f"Batch {batch_num} imported!")
    progress_dict["frame"].update()
    progress_dict["close_button"].config(state="normal")

    # allBatchLists = [
    #     sort_samples_for_cutting(sortPdfsByOrderNumber(sortPdfsByOrderItemNumber(glob(batch + '5 - Future/Samples/*.pdf', recursive=True)))),
    #     sortPdfsByOrderNumber(sortPdfsByOrderItemNumber(glob(batch + '5 - Future/Full/*.pdf', recursive=True))),
    #     sort_samples_for_cutting(sortPdfsByOrderNumber(sortPdfsByOrderItemNumber(glob(batch + '4 - Tomorrow/Samples/*.pdf', recursive=True)))),
    #     sortPdfsByOrderNumber(sortPdfsByOrderItemNumber(glob(batch + '4 - Tomorrow/Full/*.pdf', recursive=True))),
    #     sort_samples_for_cutting(sortPdfsByOrderNumber(sortPdfsByOrderItemNumber(glob(batch + '3 - Today/Samples/*.pdf', recursive=True)))),
    #     sortPdfsByOrderNumber(sortPdfsByOrderItemNumber(glob(batch + '3 - Today/Full/*.pdf', recursive=True))),
    #     sort_samples_for_cutting(sortPdfsByOrderNumber(sortPdfsByOrderItemNumber(glob(batch + '2 - Late/Samples/*.pdf', recursive=True)))),
    #     sortPdfsByOrderNumber(sortPdfsByOrderItemNumber(glob(batch + '2 - Late/Full/*.pdf', recursive=True))),
    #     sort_samples_for_cutting(sortPdfsByOrderNumber(sortPdfsByOrderItemNumber(glob(batch + '1 - OT/Samples/*.pdf', recursive=True)))),
    #     sortPdfsByOrderNumber(sortPdfsByOrderItemNumber(glob(batch + '1 - OT/Full/*.pdf', recursive=True))),
    #     glob(batch + '5 - Utility/*.pdf', recursive=True),
    # ]

    # for pdf_list in allBatchLists:
    #     try:
    #         move_to_hotfolder(pdf_list, receiving_hotfolder)
    #     except TypeError:
    #         pass

    # print('\n| Moved', batch.split('/')[-2], 'into', receiving_hotfolder.split('/')[6].split(' ')[1], material, 'HotFolder')
    return
