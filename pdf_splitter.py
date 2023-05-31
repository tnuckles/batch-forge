#!usr/bin/env python

import glob
import os
import shutil
from datetime import date

import pikepdf
from PyPDF2 import PdfFileReader, PdfFileWriter, errors

import get_pdf_data as get_pdf
import wallpaper_sorter_variables as gv

today = date.today()


def splitMultiPagePDFs(print_pdf):
    friendly_name = get_pdf.friendlyName(print_pdf)
    try:
        pdf = pikepdf.Pdf.open(print_pdf)
        num_of_pages = len(pdf.pages)
    except:
        print(f"| Couldn't check the number of pages on {friendly_name}")
        pass
    if num_of_pages > 1:
        print(f"| {friendly_name} has more than one page in its PDF. Splitting now.")
        template_name = get_pdf.template_name(print_pdf)
        namePt1 = print_pdf.split("Qty ")[0] + "Qty "
        namePt2 = print_pdf.split(template_name)[1]
        repeat = get_pdf.repeat(print_pdf)  ##
        quantity = get_pdf.quantity(print_pdf)
        for n, page in enumerate(pdf.pages):
            dst = pikepdf.Pdf.new()
            dst.pages.append(page)
            dst.save(
                namePt1
                + str(quantity)
                + "-"
                + template_name
                + " Panel "
                + str(n + 1)
                + namePt2
            )
        try:
            os.remove(print_pdf)
            print(f"| Finished splitting {friendly_name}")
        except:
            print(
                f"| Split the pages of {friendly_name},\nbut couldn't remove the original."
            )


def checkRepeatSize():
    for printPDF in glob.iglob(gv.DOWNLOAD_DIR + "*.pdf"):
        printPDFFull = printPDF.split("/")[-1].split("-")[7]
        printPDFrepeat = int(printPDF.split("/")[-1].split("-")[8].split("Rp ")[1])
        if printPDFFull == "Full":
            if printPDFrepeat % 2 == 1:
                try:
                    shutil.move(printPDF, gv.NEEDS_ATTENTION_DIR)
                    print(
                        "| File has an odd repeat and has been moved to 4 Needs Attention"
                    )
                    print("| File:", printPDF.split("/")[-1])
                except shutil.Error:
                    shutil.copy(printPDF, gv.NEEDS_ATTENTION_DIR)
                    try:
                        os.remove(printPDF)
                    except OSError:
                        print("|> Could not successfully remove file.")
                        print("|> File:", printPDF)
                except FileNotFoundError:
                    print("| Couldn't find the following file.")
                    print("| File:", printPDF)
            elif printPDFrepeat == 2:
                continue
            elif printPDFrepeat > 2:
                try:
                    crop_multipanel_pdfs(printPDF)
                except errors.PdfReadError:
                    print(
                        "| Couldn't crop the panels for the following order. Please check non-repeat 2 folders."
                    )
                    continue

    return


def checkRepeatDuringBatching(pdf, batch_dir):
    printPDFFull = pdf.split("/")[-1].split("-")[7]
    printPDFrepeat = int(pdf.split("/")[-1].split("-")[8].split("Rp ")[1])
    if printPDFFull == "Full":
        if printPDFrepeat % 2 == 1:
            try:
                shutil.move(pdf, gv.NEEDS_ATTENTION_DIR)
                print(
                    "| File has an odd repeat and has been moved to 4 Needs Attention"
                )
                print("| File:", pdf.split("/")[-1])
            except shutil.Error:
                shutil.copy(pdf, gv.NEEDS_ATTENTION_DIR)
                try:
                    os.remove(pdf)
                except OSError:
                    print("|> Could not successfully remove file.")
                    print("|> File:", pdf)
                    return
            except FileNotFoundError:
                print("| Couldn't find the following file.")
                print("| File:", pdf)
                return
        elif printPDFrepeat == 2:
            return
        elif printPDFrepeat > 2:
            try:
                crop_multipanel_pdfs(pdf, batch_dir)
            except errors.PdfReadError:
                print(
                    "| Couldn't crop the panels for the following pdf. Please check the batch folder"
                )
                print("| PDF:", pdf.split("/")[-1])
                return


def determine_panel_quantity(quantity, repeat, OT=False):
    quantity_per_panel_dict = {}

    quantity_counter = 0
    repeat = int(repeat / 2)
    for panel in range(repeat):
        quantity_per_panel_dict[panel + 1] = 0
    if OT != False:
        quantity_per_panel_dict[int(OT)] = quantity
    else:
        while quantity_counter < quantity:
            for panel in range(repeat):
                panel_num = panel + 1
                quantity_per_panel_dict[panel_num] += 1
                quantity_counter += 1
                if quantity_counter == quantity:
                    break
                elif panel_num == repeat:
                    panel = 0

    return quantity_per_panel_dict


