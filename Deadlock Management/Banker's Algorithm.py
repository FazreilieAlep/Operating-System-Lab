# Deadlock Avoidance

import random


class Job:
    def __init__(self, jobID, burst_time, device_allocated):
        self.jobID = jobID
        self.burst_time = random.randint(1, burst_time)
        self.device_allocated = device_allocated
        self.maximum_required = random.randint(device_allocated,
                                               device_allocated + 5)  # predict it will need up to 5 more space
        self.remaining_needs = self.maximum_required - self.device_allocated


class Bankers:
    def __init__(self, total_device):
        self.JobList = list()
        self.total_device = total_device
        self.unsafeState = total_device - ((20/100)*total_device)
        self.totalDeviceUsed = 0

    def addNewJob(self, newJob):
        self.JobList.append(newJob)
        self.totalDeviceUsed += newJob.device_allocated

    def random_Device_Deallocation(self):
        to_print = 'device deallocated : '
        for i in range(len(self.JobList)):
            x = random.randint(0, self.JobList[i].device_allocated)
            if x != 0:
                self.JobList[i].device_allocated -= x
                self.JobList[i].remaining_needs += x
                self.totalDeviceUsed -= x
                to_print += 'J' + str(i) + '(' + str(x) + ')    '
        print(to_print)

    def random_Device_Allocation_Request(self):
        for job in self.JobList:
            x = random.randint(1, 5)
            print("J" + str(job.jobID) + " request " + str(x) + " device")
            deviceAllocated = job.device_allocated + x
            tempTotalDeviceUsed = self.totalDeviceUsed + x
            if tempTotalDeviceUsed <= self.total_device and deviceAllocated <= job.maximum_required:
                print("device allocated ")
                job.device_allocated += x
                job.remaining_needs -= x
                self.totalDeviceUsed += x
            else:
                print("cannot allocate. request dropped ")

    def bankState(self):
        if self.totalDeviceUsed >= self.unsafeState:
            print("unsafe state ")
        else:
            print("safe state ")

    def printBankStatement(self):
        to_print = '*****************************************************************************'
        to_print += '\nJob No\tDevices Allocated\tMaximum Required\tRemaining Needs\n'
        to_print += '*****************************************************************************\n'
        for i in range(len(self.JobList)):
            to_print += str(i) + '\t\t\t' + str(self.JobList[i].device_allocated) + '\t\t\t\t\t' + str(self.JobList[i].maximum_required) + '\t\t\t\t\t' + str(self.JobList[i].remaining_needs) + '\n'
        to_print += '*****************************************************************************\n'
        to_print += '\n\nTotal Device Used : ' + str(self.totalDeviceUsed)
        to_print += '\nTotal Device : ' + str(self.total_device)
        print(to_print)
        self.bankState()


"""------------------------------------------------------"""
# Read input file and get the data
inputFile = open("input file.txt", "r")
input_data = inputFile.readlines()

for i in input_data[0].split():
    if i.isdigit():
        max_time = int(i)

for i in input_data[1].split():
    if i.isdigit():
        totalNumberOfDevice = int(i)

for i in input_data[2].split():
    if i.isdigit():
        number_of_job = int(i)

for i in input_data[3].split():
    if i.isdigit():
        max_burst_time = int(i) # not used

"""------------------------------------------------------"""
bank = Bankers(totalNumberOfDevice)
max_device_allocated = random.randint(5, totalNumberOfDevice-5) # obviously cannot exceed the totalNumberOfDevice the bank have
t = 0
totalJobArrived = 0

while t < max_time:
    bank.random_Device_Allocation_Request() # assume same job(or customer) will need other devices
    jobArriveBool = random.randint(0, 1)
    # continuos random jobInvoved arrive
    if jobArriveBool == 1 and totalJobArrived < number_of_job + 1:
        newJob = Job(totalJobArrived, max_burst_time, max_device_allocated)
        if bank.totalDeviceUsed + newJob.device_allocated < bank.total_device:
            # print('J' + str(totalJobArrived) + ' arrived')
            bank.addNewJob(newJob)
            totalJobArrived += 1
    bank.printBankStatement()
    bank.random_Device_Deallocation()
    print('_________________________________________________________________________________\n')
    t += 1

