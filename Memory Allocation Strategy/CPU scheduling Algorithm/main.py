#CPU Scheduling Algo : FCFS X SJN simulation
import csv
import pandas as pd
import random

# Get data from file
df = pd.read_csv("input.csv")
print(df.to_string())
numberOfProcess = df["Number of process"][0]
burstStart = df["burst time start"][0]
burstEnd = df["burst time end"][0]
timeLimit = df["time limit"][0]

#initialize shared data between FCFS and SJN
process = [0 for x in range(0,numberOfProcess)]
arrivalTime = [0 for x in range(numberOfProcess)]
t = 0

i = 0
start = 0
end = 0

# initialise data (SJN)
finishTimeSJN = [0 for x in range(numberOfProcess)]
processedSJN = numberOfProcess
queSJN = list()
runningProcessSJN = 0
currentRuntimeSJN = 0

# initialise data (FCFS)
finishTimeFCFS = [0 for x in range(numberOfProcess)]
processedFCFS = numberOfProcess
queFCFS = list()
runningProcessFCFS = 0
currentRuntimeFCFS = 0


# print("Time\tProcess arived\tRunning\t\t\tIn que")
print("Time\tProcess arived\tRunning SJN\t\tRunning FCFS\t\t")
print(" ")

while processedFCFS > 0 or processedSJN > 0 and t < timeLimit:

    # print for running process (FCFS)
    prinTRunTimeFCFS = ""
    if currentRuntimeFCFS != 0:
        prinTRunTimeFCFS += "P" + str(runningProcessFCFS - 1) + "[" + str(currentRuntimeFCFS - 1) + "]" + "\t\t\t"
        currentRuntimeFCFS -= 1
        if currentRuntimeFCFS == 0 and process[runningProcessFCFS - 1] > 0 and processedFCFS > 0:
            finishTimeFCFS[runningProcessFCFS - 1] = t
            processedFCFS -= 1
    else:
        prinTRunTimeFCFS += "-\t\t\t\t"

    # print for running process (SJN)
    prinTRunTimeSJN =""
    if currentRuntimeSJN != 0:
        prinTRunTimeSJN += "P" + str(runningProcessSJN-1) + "[" + str(currentRuntimeSJN-1) + "]" + "\t\t\t"
        currentRuntimeSJN -= 1
        if currentRuntimeSJN == 0 and process[runningProcessSJN-1] > 0 and processedSJN > 0:
            finishTimeSJN[runningProcessSJN-1] = t
            processedSJN -= 1
    else:
        prinTRunTimeSJN += "-\t\t\t\t"

    # random time process arrival (determine either the a process is arrived or not)
    if i < numberOfProcess:
        processArrive = random.getrandbits(1)
        addProcess = {}
        if processArrive == 1 and i < numberOfProcess:
            process[i] = random.randint(burstStart, burstEnd)
            arrivalTime[i] = t
            addProcess = {"process": i, "runningTime": process[i]}
            queSJN.append(addProcess) # add to SJN que
            queFCFS.append(addProcess) # add to FCFS Que
            i += 1

    # print(get the current que)
    printQueFCFS = "FCFS_que:" + str(",".join(["P"+str(queFCFS[i]["process"])+"("+str(queFCFS[i]["runningTime"]) +")" for i in range(len(queFCFS))]))
    printQueSJN = "\tSJN_que:" + str(",".join(["P"+str(queSJN[i]["process"])+"("+str(queSJN[i]["runningTime"]) +")" for i in range(len(queSJN))]))

    # get next running process for FCFS
    if currentRuntimeFCFS == 0:
        if len(queFCFS) != 0:
            currentRuntimeFCFS = queFCFS[0]["runningTime"]
            runningProcessFCFS = queFCFS[0]["process"] + 1
            del queFCFS[0]
        elif len(queFCFS) == 1:
            currentRuntimeFCFS = queFCFS[0]["runningTime"]
            runningProcessFCFS = queFCFS[0]["process"] + 1
            del queFCFS[0]

    # get next running process for SJN
    if currentRuntimeSJN == 0:
        if len(queSJN) != 0:
            minimum = 0
            for x in range(1, len(queSJN)):
                if queSJN[x]["runningTime"] < queSJN[minimum]["runningTime"]:
                    minimum = x
            currentRuntimeSJN = queSJN[minimum]["runningTime"]
            runningProcessSJN = queSJN[minimum]["process"] + 1
            del queSJN[minimum]
        elif len(queSJN) == 1:
            currentRuntimeSJN = queSJN[0]["runningTime"]
            runningProcessSJN = queSJN[0]["process"] + 1
            del queSJN[0]



    # print for time t update
    toPrint = "T" + str(t) + "\t\t"

    # print the arrived process
    if processArrive == 1:
        toPrint += "P" + str(i-1) + "[" + str(process[i-1]) + "]\t\t\t"
        if i == numberOfProcess:
            processArrive = 0
    else:
        toPrint += "-\t\t\t\t"

    toPrint += prinTRunTimeFCFS + prinTRunTimeSJN + printQueFCFS + printQueSJN



    print(toPrint)
    # increase the time
    t = t + 1


