#!/usr/bin/env python

"""
Calculate Waveforms for AM, FM and PM modulation of binary codes
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
import math

try:
    import numpy
    slow = False
except ImportError:
    # The numpy implementation only takes 9 % of time in comparison with the native implementation
    # (sample size = 8000 bit)
    logging.log(logging.WARN, "Could not load numpy. Calculations will be astonishingly slow.")
    slow = True


def _waveforms_numpy(code, steps):
    """
    Calculate the waveforms for a given binary code using numpy
    :param code: code to modulate
    :param steps: steps per interval to calculate
    :return: tuple of time, am, fm and pm arrays
    """
    logging.log(logging.DEBUG,
                "Using NumPy to calculate waveforms for {} using {} steps per interval.".format("".join(code), steps))
    t = numpy.arange(0, len(code), 1 / steps)
    # Base sine curves
    sin_t = numpy.sin(t[:steps] * 2 * numpy.pi)
    sin_2t = numpy.sin(2 * t[:steps] * 2 * numpy.pi)
    # Amplitude Modulation
    am = numpy.empty_like(t)
    # Frequency Modulation
    fm = numpy.empty_like(t)
    # Phase Modulation
    pm = numpy.empty_like(t)
    phase_shift = False  # Initial shift
    for idx, val in enumerate(code):
        # Lower and Upper boundaries for this cycle's calculation
        # (attention: lower boundary inclusive, upper boundary exclusive)
        idx_low = idx * steps
        idx_high = (idx + 1) * steps
        # AM value is calculated by multiplying the value (shifted to specified levels, here 1 or 2) with the sine curve
        # and then normalizing the result
        am[idx_low:idx_high] = (int(val) + 1) / 2 * sin_t[:steps]
        # FM value is calculated by doubling the sine curve's frequency if the value is HIGH
        fm[idx_low:idx_high] = sin_2t[:steps] if int(val) else sin_t[:steps]
        # PM value is calculated by phase shifting the curve by 180° (== multiplying the curve with -1) if value is 0
        if idx > 0:
            # Phase shift if val == 0
            phase_shift = phase_shift ^ (not bool(int(val)))
        factor = -1 if phase_shift else 1
        pm[idx_low:idx_high] = factor * sin_t[:steps]
    return t, am, fm, pm


def _waveforms_native(code, steps):
    """
    Calculate the waveforms for a given binary code using Plain Python
    :param code: code to modulate
    :param steps: steps per interval to calculate
    :return: tuple of time, am, fm and pm arrays
    """
    logging.log(logging.DEBUG,
                "Using Python to calculate waveforms for {} using {} steps per interval.".format("".join(code), steps))
    # Time array
    # Pre-allocation, see https://stackoverflow.com/a/521688
    t = [0.0] * (steps * len(code))
    step_width = 1 / steps
    for idx in range(1, len(t)):
        t[idx] = t[idx - 1] + step_width
    # Base sine curves
    sin_t = [0.0] * steps
    sin_2t = [0.0] * steps
    for idx, t_i in enumerate(t[:steps]):
        sin_t[idx] = math.sin(t_i * 2 * math.pi)
        sin_2t[idx] = math.sin(2 * t_i * 2 * math.pi)
    # Amplitude Modulation
    am = [0.0] * len(t)
    # Frequency Modulation
    fm = [0.0] * len(t)
    # Phase Modulation
    pm = [0.0] * len(t)
    phase_shift = False  # Initial shift
    for idx, val in enumerate(code):
        # Lower and Upper boundaries for this cycle's calculation
        # (attention: lower boundary inclusive, upper boundary exclusive)
        idx_low = idx * steps
        idx_high = (idx + 1) * steps
        for i in range(idx_low, idx_high):
            # AM value is calculated by multiplying the value (shifted to specified levels, here 1 or 2) with the sine curve
            # and then normalizing the result
            am[i] = (int(val) + 1) / 2 * sin_t[i % steps]
            # FM value is calculated by doubling the sine curve's frequency if the value is HIGH
            fm[i] = sin_2t[i % steps] if int(val) else sin_t[i % steps]
            # PM value is calculated by phase shifting the curve by 180° (== multiplying the curve with -1) if value is 0
            if idx > 0:
                # Phase shift if val == 0
                phase_shift = phase_shift ^ (not bool(int(val)))
            factor = -1 if phase_shift else 1
            pm[i] = factor * sin_t[i % steps]
    return t, am, fm, pm


def waveforms(code, steps=200):
    """
    Calculate the waveforms for a given binary code
    :param code: code to modulate
    :param steps: steps per interval to calculate
    :return: tuple of time, am, fm and pm arrays
    """
    if slow:
        return _waveforms_native(code, steps)
    else:
        return _waveforms_numpy(code, steps)


def save(waves, filename):
    """
    Save given waveform arrays to file
    :param waves: array of times and waveforms (t, am, fm, pm)
    :param filename: filename to save this file to
    """
    if slow:
        with open(filename, "w") as file:
            file.write("# t [cycle] AM          FM          PM\n")
            for i in range(len(waves[0])):
                file.write(("{+9.8f} " * len(waves)).format(*waves).strip())
            file.write("# Created with Waveform Modulator, (c) 2020 Konstantin Köhring (@galaxy102), MIT license")
            file.close()
    else:
        numpy.savetxt(filename, numpy.array(waves).T, "%+9.8f", header="t [cycle] AM          FM          PM",
                      footer="Created with Waveform Modulator, (c) 2020 Konstantin Köhring (@galaxy102), MIT license")

