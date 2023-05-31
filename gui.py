# /Users/Trevor/Documents/Scripts/batch-forge python
# UI Script for Batch Forge

from glob import glob
from tkinter import *
from os import getcwd

from batch_sorting import *
from batching_window import batch_orders_window
from caldera_importing_window import caldera_import_window
from sorter_window import sort_zipped_packages_window
from wallpaper_sorter_functions import moveForDueDates
from wallpaper_sorter_variables import SORTING_DIR, DOWNLOAD_DIR

# Checks for config file and first-time setup
print(getcwd())

# Set Installation Directory. Don't actually know if I'll really need this.
installation_dir = "/Users/Trevor/Documents/Scripts/batch-forge/"
"""installation_dir = '/Users/caldera/Downloads/batch-forge-batching_gui/"""

# Startup sorting copy tree just to make my life easier
# while testing and developing.
caldera_path = "/Users/Trevor/Documents/Scripts/Misc/caldera/var/public/"
"""caldera_path = '/Users/caldera/Desktop/gui_testing/"""
downloadDir = caldera_path + "3 Downloaded/"
sortingDir = caldera_path + "5 Sorted for Print/"


# try:
#     shutil.rmtree(caldera_path + '5 Sorted for Print')
#     shutil.copytree(caldera_path + '5 Sorted for Print Copy',
#                     caldera_path + '5 Sorted for Print')
#     moveForDueDates(glob(SORTING_DIR + '**/*.pdf', recursive=True))
# except:
#     pass

sort_results = []

# Initilize TK and main menu window
root = Tk()
app_image = Image("photo", file=installation_dir + "assets/batch_forge_icon.png")
root.call("wm", "iconphoto", root._w, app_image)
root.title("Batch Forge")
root.geometry("300x350")
root.minsize(300, 350)
root.maxsize(300, 350)

main_menu_frame = LabelFrame(root, text="Main Menu", padx=10, pady=10)

main_menu_frame.pack(padx=10, pady=10)

button_sort_orders = Button(
    main_menu_frame,
    text="Sort Orders",
    width=20,
    height=2,
    command=lambda: sort_zipped_packages_window(root),
)

button_sort_orders.pack()

if len(glob(DOWNLOAD_DIR + "*.zip")) == 0:
    button_sort_orders["text"] = "No Orders to Sort"
    button_sort_orders["state"] = DISABLED

button_batch_orders = Button(
    main_menu_frame,
    text="Build-A-Batch",
    width=20,
    height=2,
    command=lambda: batch_orders_window(root),
).pack()

button_caldera_importer = (
    Button(
        main_menu_frame,
        text="Caldera Importer",
        width=20,
        height=2,
        command=lambda: caldera_import_window(root),
    ).pack(),
)

button_drive_downloader = Button(
    main_menu_frame, text="Download from Drive", width=20, height=2
).pack()

button_dates_update = Button(
    main_menu_frame,
    text="Update Sort for Due Dates",
    width=20,
    height=2,
    command=lambda: moveForDueDates(glob(SORTING_DIR + "**/*.pdf", recursive=True)),
).pack()

button_quit = Button(
    main_menu_frame, text="Quit Batch Forge", width=20, height=2, command=root.quit
).pack()

root.mainloop()