"""COMPUTATION"""
#Turnaround time FCFS
TAT_FCFS = [finishTimeFCFS[x]-arrivalTime[x] for x in range(numberOfProcess)]
ave_TAT_FCFS = sum(TAT_FCFS)/numberOfProcess

#Turnaround time SJN
TAT_SJN = [finishTimeSJN[x]-arrivalTime[x] for x in range(numberOfProcess)]
ave_TAT_SJN = sum(TAT_SJN)/numberOfProcess

#waiting time FCFS
waiting_time_FCFS = [TAT_FCFS[x]-process[x] for x in range(numberOfProcess)]
ave_wt_FCFS = sum(waiting_time_FCFS)/numberOfProcess

#waiting time SJN
waiting_time_SJN = [TAT_SJN[x]-process[x] for x in range(numberOfProcess)]
ave_wt_SJN = sum(waiting_time_SJN)/numberOfProcess

print(" ")
print("___________________________________________________________________________________________________________________________ ")
print("Process \t\t\t" + str([x for x in range(1,numberOfProcess+1)]))
print("Running time\t\t" + str(process))
print("arrival time\t\t" + str(arrivalTime))
print(" ")
print(" ")
print("finish time SJN\t\t\t" + str(finishTimeSJN))
print("finish time FCFS\t\t\t" + str(finishTimeFCFS))
print(" ")
print("turnaround time(TAT) SJN" + str(TAT_SJN))
print("turnaround time(TAT) FCFS" + str(TAT_FCFS))
print(" ")
print("waiting time SJN\t\t" + str(waiting_time_SJN))
print("waiting time FCFS\t\t" + str(waiting_time_FCFS))
print(" ")
print("Average TAT SJN = " + str(ave_TAT_SJN))
print("Average TAT FCFS = " + str(ave_TAT_FCFS))
print(" ")
print("average waiting time SJN = " + str(ave_wt_SJN))
print("average waiting time FCFS = " + str(ave_wt_FCFS))
print(" ")
print("total running time = " + str(sum(process)))

print("___________________________________________________________________________________________________________________________ ")
#store output to local file
#create data
with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Process", "Arrival Time", "Service Time", "Finish Time(FCFS)", "Finish Time(SJN) ", "Turnaround Time(FCFS)", "Turnaround Time(SJN)", "Waiting Time(FCFS)", "Waiting Time(SJN)"])
    for i in range(numberOfProcess):
        writer.writerow([i+1, arrivalTime[i], process[i], finishTimeFCFS[i], finishTimeSJN[i], TAT_FCFS[i], TAT_SJN[i], waiting_time_FCFS[i], waiting_time_SJN[i]])

