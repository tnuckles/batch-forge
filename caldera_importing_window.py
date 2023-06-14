# /Users/Trevor/Documents/Scripts/batch-forge python

from zipfile import ZipFile, ZIP_DEFLATED
import pathlib
from datetime import datetime, timedelta
from glob import glob
from os.path import getatime
from shutil import rmtree, Error, copy
from time import ctime
from tkinter import *
from tkinter import ttk

from batch_forge_config import BATCHING_VARS as BV
from batch_forge_config import BATCHING_VARS_HIDDEN as BVH
from batch_forge_config import GENERAL_VARS as GV
from batch_forge_config import GENERAL_VARS_HIDDEN as GVH
from batch_forge_config import IMPORTER_VARS as IV
import get_pdf_data as get_pdf
from batch_sorting import *
from caldera_importing_logic import *

today = datetime.today()

PAST_ORDERS_DIR = GVH["Caldera Dirs"]["Past Batches"]
BATCH_FOLDERS_DIR = GVH["Caldera Dirs"]["Batches"]

global status_dict
status_dict = {}


def caldera_import_window(root) -> None:
    """
    Accepts root window. Opens the window for importing batches into caldera.
    """

    # Set root to a new variable and make it globally accessible.
    global root_window
    root_window = root

    # Clear out the status_dict. Status dict is used for easily accessing
    # The various labels and buttons for different printers
    if status_dict:
        status_dict.clear()

    # Set Importing Window
    global importer_window
    importer_window = Toplevel(root_window)
    importer_window.title("Caldera Importer")

    # Set the rows and columns to adjust as the window resizes
    importer_window.columnconfigure(0, weight=1)
    importer_window.columnconfigure(1, weight=1)
    importer_window.rowconfigure(0, weight=1)
    importer_window.rowconfigure(1, weight=1)

    # Counters for the rows and columns
    printer_row = 0
    printer_column = 0

    # Set printer frames
    for printer_index in IV["Printers"]:
        if printer_index == "4":
            # 4 Is unlucky in Japan, so we don't have a 4th printer.
            # We skipped straight to the 5th.
            continue

        # Printer ID is printer name: 'Ichi', 'Ni', 'San', 'Go', etc.
        printer_id = IV["Printers"][printer_index][0]

        # Printer Path is the path variable in the directory: '1 Ichi/', etc.
        printer_path = IV["Printers"][printer_index][1]

        # Setup status dict
        status_dict[printer_index] = {"name": printer_id, "path": printer_path}

        # Set printer frame
        printer_frame = Frame(importer_window, padx=15, pady=10, relief=SUNKEN, bd=8)
        printer_frame.grid(row=printer_row, column=printer_column, sticky="nsew")

        # Logic to display printers in a 2-column grid. Probably a neater way to do this
        if printer_row % 2 == 0:
            if printer_column % 2 == 0:
                printer_column += 1
            else:
                printer_row += 1
        else:
            if printer_column % 2 == 1:
                printer_column -= 1
            else:
                printer_row += 1

        # Set printer name label
        printer_name_label = Label(
            printer_frame,
            text=IV["Printers"][printer_index][0],
            justify=CENTER,
            font=("Arial", 25),
        )
        printer_name_label.pack()

        # Set printer status frame, label, and status
        printer_status_frame = LabelFrame(printer_frame, text="Status", padx=40, pady=4)
        printer_status_frame.pack()

        # Row Counter to display printer statuses properly
        row_counter = 0

        # Loop through to add each printer's paper type to the label
        for paper in GV["Paper Types"]:
            status_dict[printer_index][paper] = {}
            paper_counter = 0
            paper_type = paper

            # Set label for each paper. Displays name of the paper
            status_paper_label = Label(printer_status_frame, text=(paper + ":"))
            status_paper_label.grid(column=0, row=row_counter, sticky=E)

            # Set the label for the batch. Will show either Available or the batch name if unavailable
            paper_status_label = Label(
                printer_status_frame,
                text=get_printer_status(paper_type, printer_path),
                fg="green",
            )
            paper_status_label.grid(column=1, row=row_counter, sticky=W)

            # Increment row  counter
            row_counter += 1

            # Set the import/export button below the paper.
            import_export_button = Button(
                printer_status_frame,
                text="Import Batch",
                command=lambda paper=paper, printer_path=printer_path: batch_select_window(
                    paper, printer_path
                ),
            )
            import_export_button.grid(column=1, row=row_counter, sticky="w")

            # Add the label and button to the status dict for easy referencing later
            status_dict[printer_index][paper] = {
                "batch_label": paper_status_label,
                "batch_button": import_export_button,
            }

            # Increment row counter
            row_counter += 1

            # Increment paper counter
            paper_counter += 1

    # Once all of the buttons have been made, call refresh_printer_statuses
    # to show which folders are locked/ready for import/ready for export.
    refresh_printer_statuses()

    # Set bottom button frame for refresh and return buttons
    bottom_buttons_frame = Frame(importer_window, bd=5, relief=SUNKEN)
    bottom_buttons_frame.grid(row=row_counter, column=0, columnspan=2, sticky="nsew")

    # Set refresh button
    refresh_btn = Button(
        bottom_buttons_frame,
        text="Refresh Printers",
        width=20,
        height=3,
        command=refresh_printer_statuses,
    )
    refresh_btn.pack(side=LEFT, expand=TRUE, fill="both")

    # Set return button
    close_btn = Button(
        bottom_buttons_frame,
        text="Return to Main Menu",
        width=20,
        height=3,
        command=importer_window.destroy,
    )
    close_btn.pack(side=RIGHT, expand=TRUE, fill="both")


