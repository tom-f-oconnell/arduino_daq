#!/usr/bin/env python

from __future__ import division
import signal
import sys
import serial
import time
import numpy as np
import pyqtgraph as pg
import datetime
import numpy as np

times = []
a0_data = []
a1_data = []

# TODO autoincrement filename
pw = pg.plot()

# this might not always fire when it should?
# see https://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python
def signal_handler(signum, frame):
    print('saving output in numpy npz format...')
    with open(datetime.datetime.now().strftime('%Y%m%d_%H%M%S_data.npz'),'wb') as f:
        np.savez(f, times=times, a0_data=a0_data, a1_data=a1_data)
    print('done.')
    pw.close()
    sys.exit(0)

def convert(x):
    # off by 1?
    scaled = 5 * int(x) / 2**10
    if scaled > 5 or scaled < 0:
        return np.nan
    else:
        return scaled

signal.signal(signal.SIGINT, signal_handler)

print('press Ctrl-C to exit and save the data')

# TODO need to sleep / delay here or in arduino to not run over
# stuff?
with serial.Serial('/dev/ttyACM0', 57600, timeout=1) as ser:
    start= time.time()
    while True:
        line = ser.readline()
        try:
            a0, a1 = line.split()
        except ValueError:
            continue
        a0_data.append(5 * int(a0) / 2**10)
        a1_data.append(5 * int(a1) / 2**10)
        times.append(time.time() - start)
        # get everything less than 20 seconds ago
        first = np.argwhere(np.array(times) > (times[-1] - 20))[0][0]
        pw.plot(times[first:], a0_data[first:], clear=True, pen='y')
        pw.plot(times[first:], a1_data[first:], pen='g')
        # why is this necessary?
        pg.QtGui.QApplication.processEvents()

