#!/usr/bin/env python

"""
Waveform modulator for Bin, BCD and ASCII input to AM, FM and PM output
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

import lib.plot
import lib.gui
import lib.waveform
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Modulate Waveforms", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--nogui", help="Use CLI by preference", action="store_true")
    parser.add_argument("--steps", type=int, help="Steps to use for plotting per interval", default=200)
    parser.add_argument("--store-plot",
                        help="Create the waveform chart for the given formatted input.\n"
                             "The input is interpreted as Binary.\n"
                             "To trigger interpretation as 7-bit ASCII, prefix the input with a_.\n"
                             "To trigger interpretation as 4-bit BCD, prefix the input with d_.\n"
                             "The file will be saved as wave_INPUT.png to the current directory.",
                        action="store", metavar="INPUT", type=str)
    parser.add_argument("--store-wave",
                        help="Create the waveform data for the given formatted input.\n"
                             "The input is interpreted as Binary.\n"
                             "To trigger interpretation as 7-bit ASCII, prefix the input with a_.\n"
                             "To trigger interpretation as 4-bit BCD, prefix the input with d_.\n"
                             "The file will be saved as wave_INPUT.txt to the current directory.",
                        action="store", metavar="INPUT", type=str)
    args = parser.parse_args()
    if args.store_plot is not None and args.store_wave is not None:
        print("Please decide for either plotting or storing the waveform.")
    if args.store_plot is None and args.store_wave is None:
        lib.gui.start(lambda inp: lib.plot.plot_waveforms(inp, *lib.waveform.waveforms(inp, steps=args.steps)),
                      force_nogui=args.nogui)
    elif args.store_wave is None:
        inp = lib.gui._evaluate_input(args.store_plot)
        lib.plot.plot_waveforms(inp, *lib.waveform.waveforms(inp, steps=args.steps),
                                target="file", filename="wave_{}.png".format(args.store_plot))
    else:
        inp = lib.gui._evaluate_input(args.store_wave)
        lib.waveform.save(lib.waveform.waveforms(inp, steps=args.steps), filename="wave_{}.txt".format(args.store_wave))
