#!usr/bin/env python

import glob
import json
import zipfile as zf
from datetime import date, timedelta
from os import listdir, remove, rename, rmdir, walk
from re import findall
from shutil import Error, copy, move

import pikepdf
from macos_tags import get_all as checkTags

import get_pdf_data as get_pdf
from batch_forge_config import GENERAL_VARS as GV
from batch_forge_config import GENERAL_VARS_HIDDEN as GVH
from batch_forge_config import DRIVE_DIR, global_batch_counter
from add_macos_tag import apply_tag as applyTag

BATCH_FOLDERS_DIR = GVH["Caldera Dirs"]["Batches"]
SORTING_DIR = GVH["Caldera Dirs"]["Sorting"]
NEEDS_ATTENTION_DIR = GVH["Caldera Dirs"]["Attention"]
DOWNLOAD_DIR  = GVH["Caldera Dirs"]["Downloads"]

today = date.today()
missing_pdf_list = []
damaged_pdf_list = []
split_pdf_list = []
ot_panel_unknown_list = []



def startupChecks():
    checkBatchCounter()
    moveForDueDates(glob.glob(SORTING_DIR + "**/*.pdf", recursive=True))


def checkBatchCounter():
    if global_batch_counter["batchCounter"] > 9000:
        global_batch_counter["batchCounter"] = 1


def dueDateLookup(printPdf):
    if "order trouble" in str(checkTags(printPdf)):
        return "1 - OT/"
    else:
        dueDate = get_pdf.due_date(printPdf)
        if dueDate < date.today():
            return "2 - Late/"
        elif dueDate > date.today() + timedelta(days=1):
            return "5 - Future/"
        elif dueDate == date.today():
            return "3 - Today/"
        else:
            return "4 - Tomorrow/"


def moveForDueDates(pathToCheck):
    print("\n| Updating Orders. Today's date:", today)
    sortPdfsToSortedFolders(pathToCheck)
    print("| Done updating orders based on Due Dates.")


def sortPdfsToSortedFolders(pathToCheck):
    for printPdf in pathToCheck:
        friendlyName = get_pdf.friendly_name(printPdf)
        orderDueDate = dueDateLookup(printPdf)
        material = get_pdf.material(printPdf)
        orderSize = get_pdf.size(printPdf)
        repeat = get_pdf.repeat(printPdf)
        oddOrEven = get_pdf.odd_or_even(printPdf)
        orderLength = get_pdf.length(printPdf)

        # Checks if order is over the maximum length of a roll and moves it to Needs Attention
        if "(OTPUnknown)" in printPdf.split("/")[-1]:
            ot_panel_unknown_list.append(get_pdf.name(printPdf))
            move(
                printPdf,
                NEEDS_ATTENTION_DIR
                + printPdf.split("/")[-1].split(".pdf")[0]
                + "_OT PANEL UNKNOWN.pdf",
            )
        if orderLength >= GVH["Lookups"]["Material Length"][material]:
            try_to_move_pdf(printPdf, NEEDS_ATTENTION_DIR, friendlyName)
        else:
            if orderSize == "Samp":
                newFilePath = (
                    SORTING_DIR
                    + orderDueDate
                    + GVH["Lookups"]["Paper Dirs"][material]
                    + "Sample/"
                    + printPdf.split("/")[-1]
                )
            else:
                newFilePath = (
                    SORTING_DIR
                    + orderDueDate
                    + GVH["Lookups"]["Paper Dirs"][material]
                    + "Full/"
                    + GVH["Lookups"]["Repeats"][repeat]
                    + GVH["Lookups"]["Odds Dirs"][oddOrEven]
                    + printPdf.split("/")[-1]
                )
        try_to_move_pdf(printPdf, newFilePath, friendlyName)

    ordersInNeedsAttention = len(glob.glob(NEEDS_ATTENTION_DIR + "*.pdf"))
    if ordersInNeedsAttention > 0:
        print(
            f"\n| ****\n| 4 Needs Attention has {ordersInNeedsAttention} file(s) that need attention.\n| ****\n"
        )