def refresh_printer_statuses() -> None:
    """
    Accepts and returns nothing. Iterates over each label/button in the window
    to show the proper locked/ready to import/ ready to export status.
    """
    for printer in status_dict:
        for paper in status_dict[printer]:
            if type(status_dict[printer][paper]) == str:
                continue

            # Set paper label, import button, and printer path for easy reading
            paper_label = status_dict[printer][paper]["batch_label"]
            import_button = status_dict[printer][paper]["batch_button"]
            printer_path = status_dict[printer]["path"]

            # Set label text, and set color to green by default
            paper_label.config(text=get_printer_status(paper, printer_path), fg="green")
            import_button.config(
                text="Import Batch",
                command=lambda paper=paper, printer_path=printer_path: batch_select_window(
                    paper, printer_path
                ),
            )

            # Check if Available is in the label. If not, sets text to batch name and color to red.
            if "Available" not in paper_label.cget("text"):
                try:
                    locked_batch = (
                        HOTFOLDERS_DIR
                        + printer_path
                        + f"z_Currently Importing {paper}/"
                    )
                    paper_label.config(fg="red")
                    import_button.config(
                        text=get_lock_status(locked_batch)[0],
                        command=lambda paper=paper, printer_path=printer_path: export_batch(
                            paper, printer_path
                        ),
                        state=get_lock_status(locked_batch)[1],
                    )
                except FileNotFoundError:
                    continue


def get_lock_status(locked_batch: str) -> tuple[str, str]:
    """
    Accepts a patch to a batch folder as a string, returns a tuple of two
    strings. The first will be the text to display on the export button.
    The second will be either 'disabled' or 'normal' for the status
    of a button.
    """
    current_time = datetime.now()
    import_time = datetime.strptime(
        ctime(getatime(locked_batch)), "%a %b %d %H:%M:%S %Y"
    )
    unlock_time = import_time + timedelta(minutes=IV["Import Batch Lock Time"])
    if current_time < unlock_time:
        button_text = f"Batch locked until {unlock_time}"
        return button_text, DISABLED
    else:
        return "Export Batch", NORMAL


