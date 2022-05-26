# This code do Paged Memory Allocation simulation with a random Job arrival and random page or process burst time
# User can select either FCFS or SJN for Allocation Algo at line 309
# The system works on FIFO and free page frame for the page replacement policy (in this case the deallocationProcess() function)
import math
import random


class Job:
    def __init__(self, jobID, jobSize, pageSize, max_burst_time):
        self.jobID = jobID
        self.jobSize = jobSize
        self.remaining = jobSize
        self.jobStatus = 'Hold'
        self.pageSize = pageSize
        self.number_of_page = math.trunc(jobSize / pageSize)
        if jobSize % pageSize != 0:
            self.number_of_page += 1
        self.page = [[jobID, i, self.pageSizeInit(), random.randint(1, max_burst_time), 0, 'N'] for i in
                     range(self.number_of_page)]  # [jobid,pageid,pageSize,burst_time,counter,pageStatus]
        self.processedPage = 0

    def pageSizeInit(self):
        if self.remaining < self.pageSize:
            return self.remaining
        else:
            self.remaining -= self.pageSize
            return self.pageSize


# buffer data , hold in que processes
class ProcessBuffer:
    def __init__(self):
        self.in_que_head = None
        self.in_que_tail = None

    def addProcessToQue(self, jobID, pageID, burst_time, algoBool):  # True = FCFS, False = SJN
        newProcess = process(jobID, pageID, burst_time)
        if self.in_que_head is None:
            self.in_que_head = newProcess
            self.in_que_tail = self.in_que_head
        else:
            if algoBool is True:  # FCFS
                if self.in_que_head.nextProcess is None:
                    self.in_que_head.nextProcess = newProcess
                    self.in_que_tail = self.in_que_head.nextProcess
                else:
                    self.in_que_tail.nextProcess = newProcess
                    self.in_que_tail = self.in_que_tail.nextProcess
            else:  # SJN
                if self.in_que_head.burst_time > newProcess.burst_time:
                    temp = self.in_que_head
                    newProcess.nextProcess = temp
                    self.in_que_head = newProcess
                else:
                    pointer = self.in_que_head
                    # sort by burst time
                    while pointer.nextProcess is not None and pointer.nextProcess.burst_time < newProcess.burst_time:
                        pointer = pointer.nextProcess
                    # sort by Job
                    while pointer.nextProcess is not None and pointer.nextProcess.jobID < newProcess.jobID:
                        pointer = pointer.nextProcess
                    # sort by Page
                    while pointer.nextProcess is not None and pointer.nextProcess.pageID < newProcess.pageID and pointer.nextProcess.burst_time == newProcess.burst_time:
                        pointer = pointer.nextProcess
                    newProcess.nextProcess = pointer.nextProcess
                    pointer.nextProcess = newProcess

    def removeFirstProcessFromQue(self):  # already sorted linked list
        if self.in_que_head.nextProcess is None:
            self.in_que_head = None
            self.in_que_tail = self.in_que_head
        else:
            self.in_que_head = self.in_que_head.nextProcess


class freePageFrame:
    def __init__(self, pageFrameAdd, pageCounter):
        self.pageFrameAdd = pageFrameAdd
        self.pageCounter = pageCounter
        self.nextFreePageFrame = None


class process:
    def __init__(self, jobID, pageID, burst_time):
        self.jobID = jobID
        self.pageID = pageID
        self.burst_time = burst_time
        self.nextProcess = None


