#!/usr/bin/env python

"""
(G)UI for waveform plotter
"""
# Published under the MIT license
#
# Copyright 2020 Konstantin Köhring (@galaxy102)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
# to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions
# of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
import sys
import re

# Try starting GUI, else use text input
try:
    import tkinter
    import tkinter.messagebox

    gui = True
except ImportError:
    gui = False
    logging.log(logging.ERROR, "Could not load GUI module. Is tkinter installed?")
    logging.log(logging.ERROR, "Falling back to text input.")

# First Run flag for CLI to display header
_first_run = True

# Background Color for GUI
_BG_COLOR = "darkgray"

# Patterns for input evaluation
_BINARY_PATTERN = re.compile("[01]+")
_ASCII_PATTERN = re.compile("a_.+", flags=re.ASCII)
_DECIMAL_PATTERN = re.compile("d_\d+")

# Translation from human readable types to machine readable prefixes
_PRE_MAP = {"1-bit Binary":               "",
            "4-bit Binary Coded Decimal": "d_",
            "7-bit ASCII":                "a_"}


def _evaluate_btn(pre: tkinter.StringVar, inp: tkinter.Entry):
    """
    Evaluate the GUI content
    :param pre: Prefix selector
    :param inp: Input Field
    :return: evaluated GUI content
    """
    prefix = pre.get()
    for key in _PRE_MAP.keys():
        prefix = prefix.replace(key, _PRE_MAP[key])
    return _evaluate_input(prefix + inp.get())


def _evaluate_input(inp):
    """
    Evaluate a given text string (eventually containing a prefix)
    :param inp: [|d_|a_] + text input. No prefix means interpretation as binary, d_ means BCD, a_ means ASCII
    :return: tuple of bit-representation of the input string
    :raise ValueError: Malformed input
    """
    # Initialize output
    bit_string = None
    if re.fullmatch(_BINARY_PATTERN, inp):
        # Detected bin
        bit_string = inp
    elif re.fullmatch(_ASCII_PATTERN, inp):
        # Detected ASCII
        bit_string = ""
        for i in inp[2:]:
            bit_string += "{:07b}".format(ord(i))
    elif re.fullmatch(_DECIMAL_PATTERN, inp):
        # Detected BCD
        bit_string = ""
        for i in inp[2:]:
            bit_string += "{:04b}".format(int(i))
    if bit_string is not None:
        # Evaluation successful
        logging.log(logging.DEBUG, "Evaluated {} to {}.".format(inp, bit_string))
        return tuple(bit_string)
    else:
        # Evaluation failed
        logging.log(logging.WARN, "Could not evaluate {}.".format(inp))
        raise ValueError("Invalid input.")


def _nogui(callback):
    """
    Run the CLI
    :param callback: function to call on end of input
    """
    global _first_run
    if _first_run:
        print("##############################################")
        print(u"#  \u001b[32mAM FM PM Modulation Calculator\u001b[0m            #")
        print("#  (c) 2020 Konstantin Köhring (@galaxy102)  #")
        print("#           Published under the MIT license  #")
        print("##############################################")
        print("#  Usage: End with <Ctrl> + C + <Return>     #")
        print("#         Insert the code, press <Return>    #")
        print("#  If the code is not binary, prefix it:     #")
        print("#  a_: Use ASCII-to-bin conversion (7 bit)   #")
        print("#  d_: Use BCD conversion          (4 bit)   #")
        print("##############################################")
        _first_run = False
    while True:
        print("#                                            #", end="\u001b[43D")
        try:
            user_input = input("Code: ")
            print("#                                            #")
            print("##############################################", end="\u001b[1A\u001b[43D")
            try:
                machine_input = _evaluate_input(user_input)
                # No exception during handling input
                print("Input okay. Starting plot.")
                callback(machine_input)
            except ValueError as e:
                print(str(e))
            print("\u001b[1B")
        except KeyboardInterrupt:
            logging.log(logging.DEBUG, "Received SIGINT, terminating.")
            print("#  Leaving.                                  #")
            print("##############################################")
            sys.exit(130)


def _gui(callback):
    """
    Run the GUI
    :param callback: function to call on end of input
    """
    main = tkinter.Tk()
    main.title("Waveform Modulator")
    main.geometry("640x480")
    main.configure(background=_BG_COLOR)
    main.report_callback_exception = lambda e, v, tb: tkinter.messagebox.showerror("Error", str(v))
    head = tkinter.Frame(main, background=_BG_COLOR)
    tkinter.Label(head, text="Waveform Modulator", font="-size 24", background=_BG_COLOR).pack(pady=5)
    tkinter.Label(head, text="(c) 2020 Konstantin Köhring, MIT license", font="-size 8", background=_BG_COLOR).pack(
        pady=5)
    tkinter.Label(head, text="", background=_BG_COLOR).pack(pady=5)
    head.pack(pady=25)
    inp = tkinter.Frame(main, width=400, height=20, background=_BG_COLOR)
    inp.pack_propagate(False)
    tkinter.Label(inp, text="To Modulate:", font="-size 14", background=_BG_COLOR).pack(side=tkinter.LEFT)
    entry = tkinter.Entry(inp, width=30)
    entry.pack(side=tkinter.RIGHT)
    inp.pack(expand=False)
    sel = tkinter.Frame(main, width=400, height=200, background=_BG_COLOR)
    sel.pack_propagate(False)
    tkinter.Label(sel, text="Encoding:", font="-size 14", background=_BG_COLOR).pack(side=tkinter.LEFT)
    prefix = tkinter.StringVar()
    prefix.set("1-bit Binary")
    op = tkinter.OptionMenu(sel, prefix, "1-bit Binary", "4-bit Binary Coded Decimal", "7-bit ASCII")
    op.configure(width=30)
    op.pack(side=tkinter.RIGHT)
    sel.pack()
    exe = tkinter.Frame(main, width=400, height=40, background=_BG_COLOR)
    exe.pack_propagate(False)
    tkinter.Button(exe, text="Calculate", command=lambda: callback(_evaluate_btn(prefix, entry))).pack(
        side=tkinter.LEFT, expand=True, fill="x")
    tkinter.Label(exe, text="", background=_BG_COLOR).pack(padx=5, side=tkinter.LEFT)
    tkinter.Button(exe, text="Quit", command=lambda: sys.exit(0)).pack(side=tkinter.RIGHT, expand=True, fill="x")
    exe.pack()
    entry.focus()
    main.resizable(width=False, height=False)
    main.bind("<Return>", lambda x: callback(_evaluate_btn(prefix, entry)))
    main.bind("<KP_Enter>", lambda x: callback(_evaluate_btn(prefix, entry)))
    main.mainloop()


def start(callback, force_nogui=False):
    """
    Start CLI or GUI
    :param callback: function to call on end of input
    :param force_nogui: True if CLI should be used
    """
    logging.log(logging.DEBUG, "Starting UI.")
    if gui and not force_nogui:
        logging.log(logging.DEBUG, "Using GUI.")
        _gui(callback)
    else:
        logging.log(logging.DEBUG, "Using CLI.")
        _nogui(callback)
