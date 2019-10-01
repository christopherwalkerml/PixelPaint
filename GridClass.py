import random,pygame,os,math;

#-------------------------------------------------
#Description: this class is the basics for making a basic grid.
#   it has all the basic variables needed to create, edit, and draw a grid.
#-------------------------------------------------

scrnwid = 1040;
scrnhig = 650;

########################################################################################

def clamp(val, minval, maxval, name):
    if val > maxval:
        if name != '':
            print(name, 'has been clamped to', maxval); #make sure that the value is below the max val and above the min val
        val = maxval;
    elif val < minval:
        if name != '':
            print(name, 'has been clamped to', minval);
        val = minval;
    return val;

def default(var, typ, defl, name):
    if type(var) == typ:
        var = var;
    else:
        print(name, 'was not valid. Setting to default value of', defl); #if the val isnt the correct type, set it to a default value
        var = defl;
    return var;
########################################################################################

class grid(object):
    
    def __init__(self, cols, rows, xpos = 0, ypos = 0, xsize = scrnwid, ysize = scrnhig, vertlinewidth = 0, horlinewidth = 0, linevisible = True, outline = True):
        #Set values, and default values if input values are incorrect
        self.rows = default(rows, int, 5, 'Rows');

        self.cols = default(cols, int, 5, 'Cols');

        self.vertlinewidth = default(vertlinewidth, int, 1, 'Vertical line width');

        self.horlinewidth = default(horlinewidth, int, 1, 'Horizontal line width');

        self.linevisible = default(linevisible, bool, True, 'Line visibility');

        self.outline = default(outline, bool, True, 'Outline');

        #Make sure that there isnt more than one grid spot per pixel on screen

        self.cols = clamp(cols, 1, xsize, 'Columns per pixel');

        self.rows = clamp(rows, 1, ysize, 'Rows per pixel');

        ################ Make sure that the grid will fit on screen
        self.xpos = clamp(xpos, 0, scrnwid, 'xpos');

        self.ypos = clamp(ypos, 0, scrnhig, 'ypos');
        ################
        self.xsize = clamp(xsize, 25, scrnwid - 1, 'xsize');
            
        self.ysize = clamp(ysize, 25, scrnhig, 'ysize');
        ################ Make sure that the grid wont go beyong the screen when being displaced by the position variable
        self.xpos = clamp(self.xpos + self.xsize, 0, scrnwid, 'valid x position and sizing') - self.xsize;
        self.ypos = clamp(self.ypos + self.ysize, 0, scrnhig, 'valid y position and sizing') - self.ysize;

        #Set drawing variables
        self.idrawx = self.xpos;
        self.idrawy = self.ypos;
        self.fdrawx = self.xpos + self.xsize;
        self.fdrawy = self.ypos + self.ysize;
        #set the drawing gap between grid spots
        self.xgap = self.xsize / self.cols;
        self.ygap = self.ysize / self.rows;

########################################################################################
