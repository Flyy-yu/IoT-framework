#!/usr/bin/env python
# coding=utf-8
"""
A sample application for cmd2.
Thanks to cmd2's built-in transcript testing capability, it also serves as a
test suite for example.py when used with the transcript_regex.txt transcript.
Running `python example.py -t transcript_regex.txt` will run all the commands in
the transcript against example.py, verifying that the output produced matches
the transcript.
"""

import random
import argparse
import os
import cmd2
from colorama import Fore

class IOT_App(cmd2.Cmd):
    degrees_c = 22
    sunny = False

    def __init__(self):
        self.prompt = "(Iot-Testing)> "
        self.settable.update({'degrees_c': 'Temperature in Celsius'})
        self.settable.update({'sunny': 'Is it sunny outside?'})
        super().__init__()

    def do_sunbathe(self, arg):
        if self.degrees_c < 20:
            result = "It's {} C - are you a penguin?".format(self.degrees_c)
        elif not self.sunny:
            result = 'Too dim.'
        else:
            result = 'UV is bad for your skin.'
        self.poutput(result)

    def _onchange_degrees_c(self, old, new):
        # if it's over 40C, it's gotta be sunny, right?
        if new > 40:
            self.sunny = True

if __name__ == '__main__':
    c = IOT_App()
    c.cmdloop()