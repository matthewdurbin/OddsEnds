# -*- coding: utf-8 -*-
"""
Simple script to control an Arduino for the purposes 
of tracking temperature with a TPM36 probe
LED blinks each time temp is recorded
Author: Matthew Durbin
"""
import pyfirmata as pf
import time
import numpy as np
import matplotlib.pyplot as plt

board = pf.Arduino("COM3")
it = pf.util.Iterator(board)
it.start()

analog_input = board.get_pin("a:0:i")  # set input to a0

temps = np.empty(0)

start_time = time.strftime("%X %x")
delay = 10

# tpm36 version
while True:
    av = analog_input.read()  # analog value of analog input (measure V)
    board.digital[13].write(1)  # turn LED on
    time.sleep(0.1)  # delay .1 seconds
    board.digital[13].write(0)  # turn LED off
    if av == None:
        av = 0.1
        continue
    t = (av * 5 - 0.5) * 100  # convert voltage to temp
    tc = np.round(t, 2)
    tf = np.round(9 * t / 5 + 32, 2)
    print("Current Temperature in C/F: ", tc, "/", tf)
    temps = np.append(temps, t)
    time.sleep(delay - 0.1)