def unzipRenameSortPdfs():
    zippedPackages = sortPackagesByOrderNumber(glob.glob(DOWNLOAD_DIR + "*.zip"))
    for package in zippedPackages:
        try:
            fileToUnzipTo = (
                DOWNLOAD_DIR + (package.split("/")[-1].split("_")[0]) + "/"
            )
            with zf.ZipFile(package, "r") as zip_ref:
                zip_ref.extractall(fileToUnzipTo)
        except:
            print("| Couldn't unzip file:", package)
        orderJSON = str(glob.glob(fileToUnzipTo + "*.json")).split("'")[1]
        with open(orderJSON) as file:
            openJSON = json.load(file)
        parseJSON(openJSON, orderJSON, fileToUnzipTo)
        splitMultiPagePDFs(glob.glob(fileToUnzipTo + "*.pdf"))
        checkForMultiQtySamplePdfs(glob.glob(fileToUnzipTo + "*-Samp-*.pdf"))
        try:
            sortPdfsToSortedFolders(glob.glob(fileToUnzipTo + "*.pdf"))
        except:
            print(f"| Couldn't properly sort PDFs in {fileToUnzipTo}")

    reportListOfPdfs(
        split_pdf_list, "were split into multiple files and properly sorted"
    )
    reportListOfPdfs(
        missing_pdf_list, "were missing and were moved to 4 Needs Attention"
    )
    reportListOfPdfs(
        damaged_pdf_list, "were damaged and were moved to 4 Needs Attention"
    )
    reportListOfPdfs(
        ot_panel_unknown_list,
        "had OT panels that couldn't be read and were moved to 4 Needs Attention",
    )

    cleanupDownloadDir(DOWNLOAD_DIR)

    transfer_files_from_drive()


def parseJSON(openFile, JSONPath, fileToUnzipTo):
    count = 1
    JSONitem = openFile["order"]["item"]

    if isinstance(JSONitem, list):
        for itemNum in range(len(JSONitem)):
            count = renamePdfWithDetails(
                openFile, JSONitem[itemNum], JSONPath, fileToUnzipTo, count
            )
    else:
        count = renamePdfWithDetails(openFile, JSONitem, JSONPath, fileToUnzipTo, count)

    return


