#!/usr/bin/env python3
#Generate random notes to test on the guitar
#Never generates the same note too often compared with the others

import random
import time

def showScale():
    print("6.-----------MI-------------")
    print("5.-----------LA-------------")
    print("4.-----------RE-------------")
    print("3.-----------SOL------------")
    print("2.-----------SI-------------")
    print("1.-----------MI-------------")

#Function to check if any element in an array appears more than n times than any other element
def countDiff(c, n):
    for _i in range(len(c)):
        for _j in range(len(c)):
            if (_i!=_j):
                if (c[_i]>=c[_j]+n):
                    return False
                else: 
                    continue
    return True

def randNotes():
    notes=["mi","la","re","sol","si"]
    count=[0,0,0,0,0]
    while True:
        n=random.choice(notes)
        count[notes.index(n)]+=1
        c=count[notes.index(n)]
        if (countDiff(count,3)==False):
            count[notes.index(n)]-=1
            continue
        else:
            print(n)
            #print(count)
            time.sleep(3)

def main():
    showScale()
    randNotes()

if __name__=='__main__':
    main()
