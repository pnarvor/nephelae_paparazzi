#! /usr/bin/python3

import sys
sys.path.append('../')
import os
import signal

from ivy.std_api import *
import logging

import nephelae_pprzinterface as ppint

interface = ppint.PprzInterface()
interface.start()

signal.signal(signal.SIGINT, lambda sig,fr: interface.stop())
