#! /usr/bin/python3

import sys
import os
import sh
import signal

PPRZ_HOME = os.getenv("PAPARAZZI_HOME", None)

toBeLaunched = []

# UAV components
toBeLaunched.append({'cmd':'sw/simulator/pprzsim-launch',
                     'output':'Lisa_Neph_0',
                     'options':['-a','Lisa_Neph_0','-t','nps']})


# Other components
toBeLaunched.append({'cmd':'sw/ground_segment/cockpit/gcs',
                     'output':'gcs',
                     'options':['-layout', 'large_left_col.xml']})
toBeLaunched.append({'cmd':'sw/ground_segment/tmtc/link',
                     'output':'link',
                     'options':['-udp', '-udp_broadcast']})
toBeLaunched.append({'cmd':'sw/ground_segment/tmtc/server',
                     'output':'server',
                     'options':['-n']})

outputDir = "output/"
# Creating a folder for simulation output
try:
    print("Creating output folder for stdout dump")
    os.makedirs(outputDir)
except FileExistsError as e:
    print("Output folder already exists. Skipping.", e)
    pass

processes = []
print("Starting simulation components")
for cmd in toBeLaunched:
    command = sh.Command(os.path.join(PPRZ_HOME, cmd['cmd']))
    command = command.bake(_bg=True, _bg_exc=False,
                           _out=os.path.join(outputDir, cmd['output'] + "_stdout.txt"),
                           _err=os.path.join(outputDir, cmd['output'] + "_stderr.txt"))
    for opt in cmd['options']:
        command = command.bake(opt)
    processes.append(command())
    print("Spawned " + cmd['cmd'] + ". pid:" + str(processes[-1].pid))
print("Simulation launched. Press ctrl-c to stop.")

def signal_handler(frame, sig):
    for proc in processes:
        print("Killing ", proc.pid, end="... ")
        try:
            proc.terminate()
        except ProcessLookupError as e:
            print("Already killed (exception feedback:",e,")")
            continue
        try:
            proc.wait()
        except sh.SignalException_SIGTERM:
            print("Success.")
    exit()
signal.signal(signal.SIGINT, signal_handler)
signal.pause()


