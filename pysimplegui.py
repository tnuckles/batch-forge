# GUI with PySimpleGUI

import PySimpleGUI as sg

# Create Layout
main_window = [
    [sg.Button('Sort \'Em')],
    [sg.Button('Batch Forge')],
    [sg.Button('Caldera Import')],
    [sg.Button('Transfer from Drive')],
    [sg.Button('Quit')]
]

# Create the window
window = sg.Window('Batch Forge', main_window)

while True:
    event, values = window.read()

    if event == 'Quit' or event == sg.WIN_CLOSED:
        break

window.close()