import random


# jobInvoved object
class JOB:
    def __int__(self):
        self.jobNumber = -1
        self.memoryRequest = 0
        self.status = 'in que'

    def __init__(self, jobNumber, memoryRequest):
        self.jobNumber = jobNumber
        self.memoryRequest = memoryRequest
        self.status = 'in que'

    def updateJobStatus(self, statusUpdate):
        self.status = statusUpdate


# Memory node or memory object
class MEMORY:
    def __init__(self, memoryLocation, memoryBlockSize):
        self.memoryLocation = memoryLocation
        self.memoryBlockSize = memoryBlockSize
        self.JOB = None
        self.status = 'free'
        self.internalFragmentation = 0
        self.next = None

    def allocateJob(self, job):
        self.status = 'busy'
        self.JOB = job

    def deallocateJob(self):
        self.status = 'free'
        temp = self.JOB
        temp.updateJobStatus('completed')
        self.JOB = None


# linked list implementation
class Memory_List:
    def __init__(self):
        self.head = None
        self.tail = None
        self.lowestSizeJob = None  # for deallocation from lowest size
        self.waitingJobList = list()
        self.jobArrived = list()
        self.runningTime = 0

    def __init__(self, size):
        self.head = None
        self.tail = None
        self.lowestSizeJob = None  # for deallocation from lowest size
        self.waitingJobList = list()
        self.jobArrived = list()
        self.runningTime = 0
        self.nextFitPointer = self.head
        self.size = size

    def addMemory(self, memoryLocation, memoryBlockSize):
        memory = MEMORY(memoryLocation, memoryBlockSize)
        if self.head is None:
            self.head = memory
            self.tail = self.head
            self.runningTime += 1
        else:
            tmp = self.tail
            tmp.next = memory
            self.tail = tmp.next
            self.runningTime += 1

    def addJob(self, job):
        self.waitingJobList.append(job)
        self.jobArrived.append(job)

    def allocateJobToFreeMemoryBestFit(self):
        for job in self.waitingJobList:
            self.runningTime += 1
            if self.head is not None:
                self.runningTime += 1
                pointer = self.head
                memorySelected = MEMORY(-1, -1)
                while pointer is not None:
                    self.runningTime += 1
                    if pointer.status == 'free':
                        self.runningTime += 1
                        if pointer.memoryBlockSize >= job.memoryRequest:
                            self.runningTime += 1
                            if memorySelected.memoryLocation == -1:
                                self.runningTime += 1
                                memorySelected = pointer
                            elif memorySelected.memoryBlockSize > pointer.memoryBlockSize:
                                self.runningTime += 1
                                memorySelected = pointer

                    pointer = pointer.next

                if memorySelected.memoryLocation != -1:
                    self.runningTime += 1
                    memorySelected.allocateJob(job)
                    job.updateJobStatus('processing')
                    self.waitingJobList.remove(job)  # remove the jobInvoved from the waiting list

    def allocateJobToFreeMemoryFirstFit(self):
        for job in self.waitingJobList:
            self.runningTime += 1
            if self.head is not None:
                self.runningTime += 1
                pointer = self.head
                memorySelected = MEMORY(-1, -1)
                while pointer is not None:
                    self.runningTime += 1
                    if pointer.status == 'free':
                        self.runningTime += 1
                        if pointer.memoryBlockSize >= job.memoryRequest:
                            self.runningTime += 1
                            if memorySelected.memoryLocation == -1:
                                self.runningTime += 1
                                memorySelected = pointer
                                break

                    pointer = pointer.next

                if memorySelected.memoryLocation != -1:
                    self.runningTime += 1
                    memorySelected.allocateJob(job)
                    job.updateJobStatus('processing')
                    self.waitingJobList.remove(job)  # remove the jobInvoved from the waiting list

    def allocateJobToFreeMemoryNextFit(self):
        for job in self.waitingJobList:
            if self.head is not None:
                if self.nextFitPointer is not None:
                    pointer = self.nextFitPointer
                else:
                    pointer = self.head
                memorySelected = MEMORY(-1, -1)
                s = 0
                while s < self.size:
                    s += 1
                    if pointer.status == 'free':
                        if pointer.memoryBlockSize >= job.memoryRequest:
                            if memorySelected.memoryLocation == -1:
                                memorySelected = pointer
                                self.nextFitPointer = pointer
                                break

                    pointer = pointer.next
                    if pointer is None:
                        pointer = self.head

                if memorySelected.memoryLocation != -1:
                    memorySelected.allocateJob(job)
                    job.updateJobStatus('processing')
                    self.waitingJobList.remove(job)  # remove the jobInvoved from the waiting list

    def randomDeAllocation(self):
        if self.head is not None:
            pointer = self.head
            while pointer is not None:
                randomList1 = [2, 2, 2, 1]
                if pointer.status == 'busy':
                    toAllocateBool = random.choice(randomList1)
                    if toAllocateBool % 2 != 0:
                        pointer.deallocateJob()
                pointer = pointer.next

    def randomDeAllocationComparison(self):
        if self.head is not None:
            pointer = self.head
            while pointer is not None:
                if pointer.status == 'busy':
                    pointer.deallocateJob()
                    break
                pointer = pointer.next

    def maxMemoryBlockSize(self):
        if self.head is not None:
            self.runningTime += 1
            pointer = self.head
            maxJobSize = 0
            while pointer is not None:
                self.runningTime += 1
                if pointer.memoryBlockSize > maxJobSize:
                    self.runningTime += 1
                    maxJobSize = pointer.memoryBlockSize

                pointer = pointer.next
            return maxJobSize
        else:
            self.runningTime += 1
            return 0

    def printMemoryBlock(self):
        if self.head is not None:
            pointer = self.head
            toPrint = '\n\nMemoryList\nMemory Location\t\tMemory Block Size\t\tJob Number\t\tJob size\tinternal fragmentation\tstatus\n'
            while pointer is not None:
                toPrint += str(pointer.memoryLocation) + '\t\t\t\t' + str(pointer.memoryBlockSize) + '\t\t\t\t'
                if pointer.JOB is not None:
                    toPrint += '\t\tJ' + str(pointer.JOB.jobNumber) + '\t\t\t\t' + str(
                        pointer.JOB.memoryRequest) + '\t\t\t' + str(
                        pointer.memoryBlockSize - pointer.JOB.memoryRequest) + '\t\t\t\t\t\t'
                else:
                    toPrint += '\t\t-\t\t\t\t-\t\t\t-\t\t\t\t\t\t'
                toPrint += str(pointer.status) + '\n'
                pointer = pointer.next

            print(toPrint)

    def printJob(self):
        toPrint = '\nJob List\nJob Number\tMemory Requested\t status\n'
        for jobArrived in self.jobArrived:
            toPrint += 'J' + str(jobArrived.jobNumber) + '\t\t\t' + str(jobArrived.memoryRequest) + '\t\t\t\t\t' + str(
                jobArrived.status) + '\n'
        print(toPrint)


