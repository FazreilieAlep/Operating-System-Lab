# Python3 implementation of FIFO page
# replacement in Operating Systems.
from queue import Queue
import random

# Function to find page faults using FIFO
def pageFaults(incomingStream, n, frames):
    print("Incoming", end = "\t")
    for i in range(frames):
        print("Frame", i+1, end = "\t")
    
    #unordered set to simple determine if a page is already in the frame
    s = set()

    # Queue created to store pages in FIFO manner
    # since set will not store order or entry
    # we will use queue to note order of entry of incoming page
    queue = Queue()

    page_faults = 0
    for i in range(n):

        # if set has lesser item than frames
        # i.e. set can hold more items
        if len(s) < frames:

            # If incoming item is not present, add to set
            if incomingStream[i] not in s:
                s.add(incomingStream[i])

                # increment page fault 
                page_faults += 1

                # Push the incoming page into the queue
                queue.put(incomingStream[i])

        # If the set is full then we need to do page replacement
        # in FIFO manner that is remove first item from both
        # set and queue then insert incoming page
        else:

            # If incoming item is not present
            if incomingStream[i] not in s:
                # remove the first page from the queue
                val = queue.queue[0]

                queue.get()

                # Remove from set
                s.remove(val)

                # insert incoming page to set
                s.add(incomingStream[i])

                # push incoming page to queue
                queue.put(incomingStream[i])

                # Increment page faults 
                page_faults += 1

        print(incomingStream[i], end="\t\t\t")
        for q_item in queue.queue:
            print(q_item, end="\t\t")

        print()
    return page_faults
  
# Run code
inputfile = open("input (2).txt","r")
input_data = inputfile.readlines()

#page init
for i in input_data[0].split():
    if i.isdigit():
        page_capacity = int(i)

for i in input_data[1].split():
    if i.isdigit():
        num_pages = int(i)

page_value_range = []
for i in input_data[2].split():
    if i.isdigit():
        page_value_range.append(int(i))

pages = []
for i in range(num_pages):
    pages.append(random.randint(page_value_range[0], page_value_range[1]))
n = len(pages) 

#Print the pages
print("Pages:")
for i in range(n):
    print(str(pages[i]) , end = " ")
print("\nNumber of pages: ", n)
print("\n")
print("\nPage faults: ", pageFaults(pages, n, page_capacity))