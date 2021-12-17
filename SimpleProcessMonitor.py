# https://www.geeksforgeeks.org/how-to-make-a-process-monitor-in-python/

import psutil
import time
from prettytable import PrettyTable
import click


click.clear()

# Run once to get an overview of system health (put in a while loop for constant monitoring)

print("============================== Process Monitor ======================================\n")

# Fetch the battery information
battery = psutil.sensors_battery().percent
print("----Battery Available: %d " % (battery,) + "%")

# We have used PrettyTable to print the data on console.
# t = PrettyTable(<list of headings>)
# t.add_row(<list of cells in row>)

# Fetch the Network information
print("----Networks----")
table = PrettyTable(['Network', 'Status', 'Speed'])
for key in psutil.net_if_stats().keys():
    name = key
    up = "Up" if psutil.net_if_stats()[key].isup else "Down"
    speed = psutil.net_if_stats()[key].speed
    table.add_row([name, up, speed])
print(table)

# Fetch the memory information
print("----Memory----")
memory_table = PrettyTable(["Total", "Used", "Available", "Percentage"])

vm = psutil.virtual_memory()
memory_table.add_row([
    vm.total,
    vm.used,
    vm.available,
    vm.percent
])

print(memory_table)

# Fetch the last 10 processes from available processes
print("----Processes----")
process_table = PrettyTable(['PID', 'PNAME', 'STATUS', 'CPU', 'NUM THREADS'])

for process in psutil.pids()[-10:]:

    # While fetching the processes, some may exit
    # Hence we need to put this code in try-except block
    try:
        p = psutil.Process(process)
        process_table.add_row([
            str(process),
            p.name(),
            p.status(),
            str(p.cpu_percent()) + "%",
            p.num_threads()
        ])

    except Exception as e:
        pass
print(process_table)

time.sleep(1)
