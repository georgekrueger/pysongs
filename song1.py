#!/usr/bin/env python
# test code for PyPortMidi
# a port of a subset of test.c provided with PortMidi
# John Harrison
# harrison [at] media [dot] mit [dot] edu

# March 15, 2005: accommodate for SysEx messages and preferred list formats
#                 SysEx test code contributed by Markus Pfaff 
# February 27, 2005: initial release

import pypm
import array
import time
import copy

INPUT=0
OUTPUT=1

def PrintDevices(InOrOut):
    for loop in range(pypm.CountDevices()):
        interf,name,inp,outp,opened = pypm.GetDeviceInfo(loop)
        if ((InOrOut == INPUT) & (inp == 1) |
            (InOrOut == OUTPUT) & (outp ==1)):
            print loop, name," ",
            if (inp == 1): print "(input) ",
            else: print "(output) ",
            if (opened == 1): print "(opened)"
            else: print "(unopened)"
    print

class Pattern:
    class Event:
        def __init__(self, offset, pitch, vel, length):
            self.offset = offset
            self.pitch = pitch
            self.vel = vel
            self.length = length

        def __str__(self):
            return "@{self.offset} p: {self.pitch}, v: {self.vel}, l: {self.length}".format(self=self)

    def __init__(self, length):
        self.events = []
        self.length = length
        print self

    def __str__(self):
        return "New Pattern. Length: {self.length}".format(self=self)

    def addNote(self, offset, pitch, vel, length):
        event = self.Event(offset, pitch, vel, length)
        self.events.append(event)

    def addPattern(self, offset, pattern, repeatCount):
        for i in range(repeatCount):
            for e in pattern.events:
                newEvent = copy.deepcopy(e)
                newOffset = offset + (i * pattern.length) + e.offset
                newEvent.offset = newOffset
                print "event added " + str(newEvent)
                self.events.append(newEvent)

    def play(self):
        dev = 1
        latency = 1000
        midiOut = pypm.Output(dev, latency)
        time = pypm.Time()
        for event in self.events:
            midiOut.Write([[[0x90, event.pitch, event.vel], time + event.offset]])
            midiOut.Write([[[0x90, event.pitch, 0], time + event.offset + event.length]])

        
        del midiOut
        
def TestOutput():
    len = 250
    p1NumEvents = 20
    p1Length = len * p1NumEvents
    p1 = Pattern(p1Length)
    for i in range(p1NumEvents):
        p1.addNote(i*len, 50 + (i*2), 100, len)
    
    p2 = Pattern(p1.length * 4)
    p2.addPattern(0, p1, 4)

    p2.play()


# main code begins here
pypm.Initialize() # always call this first, or OS may crash when you try to open a stream
TestOutput()
while(1):
    dummy = raw_input("Type 'q' to quit.\n")
    if dummy == "q" or dummy == "quit":
        break
pypm.Terminate()
