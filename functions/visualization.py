from fileinput import filename
import matplotlib.pyplot as plt
import csv
from scipy.signal import savgol_filter

def graph_plotting(file_name):
    time = []
    branches = []
    cache_misses = []
    cache_reference = []
    instructions = []
    cache_misses = []
    bus_cycles = []
    branch_loads = []
    # time, cycles, branches, instructions, cache-reference, cache - \
    #     misses, bus-cycles, branch-loads, iTLB-load-misse, dTLB-load-misse
    with open(file_name, 'r') as csvfile:
        csv_lines = csv.reader(csvfile, delimiter=',')
        line_no = 0
        for row in csv_lines:
            # if (line_no >= 20):
            #     break
            if (row[0]=='time'):
                continue
            time.append(float(row[0]))
            branches.append(float(row[2]))
            instructions.append(float(row[3]))
            cache_reference.append(float(row[4]))
            cache_misses.append(float(row[5]))
            bus_cycles.append(float(row[6]))
            branch_loads.append(float(row[7]))
            line_no += 1
            
    # fig, ax1 = plt.subplots()

    # color = 'tab:red'
    # ax1.set_xlabel('Time')
    # ax1.set_ylabel()
    if (len(branches)%2 == 0):
        window = len(branches) - 1
    else:
        window = len(branches)
    plt.plot(time, branches, label='branches')
    plt.plot(time, cache_misses, label='cache misses')
    plt.plot(time, cache_reference, label='cache reference')
    plt.plot(time, instructions, label='instructions')
    plt.plot(time, bus_cycles, label='bus cycles')
    plt.plot(time, branch_loads, label='branch loads')
    plt.xlabel('Time')
    plt.ylabel('Counts')
    plt.title(file_name.split("/")[1].split(".")[0])
    plt.legend()
    plt.show()