def crop_multipanel_pdfs(print_pdf_to_split, batch_dir):
    storage_dir = gv.CALDERA_DIR + "# Past Orders/Original Files/"
    shutil.copy(print_pdf_to_split, storage_dir)

    order_dict = {
        "file_name": print_pdf_to_split.split(".pdf")[0],
        "order_number": get_pdf.order_number(print_pdf_to_split),
        "order_item": get_pdf.order_item(print_pdf_to_split),
        "due_date": get_pdf.due_date(print_pdf_to_split),
        "ship_method": get_pdf.ship_method(print_pdf_to_split),
        "material": get_pdf.material(print_pdf_to_split),
        "size": get_pdf.size(print_pdf_to_split),
        "repeat": get_pdf.repeat(print_pdf_to_split),
        "repeat_panels": int(get_pdf.repeat(print_pdf_to_split) / 2),
        "quantity": get_pdf.quantity(print_pdf_to_split),
        "odd_or_even": get_pdf.odd_or_even(print_pdf_to_split),
        "template_name": get_pdf.template_name(print_pdf_to_split),
        "order_length": get_pdf.length(print_pdf_to_split),
        "order_width": get_pdf.width(print_pdf_to_split),
        "order_height": get_pdf.height(print_pdf_to_split),
        "multi_page_pdfs": [],
        "pdf_panels_to_combine": [],
    }

    order_dict["copped_pdf_name"] = (
        order_dict["file_name"].split(order_dict["template_name"])[0]
        + order_dict["template_name"]
        + " Split"
        + order_dict["file_name"].split(order_dict["template_name"])[1]
        + ".pdf"
    )

    if "(OTP" in get_pdf.name(order_dict["template_name"]):
        OT_Panel = (
            get_pdf.name(order_dict["template_name"]).split("(OTP")[1].split(")")[0]
        )
        quantity_per_panel_dict = determine_panel_quantity(
            order_dict["quantity"], order_dict["repeat"], OT_Panel
        )
    else:
        quantity_per_panel_dict = determine_panel_quantity(
            order_dict["quantity"], order_dict["repeat"]
        )

    os.chdir(batch_dir)
    for page in range(order_dict["repeat_panels"]):
        writer = PdfFileWriter()
        inputPDF = open(print_pdf_to_split, "rb")
        cropPDF = PdfFileReader(inputPDF)
        page = cropPDF.getPage(0)
        lowerLeftX = 0
        lowerLeftY = 0
        upperRightX = 1800
        upperRightY = cropPDF.getPage(0).cropBox.getUpperRight()[1]
        for crop_count in range(order_dict["repeat_panels"]):
            page.trimBox.lowerLeft = (lowerLeftX, lowerLeftY)
            page.trimBox.upperRight = (upperRightX, upperRightY)
            page.bleedBox.lowerLeft = (lowerLeftX, lowerLeftY)
            page.bleedBox.upperRight = (upperRightX, upperRightY)
            page.cropBox.lowerLeft = (lowerLeftX, lowerLeftY)
            page.cropBox.upperRight = (upperRightX, upperRightY)
            writer.addPage(page)
            lowerLeftX += 1728
            upperRightX += 1728
            printPDFName = (
                batch_dir
                + "/"
                + order_dict["order_number"]
                + "-"
                + order_dict["order_item"]
                + "-"
                + str(crop_count + 1)
                + ".pdf"
            )
            if printPDFName in order_dict["multi_page_pdfs"]:
                continue
            else:
                order_dict["multi_page_pdfs"].append(printPDFName)
            with open(printPDFName, "wb") as outputPDF:
                writer.write(outputPDF)
        inputPDF.close()

    for PDF in order_dict["multi_page_pdfs"]:
        writer = PdfFileWriter()
        try:
            print_pdf = PdfFileReader(open(PDF, "rb"))
        except errors.PdfReadError:
            print("| Couldn't fix file. Skipping.\n| File:", PDF)
            continue
        num_of_pages = print_pdf.getNumPages()

        for pageNum in range(num_of_pages):
            if (pageNum + 1) < num_of_pages:
                continue
            else:
                writer.addPage(print_pdf.getPage(pageNum))

        newNamePt1 = order_dict["file_name"].split(order_dict["template_name"])[0]
        newNamePt2 = order_dict["file_name"].split(order_dict["template_name"])[1]
        panelNum = (
            order_dict["template_name"]
            + " TQ"
            + str(order_dict["quantity"])
            + " P"
            + str(pageNum + 1)
        )
        newName = newNamePt1 + panelNum + newNamePt2 + ".pdf"

        new_quantity_name_pt1 = (
            newName.split("Qty " + str(order_dict["quantity"]))[0] + "Qty "
        )
        new_quantity_name_pt2 = newName.split("Qty " + str(order_dict["quantity"]))[1]
        adjusted_quantity = str(quantity_per_panel_dict[pageNum + 1])
        final_name = new_quantity_name_pt1 + adjusted_quantity + new_quantity_name_pt2

        if final_name in order_dict["pdf_panels_to_combine"]:
            continue
        else:
            order_dict["pdf_panels_to_combine"].append(final_name)

        with open(final_name, "wb") as outputPDF:
            writer.write(outputPDF)

    # splitAndCombinedPDF = combineSplitPDFS(order_dict['pdf_panels_to_combine'], order_dict['copped_pdf_name'])

    for PDF in order_dict["multi_page_pdfs"]:
        os.remove(PDF)
    os.remove(print_pdf_to_split)

    for print_pdf in glob.glob(batch_dir + "/*-Qty 0-*"):
        os.remove(print_pdf)
