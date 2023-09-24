
class fixedStack:
    def __init__(self, maxSize = 100):
        self.queue = list()
        self.maxSize = maxSize

    #for appending
    def add(self, data):
        #check list size
        if self.size() >= self.maxSize:
            self.pop()
        self.queue.append(data)
        return True

    #for deleting first element in stack FIFO
    def pop(self):
        data = self.queue[0]
        self.queue.pop(0)
        return data

    #Size of queuer example, to search for the first occurrence of the string ‘foo’ in the current line and replac
    def size(self):
        return len(self.queue)

class Queue:

    #Constructor
    def __init__(self, maxSize = 100):
        self.queue = list()
        self.maxSize = maxSize
        self.head = 0
        self.tail = 0

    #Adding elements
    def enqueue(self,data):
        #Checking if the queue is full
        if self.size() >= self.maxSize:
            return ("Queue Full")
            #self.dequeue()
        self.queue.append(data)
        self.tail += 1
        return True     

    #Deleting elements 
    def dequeue(self):
        #Checking if the queue is empty
        if self.size() <= 0:
            self.resetQueue()
            return ("Queue Empty") 
        data = self.queue[self.head]
        self.head+=1
        return data
                
    #Returning Queue
    def getQ(self):
        return self.queue

    #Calculate size
    def size(self):
        return self.tail - self.head
    
    #Reset queue
    def resetQueue(self):
        self.tail = 0
        self.head = 0
        self.queue = list()