def get_printer_status(paper: str, printer_path: str) -> str:
    """
    Accepts paper as a string and printer_path as a string. Uses glob to look
    through printer folders and return if a printer is importing a
    batch for the given paper type.

    Returns 'Available' if the printer is open, otherwise returns a batch name.
    """

    # If the number of batches in a hotfolder is 0, it is available
    if (
        len(
            glob(
                HOTFOLDERS_DIR
                + "/"
                + printer_path
                + "z_Currently Importing "
                + paper
                + "/*"
            )
        )
        == 0
    ):
        return "Available"

    # Else, display batch name
    else:
        return glob(
            HOTFOLDERS_DIR
            + "/"
            + printer_path
            + "z_Currently Importing "
            + paper
            + "/*"
        )[0].split("/")[-1]


def batch_select_window(paper: str, printer_path: str) -> None:
    """
    Accepts paper type as a string, path to the printer as a string.
    Opens a new window with list of available batches to import for the given
    printer and paper type.

    Returns nothing.
    """
    # Set batch selector window and make it global
    global batch_selector_window
    batch_selector_window = Toplevel(importer_window)
    printer_name = printer_path.split(" ")[1].split("/")[0]

    # Set window title
    batch_selector_window.title(
        "Select a " + paper + " Batch for Import to " + printer_name
    )
    # Set window framee
    selector_window_frame = Frame(batch_selector_window, relief=SUNKEN, bd=8, padx=20)
    selector_window_frame.pack()

    # Iterate over priority options to make a frame for each
    for priority in BV["Priorities"]:
        priority = BV["Priorities"][priority]
        # Set labelFrame for each priority
        priority_frame = LabelFrame(
            selector_window_frame, text=priority, padx=20, pady=5
        )
        priority_frame.pack(expand=True, fill=BOTH, side=TOP, padx=30, pady=5)

        # Set the path to the batches folder for the Glob in following line
        batches_path = BATCH_FOLDERS_DIR + "* " + paper + "*P-" + priority

        # Make a glob list of the available batches
        batch_list = glob(batches_path)

        # Sort available batches by ID
        batch_list = sort_batches_by_ID(batch_list)

        # If there are no batches, display no available batches
        if len(batch_list) == 0:
            batch_label = Label(priority_frame, text=f"No {priority} batches.")
            batch_label.pack()

        # If batches are available, create a button for each batch on incrementing rows
        row_counter = 0
        for matching_batch in batch_list:
            # Get a friendly batch name
            friendly_batch = matching_batch.split("/")[-1]

            # Set a button for each batch with the text being the label name and the command to import the batch
            batch_button = Button(
                priority_frame,
                text=friendly_batch,
                width=30,
                command=lambda batch=friendly_batch: import_selected_batch(
                    batch, printer_path
                ),
            )
            batch_button.grid(column=0, row=row_counter, sticky=W)
            row_counter += 1

    # Set the cancel button to return to the previous window
    cancel_button = Button(
        selector_window_frame,
        text="Cancel",
        command=lambda: batch_selector_window.destroy(),
    )
    cancel_button.pack(pady=(10, 20))


def import_selected_batch(batch: str, printer_path: str) -> None:
    """
    Accepts a batch name as a string and a printer path as a string. Returns nothing.

    Creates a new window to display a progress bar for importing the batch and moving
    each pdf into the hotfolder in order
    """

    # Destroy the batch_selector_window
    batch_selector_window.destroy()

    # Set batch number
    batch_num = batch.split(" ")[1]

    # Create import window
    import_status_window = Toplevel(importer_window)

    # Set window title
    import_status_window.title("Importing Batch " + batch_num)

    # Set importing frame
    import_status_frame = LabelFrame(import_status_window, text=f"Importing {batch}")
    import_status_frame.pack(padx=10, pady=10)

    # Set progress bar
    import_progress_bar = ttk.Progressbar(
        import_status_frame, orient="horizontal", length=300, mode="determinate"
    )
    import_progress_bar.pack(padx=10, pady=(10, 6))

    # Set label for current import status. Will display which PDF is being imported
    import_pdf_label = Label(import_status_frame, text="Preparing...", padx=2)
    import_pdf_label.pack(padx=3, pady=(0, 6))

    # Set close button to return to the importer window. Disabled by default
    # so importing isn't stopped prematurely.
    close_button = Button(
        import_status_window,
        text="Return to Importer Window",
        width=20,
        height=2,
        state=DISABLED,
        command=lambda: close_import_status_window(import_status_window),
    )
    close_button.pack(padx=10, pady=10)

    # Create a dict for easy access to the frame, label, bar, and button
    import_info_dict = {
        "frame": import_status_frame,
        "label": import_pdf_label,
        "bar": import_progress_bar,
        "close_button": close_button,
    }

    # Set the batch path, then call import_to_caldera to move each pdf into the
    # hotfolder in order and update the progress bar accordingly
    batch_path = BATCH_FOLDERS_DIR + batch
    import_status_window.update()
    import_status_window.after(
        10, import_to_caldera(batch_path, printer_path, import_info_dict)
    )