def renamePdfWithDetails(openFile, JSONitem, JSONPath, fileToUnzipTo, count):
    orderNumber = openFile["orderNumber"]
    keepTrackOfOrderNumber(orderNumber)
    orderTroubleStatus = openFile["type"]
    orderDueDate = openFile["orderDueDate"]
    shipVia = GV["Shipping Methods"][openFile["shippingInfo"]["method"]["shipvia"]]
    originalPDFName = JSONitem["filename"]
    orderItemID = originalPDFName.split("_")[0]
    itemID = originalPDFName.split("_")[0]
    try:
        templateName = (
            JSONitem["description"].split(" ")[2]
            + " "
            + JSONitem["description"].split(" ")[3]
        )
    except IndexError:
        templateName = JSONitem["description"].split(" Wallpaper")[0]
    paperType = GVH["Lookups"]["Substrate"][JSONitem["paper"]]
    quantity = JSONitem["quantityOrdered"]
    height = JSONitem["height"]
    width = JSONitem["width"]
    repeat = JSONitem["wallpaperRepeat"]
    otNotes = openFile["order_trouble_notes"]
    if len(openFile["order_trouble_notes"]) != 0:
        orderTroubleNotes = parseOTNotes(otNotes, orderItemID, repeat)
        if orderTroubleNotes != False:
            templateName = templateName + " " + orderTroubleNotes

    if width == "9":
        orderSize = "Samp"
        length = "9.5"
        height = "9"
        width = "25"
    else:
        width = str(int(width) * int(quantity) + 1)
        height = str(int(height) + 4.25)
        if height == "148.25":
            height = "146.25"
        orderSize = "Full"
        length = str(get_pdf.calculate_length(quantity, height))
        # See Length Notes at the end of the function for an explanation.
    newPDFName = (
        orderNumber
        + "-"
        + str(count)
        + "-("
        + orderDueDate
        + ")-"
        + shipVia
        + "-"
        + paperType
        + "-"
        + orderSize
        + "-Rp "
        + repeat.split("'")[0]
        + "-Qty "
        + quantity
        + "-"
        + templateName
        + "-L"
        + length
        + "-W"
        + width
        + "-H"
        + height
    )
    renamePDF(originalPDFName, newPDFName, JSONPath)
    if orderTroubleStatus != "new":
        applyTag(
            "order trouble",
            DOWNLOAD_DIR
            + "/"
            + get_pdf.order_number(newPDFName)
            + "/"
            + newPDFName
            + ".pdf",
        )
    keepTrackOfPDF(orderNumber, originalPDFName)
    count += 1
    if orderNumber in GVH["Order Items Dicts"]:
        GVH["Order Items Dicts"][orderNumber][itemID] = {
            "Status": "Sorted",
            "Due Date": orderDueDate,
            "Shipping": shipVia,
            "Material": paperType,
            "Order Size": orderSize,
            "Repeat": repeat.split("'")[0],
            "Quantity": quantity,
            "Template": templateName,
            "Length": length,
            "Width": width,
            "Height": height,
            "OT Notes": otNotes,
            "File Path": SORTING_DIR
            + "2 - Late/"
            + GVH["Lookups"]["Paper Dirs"][paperType]
            + GVH["Lookups"]["Size Dirs"][orderSize]
            + GVH["Lookups"]["Repeats"][int(repeat.split("'")[0])]
            + GVH["Lookups"]["Odds Dirs"][int(quantity) % 2]
            + newPDFName,
        }
    else:
        GVH["Order Items Dicts"][orderNumber] = {
            itemID: {
                "Status": "Sorted",
                "Due Date": orderDueDate,
                "Shipping": shipVia,
                "Material": paperType,
                "Order Size": orderSize,
                "Repeat": repeat.split("'")[0],
                "Quantity": quantity,
                "Template": templateName,
                "Length": length,
                "Width": width,
                "Height": height,
                "OT Notes": otNotes,
                "File Path": SORTING_DIR
                + "2 - Late/"
                + GVH["Lookups"]["Paper Dirs"][paperType]
                + GVH["Lookups"]["Size Dirs"][orderSize]
                + GVH["Lookups"]["Repeats"][int(repeat.split("'")[0])]
                + GVH["Lookups"]["Odds Dirs"][int(quantity) % 2]
                + newPDFName,
            }
        }

    """ # Length Notes: I will never remember why I did this, so here are my notes. The length is the length of material an order will take up.
        # Length Notes: The above equation takes the quantity and divides it by two since we can fit two panels side by side.
        # Length Notes: it then multiplies that by the height to get the overall length of material.
        # Length Notes: after, it takes the quantity/2, rounds it down, and multiplies it by .5 for the .5" gap between each panel.
        # Length Notes: lastly, it takes the quantity % 2 to see if the quantity is odd or not. If the quantity is odd, then it will add on one more length of .5"
        # Length Notes: for the times that a panel is by itself and still has another .5" section."""

    return count


def parseOTNotes(otNotes, orderItemID, repeat):
    if "'" in repeat:
        repeat = repeat.split("'")[0]
    try:
        orderItemIDFromUser = str(
            findall(r"(?<!\d)\d{7}(?!\d)", otNotes)
        )  # should find any 7 digit number for the orderItemID
        if orderItemIDFromUser != "[]":
            orderItemIDFromUser = orderItemIDFromUser.split("['")[1].split("']")[0]
            if orderItemIDFromUser != orderItemID:
                return False
        panelID = str(
            findall(r"\D+(\d+)", otNotes)
        )  # should find a digit after a string
        if panelID != "[]":
            panelID = panelID.split("['")[1].split("']")[0]
            if int(panelID) > (int(repeat) / 2):
                formattedOTNotes = "(OTPUnknown)"
                return formattedOTNotes
        formattedOTNotes = "(OTP" + panelID + ")"
        if formattedOTNotes == "(OTP[])":
            formattedOTNotes = False

        return formattedOTNotes
    except:
        formattedOTNotes = "(OTPUnknown)"
        return formattedOTNotes


def renamePDF(old, new, JSONFilePath):
    extension = old.split(".")[-1]
    itemName = new + "." + extension
    dirPath = JSONFilePath.split(JSONFilePath.split("/")[-1])[0]
    try:
        copy(dirPath + old, dirPath + old + " - temp.pdf")
        rename(dirPath + old, dirPath + itemName)
        remove(dirPath + old + " - temp.pdf")
    except OSError:
        try:
            move(JSONFilePath, NEEDS_ATTENTION_DIR)
        except:
            pass
        missing_pdf_list.append(itemName.split("-")[0])
    return


