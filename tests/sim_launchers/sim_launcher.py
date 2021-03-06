#! /usr/bin/python3

import sys
import os
import sh
import signal
import argparse

PPRZ_HOME = os.getenv("PAPARAZZI_HOME", None)

parser = argparse.ArgumentParser(description='Helepr to launch paparazzi simulations, with the sim simulator.')
parser.add_argument('-o','--output', dest='output', type=str, default=None,
                    help="Output folder where to write stdout and stderr of launched components. (default is /dev/null)")
parser.add_argument('aircrafts', type=str, nargs='*',
                    help="Aircrafts to be launched")
args = parser.parse_args()

toBeLaunched = []

# UAV components
for uav in args.aircrafts:
    toBeLaunched.append({'cmd':'sw/simulator/pprzsim-launch',
                         'output':uav,
                         'options':['-a', uav,'-t','sim', '--boot', '--norc']})


# Other components
toBeLaunched.append({'cmd':'sw/ground_segment/cockpit/gcs',
                     'output':'gcs',
                     'options':['-layout', 'large_left_col.xml']})
toBeLaunched.append({'cmd':'sw/ground_segment/tmtc/server',
                     'output':'server',
                     'options':['-n']})

# Not needed with sim type simulation
# toBeLaunched.append({'cmd':'sw/ground_segment/tmtc/link',
#                      'output':'link',
#                      'options':['-udp', '-udp_broadcast']})

# Creating a folder for simulation output
if args.output is not None:
    try:
        print("Creating output folder for stdout dump")
        os.makedirs(args.output)
    except FileExistsError as e:
        print("Output folder already exists. Skipping.", e)
        pass

processes = []
print("Starting simulation components")
for cmd in toBeLaunched:
    command = sh.Command(os.path.join(PPRZ_HOME, cmd['cmd']))
    command = command.bake(_bg=True, _bg_exc=False)
    if args.output is not None:
        command = command.bake(_out=os.path.join(args.output, cmd['output'] + "_stdout.txt"),
                               _err=os.path.join(args.output, cmd['output'] + "_stderr.txt"))
    else:
        command = command.bake(_out="/dev/null", _err="/dev/null")
                               

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