def export_batch(paper: str, printer_path: str) -> None:
    """
    Accepts paper type as a string and the printer path as a string.
    Returns nothing.

    Removes PDFs from a given printer's hotfolder and back into the batch
    folder. After doing so, moves batch into the Past Orders folder.

    Depending on user's settings, may compress folder to save space.
    """
    # Find the path to the batch directory with a glob
    batch_dir = glob(
        HOTFOLDERS_DIR + printer_path + f"z_Currently Importing {paper}/*/"
    )[0]

    # Get a list of all the priority directories in the batch directory
    priority_in_batch_dir = glob(batch_dir + "*/")

    # Remove each of the priority directories as they aren't needed anymore
    for dir in priority_in_batch_dir:
        rmtree(dir)

    # Get a list of all of the PDFs inside the hotfolder that need to be exported
    paper_hotfolder = HOTFOLDERS_DIR + printer_path + paper + "/"
    batch_list = glob(paper_hotfolder + "*.pdf")

    # Set the friendly name for each PDF.
    for print_pdf in batch_list:
        # Since color charts and roll stickers don't need order numbers or any
        # other info, sets their friendly name to just Color Chart or Roll
        # Stickers, respectively

        if "Color Chart" in print_pdf:
            friendly_name = "Color Chart"
        elif "Roll Sticker" in print_pdf:
            friendly_name = "Roll Stickers"
        else:
            friendly_name = get_pdf.friendly_name(print_pdf)

        try_to_move_pdf(print_pdf, batch_dir, friendly_name)

    # Checks user preferences for whether or not to compress exported batch
    if IV["Compress Exported Batches"] is True:
        zipped_batch_dir = zip_batch_for_export(batch_dir)
        move(zipped_batch_dir, PAST_ORDERS_DIR)
        rmtree(batch_dir)
    else:
        try:
            move(batch_dir, PAST_ORDERS_DIR)
        except Error:
            copy(batch_dir, PAST_ORDERS_DIR)
            rmtree(batch_dir)

    return refresh_printer_statuses()


def zip_batch_for_export(batch_dir: str) -> str:
    """
    Accepts a path to a dir as a string. Compresses the directory before
    exporting for storage.

    Returns a path to the dir as a string.
    """

    # Stripe the last  '/' off of the batch_dir
    dir_to_zip = batch_dir.rstrip(batch_dir[-1])
    # Set the new directory name for the zipped batch
    zipped_batch_dir = dir_to_zip + ".zip"

    # Get an iterator for all of the contents in the batch folder to be zipped
    zip_dir_contents = pathlib.Path(dir_to_zip)

    # start zip process
    with ZipFile(zipped_batch_dir, "w", ZIP_DEFLATED) as to_zip:
        # iterate over zip_dir_contents and add each one to the zip file
        for print_pdf in zip_dir_contents.iterdir():
            to_zip.write(print_pdf)

    # close zip file
    to_zip.close()

    return zipped_batch_dir


def close_import_status_window(import_status_window):
    """
    Accets the import status window as a tkinter object.
    Returns nothing.

    Closes the import_status_window and refreshes the status
    of each of the printers
    """

    import_status_window.destroy()
    refresh_printer_statuses()
