#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 18:44:07 2019

@author: aditipatil
"""

import random
import math
from matplotlib import pyplot as plt
import numpy as np

def image_example():
    '''should produce red,purple,green squares
    on the diagonal, over a black background'''
    # RGB indexes
    red,green,blue = range(3)
    # img array 
    # all zeros = black pixels
    # shape: (150 rows, 150 cols, 3 colors)
    img = np.zeros((150,150,3))
    for x in range(50):
        for y in range(50):
            # red pixels
            img[x,y,red] = 1.0
            # purple pixels
            # set 3 color components 
            img[x+50, y+50,:] = (.5,.0,.5)
            # green pixels
            img[x+100,y+100,green] = 1.0
    plt.imshow(img)

def normpdf(x, mean, sd):
    """
    Return the value of the normal distribution 
    with the specified mean and standard deviation (sd) at
    position x.
    You do not have to understand how this function works exactly. 
    """
    var = float(sd)**2
    denom = (2*math.pi*var)**.5
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    return num/denom

def pdeath(x, mean, sd):
    start = x-0.5
    end = x+0.5
    step =0.01    
    integral = 0.0
    while start<=end:
        integral += step * (normpdf(start,mean,sd) + normpdf(start+step,mean,sd)) / 2
        start += step            
    return integral    
    
recovery_time = 4
virality = 0.9
mean = 3
stdev = 1

class Cell(object):

    def __init__(self,x, y):
        self.x = x
        self.y = y
        self.state = "S"
        self.time = 0
        
    def infect(self):
        self.state = 'I'
        
    def process(self, adjacent_cells):
        if not(self.state == 'I'):
            return None
        t = self.time
        self.time = self.time + 1
        if t >= recovery_time:
            self.state = 'S'
            self.time = 0
        if (self.state == 'I') and (random.random() <= pdeath(t, mean, stdev)):
            self.state = 'R'
        if self.state == 'I':
            for n in adjacent_cells:
                if (n.state == 'S') and (random.random() <= virality):
                    n.infect()
        
class Map(object):
    def __init__(self):
        self.height = 150
        self.width = 150
        self.cells = {}
    def add_cell(self, cell):
        self.cells[(cell.x, cell.y)] = cell
    def display(self):
        li = [] 
        for x in range(self.width):
            p = []
            for y in range(self.height):
                if not((x, y) in self.cells):
                    p.append((0.0, 0.0, 0.0))
                elif self.cells[(x, y)].state == 'S':
                    p.append((0.0, 1.0, 0.0))
                elif self.cells[(x, y)].state == 'I':
                    p.append((1.0, 0.0, 0.0))
                elif self.cells[(x, y)].state == 'R':
                    p.append((0.5, 0.5, 0.5))
            li.append(p)
        
        plt.imshow(li)
    
    def adjacent_cells(self, x,y):
        s = set() # i made this a set instead of a list because it makes more sense to me
        
        if (x + 1, y) in self.cells:
            s = s | {self.cells[(x + 1, y)]}
        if (x - 1, y) in self.cells:
            s = s | {self.cells[(x - 1, y)]}
        if (x, y + 1) in self.cells:
            s = s | {self.cells[(x, y + 1)]}
        if (x, y - 1) in self.cells:
            s = s | {self.cells[(x, y - 1)]}
        
        return s
    
    def time_step(self):
        for i in self.cells:
            self.cells[i].process(self.adjacent_cells(i[0], i[1]))
        self.display()
            
def read_map(filename):
    
    m = Map()
    file = open(filename)
    
    for line in file:
        c = line.split(',')
        c[0] = int(c[0])
        c[1] = int(c[1][:-1])
        x, y = c
        m.add_cell(Cell(x, y))
    
    return m