#!/usr/bin/env python

"""
Plot Waveforms for AM, FM and PM modulation of binary codes
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

try:
    import matplotlib.pyplot as plt
except ImportError:
    logging.log(logging.ERROR, "Could not load PyPlot. Please download and install Matplotlib.")
    sys.exit(1)


def _plot_waveform(t, wave, subplot, fmt, label, steps):
    """
    Create Subplot for the given Waveform
    :param t: time array
    :param wave: wave amplitude array
    :param subplot: subplot index
    :param fmt: PyPlot format code
    :param label: label for legend
    :param steps: steps used in calculation
    """
    plt.subplot(subplot)
    plt.plot(t, wave, fmt, label=label)
    plt.xlim(0, len(wave) / steps)
    plt.vlines(t[::steps], -1.1, 1.1, ls="dotted")
    plt.ylim(-1.1, 1.1)
    plt.xticks([], [])
    plt.yticks([-1, 0, 1], [-1, 0, 1])


def plot_waveforms(values, t, am, fm, pm, target="show", filename=None):
    """
    Show or save waveform plots
    :param values: actual code to modulate
    :param t: time array
    :param am: wave array for amplitude modulation
    :param fm: wave array for frequency modulation
    :param pm: wave array for phase modulation
    :param target: "show" - display the plot, "file" - save the plot to the given file
    :param filename: file name to save the plot to, if target is "file"
    :raise RuntimeError: target and/or filename mismatch
    """
    steps = int(len(t) / len(values))
    plt.figure(figsize=(16, 8))
    plt.subplot(411)
    plt.title("\nModulations of {}\n".format("".join(values)))  # Newline needed for vertical space
    # Plot values (tricky as steps are unidirectional in mpl)
    t_ax = list(t[::steps])
    t_ax.append(t[-1])
    values_ax = [int(val) for val in values]
    values_ax.append(int(values[-1]))
    plt.plot(t_ax, values_ax, ds="steps-post", label="Data")
    plt.xlim(0, len(values))
    plt.vlines(t[::steps], -0.1, 1.1, ls="dotted")
    plt.ylim(-0.1, 1.1)
    plt.xticks([], [])
    plt.yticks([0, 1], [0, 1])
    for wave in ((am, 412, "g-", "AM"),
                 (fm, 413, "r-", "FM"),
                 (pm, 414, "c-", "PM")):
        _plot_waveform(t, *wave, steps)
    # Plot ticks
    plt.xticks([i for i in range(len(values) + 1)], [i for i in range(len(values) + 1)])
    plt.xlabel("Cycle")
    # Prettify the output and display legend
    plt.figlegend(loc=(0.4225, 0.025), ncol=4)
    plt.tight_layout(rect=(0.05, 0.05, 1, 1))
    if target == "show":
        plt.show()
    elif target == "file" and filename is not None:
        plt.savefig(filename)
    else:
        logging.log(logging.ERROR, "Could not reach target {}.".format(target))
        raise RuntimeError("Invalid target.")