# active data
class Main_Memory:
    def __init__(self, number_of_pageFrame, OSSpace):
        self.number_of_pageFrame = number_of_pageFrame
        self.page_frame = [[i, '-', '-', 'free', 0, 0] for i in range(
            number_of_pageFrame)]  # [pageFrameAddress,inPageFrameJob, inPageFrameProcess,pageFrameStatus,counter,burst_counter]
        self.free_memory = 0
        self.OSspace = OSSpace
        self.PMT = [[0, 0, pmt] for pmt in range(number_of_page_frame)]
        self.InitOSspace(OSSpace)
        self.inMemoryPageCounter = 0
        self.initPageCounter()
        self.free_memory_buffer_head = None  # linked list to arrange free list  based on it counter(for FIFO implementation) # act as the Head Of the list
        self.initFreeMemoryBuffer()
        self.in_que_process_buffer = ProcessBuffer()
        self.job_list = list()

    def InitOSspace(self, OSSpace):
        for os in range(OSSpace):
            self.page_frame[os] = [os, 'OS', '-', 'busy', 'x', 'x']
            self.PMT[os] = ['-', '-', os]

    def initPageCounter(self):
        r = [i for i in range(0, self.number_of_pageFrame - self.OSspace)]
        self.inMemoryPageCounter = len(r)
        for i in range(self.OSspace, self.number_of_pageFrame):
            ran = random.choice(r)
            self.page_frame[i][4] = ran
            r.remove(ran)

    def initFreeMemoryBuffer(self):
        for x in range(self.OSspace, self.number_of_pageFrame):
            self.addFreePageFrame(self.page_frame[x][0], self.page_frame[x][4])
            self.free_memory += 1

    def addFreePageFrame(self, pageFrameAdd, pageCounter):  # sorted based on pageCounter for FIFO
        newFreePageFrame = freePageFrame(pageFrameAdd, pageCounter)
        if self.free_memory_buffer_head is None:
            self.free_memory_buffer_head = newFreePageFrame
        elif self.free_memory_buffer_head.pageCounter > newFreePageFrame.pageCounter:
            temp = self.free_memory_buffer_head
            newFreePageFrame.nextFreePageFrame = temp
            self.free_memory_buffer_head = newFreePageFrame
        else:
            pointer = self.free_memory_buffer_head
            while pointer.nextFreePageFrame is not None and pointer.nextFreePageFrame.pageCounter < newFreePageFrame.pageCounter:
                pointer = pointer.nextFreePageFrame
            newFreePageFrame.nextFreePageFrame = pointer.nextFreePageFrame
            pointer.nextFreePageFrame = newFreePageFrame

    def removeFirstFreePageFrame(self):  # FIFO
        self.free_memory_buffer_head = self.free_memory_buffer_head.nextFreePageFrame
        self.free_memory -= 1

    def allocateProcess(self):
        while self.in_que_process_buffer.in_que_head is not None:
            if self.in_que_process_buffer.in_que_head is not None and self.free_memory_buffer_head:
                # get the pageFrameAddress,inPageFrame,pageFrameStatus,counter,burst_counter to allocate the page frame
                # jobID, pageID, burst_time from the in_que_process_buffer
                # pageFrameAddress from free_memory_buffer_head
                # counter is the inMemoryPageCounter

                pageFrameAddress = self.free_memory_buffer_head.pageFrameAdd
                inPageFrameJob = self.in_que_process_buffer.in_que_head.jobID
                inPageFrameProcess = self.in_que_process_buffer.in_que_head.pageID
                pageFrameStatus = 'busy'
                counter = self.inMemoryPageCounter
                burst_counter = self.in_que_process_buffer.in_que_head.burst_time

                # update the page which was still in memory
                if self.page_frame[pageFrameAddress][2] != '-':
                    self.updatePage(self.page_frame[pageFrameAddress][1], self.page_frame[pageFrameAddress][2],'N')  # update previous page status

                # update the page_frame[pageFrameAddress]
                self.page_frame[pageFrameAddress] = [pageFrameAddress, inPageFrameJob, inPageFrameProcess,
                                                     pageFrameStatus, counter,
                                                     burst_counter]

                # update the job(hold -> running) and job page(N -> Y) status
                self.updateJob(self.in_que_process_buffer.in_que_head.jobID, 'Running')
                self.updatePage(self.in_que_process_buffer.in_que_head.jobID,
                                self.in_que_process_buffer.in_que_head.pageID, 'Y')

                # update the PMT table
                self.PMT[pageFrameAddress] = [self.in_que_process_buffer.in_que_head.jobID,
                                              self.in_que_process_buffer.in_que_head.pageID, pageFrameAddress]

                # update necessary things
                self.job_list[inPageFrameJob].processedPage += 1
                self.inMemoryPageCounter += 1
                self.free_memory -= 1

                # removing First from que
                self.removeFirstFreePageFrame()
                self.in_que_process_buffer.removeFirstProcessFromQue()
            else:
                break

    def deallocateProcess(
            self):  # update the page frame status to 'free' and add the free pageframe to the freeMemoryQue, update the jobStatus
        for x in range(self.OSspace, self.number_of_pageFrame):
            if self.page_frame[x][5] > 0:
                self.page_frame[x][5] -= 1  # reduce burst counter
            elif self.page_frame[x][3] != 'free':
                self.page_frame[x][3] = 'free'  # update page frame status
                # self.updatePage(self.page_frame[x][1], self.page_frame[x][2], 'N')  # update page status
                if self.job_list[self.page_frame[x][1]].processedPage == self.job_list[
                    self.page_frame[x][1]].number_of_page:
                    self.updateJob(self.page_frame[x][1], 'finished')  # update job status
                self.addFreePageFrame(self.page_frame[x][0], self.page_frame[x][4])
                self.free_memory += 1

                # update PMT
                self.PMT[x] = ['-', '-', x]
            else:
                continue

    def updatePage(self, jobID, pageID, pageStatus):
        self.job_list[jobID].page[pageID][5] = pageStatus

    def updateJob(self, jobID, jobStatus):
        if self.job_list[jobID].jobStatus != jobStatus:
            self.job_list[jobID].jobStatus = jobStatus

    def printMMT(self):
        to_print = "Main Memory\t\tPage Frame\t\tStatus\t\tCounter\t\tBurst_Counter\n"
        for PM in range(self.number_of_pageFrame):
            if self.page_frame[PM][1] == 'OS':
                to_print += "OS\t\t\t\t" + str(PM) + "\n"
            elif self.page_frame[PM][1] == '-':
                to_print += "-\t\t\t\t" + str(PM) + '\t\t\t\tfree\t\t' + str(
                    self.page_frame[PM][4]) + '\t\t' + '\n'
            else:
                jobid = self.page_frame[PM][1]
                pageId = self.page_frame[PM][2]
                status = self.page_frame[PM][3]
                counter = self.page_frame[PM][4]
                burst_counter = self.page_frame[PM][5]
                to_print += 'J' + str(jobid) + 'P' + str(pageId) + "\t\t\t" + str(
                    PM) + "\t\t\t\t" + status + '\t\t' + str(
                    counter) + '\t\t\t' + str(burst_counter) + '\n'
        print(to_print)

    def printInQueProcess(self):
        to_print = 'Process in que : '
        if self.in_que_process_buffer.in_que_head is not None:
            pointer = self.in_que_process_buffer.in_que_head
            while pointer is not None:
                to_print += '{J' + str(pointer.jobID) + 'P' + str(pointer.pageID) + '[' + str(
                    pointer.burst_time) + ']} -> '
                pointer = pointer.nextProcess
            to_print += 'None\n'
        else:
            to_print += 'None\n'
        print(to_print)

    def printJobList(self):
        to_print = ''
        for JOB in range(len(self.job_list)):
            to_print += '\nJOB ' + str(JOB) + '\n'
            to_print += "Page\tburst_time\tstatus\n"
            for PAGE in range(len(self.job_list[JOB].page)):
                to_print += "Page " + str(PAGE) + "\t" + str(self.job_list[JOB].page[PAGE][3]) + "\t\t\t" + self.job_list[JOB].page[PAGE][5] + "\n"

        print(to_print)