def keepTrackOfPDF(orderNumber, pdfFileName):
    if pdfFileName in GVH["Count of Refd PDFs"][orderNumber]:
        GVH["Count of Refd PDFs"][orderNumber][pdfFileName] += 1
    else:
        GVH["Count of Refd PDFs"][orderNumber][pdfFileName] = 1


def keepTrackOfOrderNumber(
    orderNumber,
):  # keeps track of the original PDF names to alert fulfillment to multi-paper type PDFs
    if orderNumber in GVH["Count of Refd PDFs"]:
        pass
    else:
        GVH["Count of Refd PDFs"][orderNumber] = {}


def reportDuplicatePDFs():  # prints out any PDFs from keepTrackOfOrderNumber() that have a count of 2 or more
    for orderNumber in GVH["Count of Refd PDFs"]:
        for pdfName in GVH["Count of Refd PDFs"][orderNumber]:
            if GVH["Count of Refd PDFs"][orderNumber][pdfName] > 1:
                print(
                    "\n| The following Order has samples with multiple material types:"
                )
                print("| " + orderNumber + ": " + pdfName.replace("_", " "))


def removeUnneededUnzippedFiles(pathToCheck):
    for file in pathToCheck:
        try:
            remove(file)
        except:
            print(f"| Couldn't remove {file}")


def removeEmptyDirectories(
    batchDirectory,
):  # once a batch folder has been made, walks through the batch folder and removes any empty directories.
    dirToWalk = list(walk(batchDirectory))
    for path, _, _ in dirToWalk[::-1]:
        if len(listdir(path)) == 0:
            rmdir(path)
    return


def cleanupDownloadDir(pathToClean):
    try:
        removeUnneededUnzippedFiles(glob.glob(pathToClean + "*/*.xml"))
        try:
            removeUnneededUnzippedFiles(glob.glob(pathToClean + "*/*.json"))
            try:
                removeEmptyDirectories(pathToClean)
                try:
                    removeUnneededUnzippedFiles(glob.glob(pathToClean + "*.zip"))
                except:
                    print("| Unknown error while removing zip folders in 3 Downloaded")
                    pass
            except:
                print("| Unknown error while removing empty folders in 3 Downloaded")
                pass
        except:
            print("| Unknown error while removing JSON files in 3 Downloaded")
            pass
    except:
        print("| Unknown error while removing XML files in 3 Downloaded")
        pass
    return


def splitMultiPagePDFs(pathGlobToCheck):
    results = []
    for file in pathGlobToCheck:
        try:
            pdf = pikepdf.Pdf.open(file)
            NumOfPages = len(pdf.pages)
        except:
            damaged_pdf_list.append(get_pdf.name(file))
            move(
                file,
                NEEDS_ATTENTION_DIR
                + file.split("/")[-1].split(".pdf")[0]
                + "_DAMAGED.pdf",
            )
            pass
        try:
            NumOfPages = len(pdf.pages)
            if NumOfPages > 1:
                templateName = get_pdf.template_name(file)
                namePt1 = file.split("Qty ")[0] + "Qty "
                namePt2 = file.split(templateName)[1]
                quantity = get_pdf.quantity(file)
                for n, page in enumerate(pdf.pages):
                    dst = pikepdf.Pdf.new()
                    dst.pages.append(page)
                    dst.save(
                        namePt1
                        + str(quantity)
                        + "-"
                        + templateName
                        + " Panel "
                        + str(n + 1)
                        + namePt2
                    )
                try:
                    remove(file)
                    split_pdf_list.append(get_pdf.friendly_name(file))
                except:
                    results.append(
                        f"| Split the pages of {file},\nbut couldn't remove the original."
                    )
        except:
            pass
    return results