# Read file and get the data
inputFile = open("input File.txt", "r")
input_data = inputFile.readlines()
##############################################
# get number of memory block
for i in input_data[0].split():
    if i.isdigit():
        numberOfMemoryBlock = int(i)
# get max mem block size
for i in input_data[1].split():
    if i.isdigit():
        maxMemoryBlockSize = int(i)
# get number of jobInvoved
for i in input_data[2].split():
    if i.isdigit():
        numberOfJob = int(i)
################################################

MemoryList = Memory_List(numberOfMemoryBlock)  # for next fit algo
# the 2 below are for running time comparison
# MemoryList = Memory_List() # Best Fit
# MemoryList2 = Memory_List() # First Fit
initial = 10000

for i in range(numberOfMemoryBlock):
    location = random.randint(initial, initial + maxMemoryBlockSize)
    blockSize = random.randint(1, 1000)
    initial += blockSize + 5000
    MemoryList.addMemory(location, blockSize)
    # MemoryList2.addMemory(location, blockSize)
# MemoryList.printMemoryBlock()

j = 1
maxJobSize = MemoryList.maxMemoryBlockSize()  # max jobInvoved size

# #best fit algo
# while j <= numberOfJob:
#     MemoryList.randomDeAllocation();
#     jobArriveBool = random.randint(0, 1)
#
#     # continuos random jobInvoved arrive
#     if jobArriveBool == 1:
#         MemoryList.addJob(JOB(j, random.randint(1, maxJobSize)))
#         MemoryList.allocateJobToFreeMemoryBestFit()
#         j += 1
#     MemoryList.printJob()
#     MemoryList.printMemoryBlock()


# #first fit algo
# while j <= numberOfJob:
#     MemoryList2.randomDeAllocation();
#     jobArriveBool = random.randint(0, 1)
#
#     # continuos random jobInvoved arrive
#     if jobArriveBool == 1:
#         MemoryList2.addJob(JOB(j, random.randint(1, maxJobSize)))
#         MemoryList2.allocateJobToFreeMemoryFirstFit()
#         j += 1
#     MemoryList2.printJob()
#     MemoryList2.printMemoryBlock()


# next fit algo
while j <= numberOfJob:
    MemoryList.randomDeAllocation();
    jobArriveBool = random.randint(0, 1)

    # continuos random jobInvoved arrive
    if jobArriveBool == 1:
        MemoryList.addJob(JOB(j, random.randint(1, maxJobSize)))
        MemoryList.allocateJobToFreeMemoryNextFit()
        j += 1
    MemoryList.printJob()
    MemoryList.printMemoryBlock()

# first fit and best fit running time comparison
# while j <= numberOfJob:
#     MemoryList.randomDeAllocationComparison();
#     MemoryList2.randomDeAllocationComparison();
#     jobArriveBool = random.randint(0, 1)
#
#     # continuos random jobInvoved arrive
#     if jobArriveBool == 1:
#         MemoryList.addJob(JOB(j, random.randint(1, maxJobSize)))
#         MemoryList.allocateJobToFreeMemoryBestFit()
#
#         MemoryList2.addJob(JOB(j, random.randint(1, maxJobSize)))
#         MemoryList2.allocateJobToFreeMemoryFirstFit()
#         j += 1
# print("Best Fit     :" + str(MemoryList.runningTime))
# print("First Fit    :" + str(MemoryList2.runningTime))
