#!/usr/bin/env python2.7
"""
Clone of 2048 game.
"""
import random
import os
import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    #remove 0s from list and append to the end
    tmp=filter(None,line)
    diff=len(line)-len(tmp)        
    for _ in range(diff):
        tmp.append(0)
    # merge elements
    res=list(tmp)
    counter=0
    while counter<len(tmp)-1:
        if (tmp[counter]==tmp[counter+1]):
            res[counter]=tmp[counter]*2
            res[counter+1]=0
            counter+=1
        counter+=1
       
    #remove 0s from final list
    diff=res.count(0)
    res=filter(None,res)
    for _ in range(diff):
        res.append(0)
    return res

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, _height, _width):
        self._height=_height
        self._width=_width
        self.reset()
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid=[[0 for _ in range(self._width)]
                   for __ in range(self._height)]
        self.new_tile()
        self.new_tile()
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        grid2text=""
        for row in self._grid:
            grid2text+=str(row)+'\n'
        return grid2text

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width
    
    def is_grid_full(self):
        """
        Return True if there is no empty tile.
        """
        isfull=True
        for row in self._grid:
            if 0 in row:
                isfull=False
                break
        return isfull    
                
        
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        hasmoved=False
        if direction==LEFT:
            for row in range(self._height):
                if merge(self._grid[row])!= self._grid[row]:
                    hasmoved=True
                self._grid[row] = merge(self._grid[row])
                 
        if direction==RIGHT:
            for row in range(self._height):
                tmp_list=self._grid[row][::-1]
                #print tmp_list
                if merge(tmp_list)[::-1] != self._grid[row]:
                    hasmoved=True
                self._grid[row] = merge(tmp_list)[::-1]   
            #print str(self)
        if direction==UP:
            for col in range(self._width):
                tmp_list=(lambda n: [self._grid[row][col] for row in range(n)])(self._height)
                #print tmp_list
                tmp_list=merge(tmp_list)
                #print tmp_list
                for elem in range(len(tmp_list)):
                    if self._grid[elem][col]!=tmp_list[elem]:
                        hasmoved=True
                    self._grid[elem][col]=tmp_list[elem]
            print str(self)
        if direction==DOWN:
            for col in range(self._width):
                tmp_list=(lambda n: [self._grid[i][col] for i in range(n)])(self._height)[::-1]
                #print tmp_list
                tmp_list=merge(tmp_list)[::-1]
                #print tmp_list
                for elem in range(len(tmp_list)):
                    if self._grid[elem][col]!=tmp_list[elem]:
                        hasmoved=True
                    self._grid[elem][col]=tmp_list[elem]
            print str(self)
        if self.is_grid_full()==False and hasmoved==True:
            self.new_tile()
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        tile=0
        if random.randint(1,100)<=90:
            tile=2
        else:
            tile=4
        tmp_list=[]
        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col]==0:
                    tmp_list.append([row,col])
        tile_pos=random.choice(tmp_list)
        self._grid[tile_pos[0]][tile_pos[1]]=tile
        

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col]=value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

    def draw(self):
        print str(self)

    
def main():
    game=TwentyFortyEight(4,4)   
    screen=curses.initscr()
    screen.keypad(1)
    curses.noecho()
    dims=screen.getmaxyx()
    x,y=0,0
    q=-1
    while q!= ord('q'):
        #screen.clear()
        screen.clear()
        screen.addstr(x,y,str(game))
        screen.refresh()
        q=screen.getch()
        if q == curses.KEY_DOWN:
           game.move(DOWN)
        if q== curses.KEY_UP:
           game.move(UP)
        if q== curses.KEY_LEFT:
           game.move(LEFT)
        if q== curses.KEY_RIGHT:
           game.move(RIGHT) 
    curses.endwin()
if __name__=='__main__':              
    main()
