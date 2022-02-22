import matplotlib.pyplot as plt
import csv

def graph_plotting(file_name):
    time = []
    branches = []
    cache_misses = []
    cache_reference = []
    instructions = []
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
            cache_misses.append(float(row[5]))
            cache_reference.append(float(row[4]))
            instructions.append(float(row[3]))
            line_no += 1
            
    # fig, ax1 = plt.subplots()

    # color = 'tab:red'
    # ax1.set_xlabel('Time')
    # ax1.set_ylabel()
    plt.plot(time, branches, label='branches')
    plt.plot(time, cache_misses, label='cache misses')
    plt.plot(time, cache_reference, label='cache reference')
    plt.plot(time, instructions, label='instructions')
    plt.xlabel('Time')
    plt.ylabel('Counts')
    plt.legend()
    plt.show()