# Read input file and get the data
inputFile = open("paged input.txt", "r")
input_data = inputFile.readlines()
##############################################
# get number of size
for i in input_data[0].split():
    if i.isdigit():
        pageSize = int(i)

# get number of jobs
for i in input_data[1].split():
    if i.isdigit():
        number_of_job = int(i)
job = list()

# get number of page frame
for i in input_data[2].split():
    if i.isdigit():
        number_of_page_frame = int(i)

# get number of page frame occupied by OS
for i in input_data[3].split():
    if i.isdigit():
        OSspace = int(i)

# get max jobInvoved size
for i in input_data[4].split():
    if i.isdigit():
        max_jobSize = int(i)

# get max jobInvoved max burst time
for i in input_data[5].split():
    if i.isdigit():
        max_burst_time = int(i)
################################################

# Main Code Program
memory = Main_Memory(number_of_page_frame, OSspace)

t = 0
totalJobArrived = 0
while t < 100:
    memory.allocateProcess()
    memory.printMMT()
    jobArriveBool = random.randint(0, 1)
    # continuos random jobInvoved arrive
    if jobArriveBool == 1 and totalJobArrived < number_of_job + 1:
        ranJobSize = random.randint(1, max_jobSize + 1)
        newJob = Job(totalJobArrived, ranJobSize, pageSize, max_burst_time)
        memory.job_list.append(newJob)
        # addProcessToQue(self, jobID, pageID, burst_time, algoBool)
        for i in range(newJob.number_of_page):
            memory.in_que_process_buffer.addProcessToQue(totalJobArrived, i, newJob.page[i][3], False)
        print('job ' + str(totalJobArrived) + ' arrived')
        totalJobArrived += 1
    memory.printInQueProcess()
    memory.deallocateProcess()
    t += 1
memory.printJobList()

# number_of_page_frame = 12
# OSspace = 2
# number_of_job = 5
# max_jobSize = 50
# pageSize = 10
# max_burst_time = 5
