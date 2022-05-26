# this is a paged allocation method
# random is used to randomized job's page to main memory

import math
import random


class Job:

    def __init__(self, jobId, job_size, pageSize):
        self.jobId = jobId
        self.size = job_size
        self.remaining = job_size
        self.page_size = pageSize
        self.status = 'in que'  # in que -> in process -> finished
        numberOfPage = math.trunc(job_size / pageSize)
        if job_size % pageSize != 0:
            numberOfPage += 1
        # Job Table in array form
        self.Page = [self.remaining_line() for k in range(numberOfPage)]
        # Page Map Table in array form
        self.PMT = ['' for pmt in range(numberOfPage)]  # page frame id in the list
        self.PMTStatus = ['N' for pmtS in range(numberOfPage)]
        self.lastPageInMemory = None

    def remaining_line(self):
        if self.remaining < self.page_size:
            return self.remaining
        else:
            self.remaining -= self.page_size
            return self.page_size

    def updatePageStat(self, pageNo, pageFrameNo):
        self.PMTStatus[pageNo] = 'Y'
        self.PMT[pageNo] = pageFrameNo

    def print_JTandPMT(self):
        to_print = "JOB " + str(self.jobId) + "\t\t\t\t\t\t" + "JOB " + str(self.jobId) + "  PMT\n"
        for j in range(len(self.Page)):
            to_print += "Page " + str(j) + "\t\t\t\t\t\t" + "P" + str(j) + ' ' + str(self.PMTStatus[j]) + '\t' + str(
                self.PMT[j]) + "\n"
        print(to_print)


class Memory:
    def __init__(self, numberOfPageFrame, pageSize):
        self.number_of_page_frame = numberOfPageFrame
        self.page_frame_size = pageSize
        # Memory Map Table
        self.page_frame = [None for p in range(numberOfPageFrame)]
        self.page_frameStatus = ['free' for f in range(numberOfPageFrame)]
        self.free_page_frame = [q for q in range(numberOfPageFrame)]
        self.jobInQue = list()

    def OSspace(self, OSspace):
        for i in range(OSspace + 1):
            self.page_frameStatus[i] = 'busy'
            self.free_page_frame.pop(0)
            self.page_frame[i] = 'OS\t'

    def addJobToQue(self, joB):
        self.jobInQue.append(joB)

    def allocate_job(self):
        if len(self.jobInQue) != 0:
            jobToAllocate = self.jobInQue[0]  # FCFS
            inMemory = 0
            for j in range(len(jobToAllocate.PMT)):
                if len(self.free_page_frame) != 0:
                    pageFrame = self.allocate_page(jobToAllocate.jobId, j)
                    self.jobInQue[0].updatePageStat(j, pageFrame)
                    inMemory += 1
                else:
                    break
            if inMemory == len(jobToAllocate.PMT):
                del self.jobInQue[0]

    def allocate_page(self, jobNumber, pageNumber):
        randomPageFrame = random.choice(self.free_page_frame)
        self.free_page_frame.remove(randomPageFrame)
        self.page_frameStatus[randomPageFrame] = 'busy'
        self.page_frame[randomPageFrame] = 'J' + str(jobNumber) + ' P' + str(pageNumber)
        return randomPageFrame

    def printMMT(self):
        to_print = "Main Memory\t\t" + "Page Frame\n"
        for PM in range(number_of_page_frame):
            to_print += str(self.page_frame[PM]) + "\t\t\t" + str(PM) + "\n"
        print(to_print)

    # def deallocate_job(self):


# Read input file and get the data
inputFile = open("paged input.txt", "r")
input_data = inputFile.readlines()
##############################################
# get number of size
for i in input_data[0].split():
    if i.isdigit():
        page_size = int(i)

# get number of jobs
for i in input_data[1].split():
    if i.isdigit():
        number_of_job = int(i)
job = ['' for x in range(number_of_job)]

# get number of page frame
for i in input_data[2].split():
    if i.isdigit():
        number_of_page_frame = int(i)

# get number of page frame occupied by OS
for i in input_data[3].split():
    if i.isdigit():
        OS_page_frame = int(i)

# get max job size
for i in input_data[4].split():
    if i.isdigit():
        max_jobSize = int(i)
################################################

# main code
memory = Memory(number_of_page_frame, page_size)
memory.OSspace(OS_page_frame)

t = 0
totalJobArrived = 0
while t < 100 and len(memory.free_page_frame) != 0:
    memory.allocate_job()
    memory.printMMT()
    jobArriveBool = random.randint(0, 1)
    # continuos random job arrive
    if jobArriveBool == 1 and totalJobArrived < number_of_job:
        ranJobSize = random.randint(1, max_jobSize + 1)
        job[totalJobArrived] = Job(totalJobArrived, ranJobSize, page_size)
        memory.addJobToQue(job[totalJobArrived])
        job[totalJobArrived].print_JTandPMT()
        totalJobArrived += 1

    t += 1

for p in range(number_of_job):
    if job[p] != '':
        job[p].print_JTandPMT()
print(memory.jobInQue)