def checkForMultiQtySamplePdfs(pdfList):
    listOfSampsToDuplicate = []

    for printPdf in pdfList:
        quantity = get_pdf.quantity(printPdf)
        if quantity > 1:
            pdfName = get_pdf.template_name(printPdf)
            sampToDuplicate = []
            sampToDuplicate.append(printPdf)
            for i in range(quantity):
                firstHalf = printPdf.split("Qty " + str(quantity))[0]
                pdfNameWithCounter = pdfName + "(" + str(i + 1) + ")"
                secondHalf = printPdf.split(pdfName)[1]
                newNameToDuplicate = (
                    firstHalf + "Qty 1-" + pdfNameWithCounter + secondHalf
                )
                sampToDuplicate.append(newNameToDuplicate)
            listOfSampsToDuplicate.append(tuple(sampToDuplicate))

    for tupleOfSamples in listOfSampsToDuplicate:
        sampToDuplicateFrom = tupleOfSamples[0]
        for i in tupleOfSamples:
            if i == sampToDuplicateFrom:
                continue
            else:
                copy(sampToDuplicateFrom, i)
        remove(sampToDuplicateFrom)

    return


def reportListOfPdfs(list_to_report, str_to_print):
    results = []
    if len(list_to_report) > 0:
        for item in list_to_report:
            if item == None:
                pass
            else:
                results.append(f"{item}: {str_to_print}")
        return results
    else:
        return results


def sortPackagesByOrderNumber(
    packageList,
):  # takes a list of pathstopdfs and sorts them by orderNumber, from least to greatest.
    listToSort = []
    sortedList = []
    for package in packageList:
        pdfOrderNumber = package.split("/")[-1].split("_")[0]
        listToSort.append((pdfOrderNumber, package))
    listToSort.sort(reverse=False, key=lambda pdf: pdf[0])
    packageList = listToSort
    listToSort = []
    for package in packageList:
        sortedList.append(package[1])
    packageList = sortedList
    sortedList = []
    return packageList


def try_to_move_pdf(
    printPDF, BatchDir, friendlyPdfName, verbose=False
):  # function that tries to move a PDF. If it can't move, it will try to copy then remove the original. If it can't do that, it will error out gracefully.
    try:
        move(printPDF, BatchDir)
        if verbose == True:
            print(f"| Moved: {friendlyPdfName}")
        return
    except Error:
        if get_pdf.size == "Full":
            copy(printPDF, BatchDir)
        try:
            remove(printPDF)
            return
        except OSError:
            print(
                "|> Moved PDF to batch folder, but couldn't remove the original file. Please remove the original file."
            )
            print("|> PDF:", friendlyPdfName)
            print("|> Path:", printPDF)
            return
    except FileNotFoundError:
        print("|> Couldn't move PDF. Please check to make sure it exists.")
        print("|> PDF:", friendlyPdfName)
        print("|> Path:", printPDF)
        return


def transfer_files_from_drive():
    # New name convention: 300013884-1-(2022-02-02)-Stnd-Wv-Samp-Rp 2-Qty 1-Watercolor Herringbone-L9.5-W25-H9

    list_to_transfer = glob(DRIVE_DIR + "/*.pdf")
    if len(list_to_transfer) < 1:
        print("\n| No files to transfer from Google Drive.")
        return
    for print_pdf in list_to_transfer:
        pdf_name = get_pdf.name(print_pdf)
        pdf_friendly_name = get_pdf.friendly_name(pdf_name)
        pdf_material = GVH["Lookups"]["Papere Dirs"][get_pdf.material(pdf_name)]
        pdf_order_size = GVH["Lookups"]["Size Dirs"][get_pdf.size(pdf_name)]
        pdf_repeat = GVH["Lookups"]["Repeats"][get_pdf.repeat(pdf_name)]
        even_or_odd = GVH["Lookups"]["Odds Dors"][get_pdf.odd_or_even(pdf_name)]
        if pdf_order_size == "Full":
            dest_path = (
                SORTING_DIR
                + "3 - Today/"
                + pdf_material
                + pdf_order_size
                + pdf_repeat
                + even_or_odd
                + pdf_name
                + ".pdf"
            )
        else:
            dest_path = (
                SORTING_DIR
                + "3 - Today/"
                + pdf_material
                + pdf_order_size
                + pdf_name
                + ".pdf"
            )
        print(f"\n| Trying to move {pdf_friendly_name}.")
        try_to_move_pdf(print_pdf, dest_path, pdf_friendly_name, verbose=True)
    print("\n| Finished transferring files from Google Drive.")

    return
