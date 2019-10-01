#------------------------------------------------
# Program : Pixel OOP assignment by Chris Walker
# Date: November 20 2017
# Description: This program imports the main Grid Class
#   and creates several child grids using this class.
#   The main goal of this program is to let the user
#   draw onto the screen by clicking and dragging.
#Features:
#   - Drawing
#   - Replacing
#   - Erasing
#   - Pipette
#   - Clear
#   - A 2000 colour palette
#   - Saving and Loading (1 save only)
#   - Undoing
#   - Different font sizes
#   - chosing grid width and height
#------------------------------------------------

import random,pygame,os,math,re,sys;
from GridClass import grid;
pygame.init();

font = pygame.font.Font(None, 60);

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (225,50);

scrnwid = 1040;
scrnhig = 650;
win = pygame.display.set_mode((scrnwid,scrnhig));

GRAY = (119, 119, 119);
BLACK = (0, 0, 0);
WHITE = (255, 255, 255);
RED = (255, 0, 0);

class glob(): #global variables

    def __init__(self):
        self.isundo = False;
        self.drawcolour = BLACK;
        self.drawmode = 'draw';
        self.fontsize = 1;
        self.firstclick = True; #global variables
        self.undolist = [];
        self.ingame = False;
        self.xpixels = 0;
        self.ypixels = 0;
        self.edit = False;
        self.loadsave = False;
        self.save = False;
        self.drawlist = [];

glo = glob();

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

sys.setrecursionlimit(1000000000)

def fill(gridid, c, r, colr): #my failed attempt at a filling feature
    if gridid.gridspots[c][r].colour != colr:
        pass;
    else:
        gridid.gridspots[c][r].colour = glo.drawcolour;
        if c < gridid.cols - 1:
            fill(gridid, c + 1, r, colr);
        if c > 0:
            fill(gridid, c - 1, r, colr);
        if r < gridid.rows - 1:
            fill(gridid, c, r + 1, colr);
        if r > 0:
            fill(gridid, c, r - 1, colr);
            
########################################################################################

xysizelist = [[100, 'x pixels', False], [50, 'y pixels', False], [False, 'Start']]; #menu grid stuff
class choose():

    def __init__(self):
        self.colour = BLACK;
        self.size = xysizelist[0];
        del xysizelist[0];
        self.spotype = 'menu';

class exitgame():

    def __init__(self): #make a class object to close the game
        self.colour = RED;
        self.spotype = 'exitgame';

modelist = ['draw', 'erase', 'fill', 'replace', 'pipette', 'clear']; #modes
class tools():

    def __init__(self):
        self.colour = BLACK;
        self.mode = modelist[0];
        del modelist[0];
        self.spotype = 'tools'; #make child classes for the pixel grid

fontlist = [1,3,5,9,20]; #font sizes. (you can add a font size if you want. just add a comma, then a number. ex: [1,2,3,9,30]
class drawsizes():

    def __init__(self):
        self.colour = BLACK;
        self.font = fontlist[0];
        del fontlist[0];
        self.spotype = 'drawsizes';

class pixel():

    def __init__(self):
        self.colour = WHITE; #the pixels on the drawing screen
        self.spotype = 'pixel';

colourlist = [];
#make a few colours
for r in range(1, 256, 15):
    for g in range(1, 256, 15):
        for b in range(1, 256, 15):
            col = (r,g,b);
            colourlist.append(col);

class palette():

    def __init__(self):
        self.colour = colourlist[0]; #create the palette class
        del colourlist[0];
        self.spotype = 'palette';

class colourdisplay(): #create the colour display class

    def __init__(self):
        self.colour = glo.drawcolour;
        self.spotype = 'colourdisplay';

class undo(): #create the undo class

    def __init__(self):
        self.colour = BLACK;
        self.spotype = 'undo';

sllist = [[1,'Save'],[1,'Load']];
class saveload(): #create rhe save and load class

    def __init__(self):
        self.colour = BLACK;
        self.slmode = sllist[0];
        del sllist[0];
        self.spotype = 'saveload';
        
########################################################################################

#---------------------------------------------------
#Description: This class draws all of the child classes when they are passed through the draw method.
#Instead of initializing each child class individually, you just simply pass through what
        #type of grid that it will be, and it gets created, and drawn properly.
#---------------------------------------------------

class pixelgrid(grid):

    def __init__(self, gridtype, cols, rows, xpos = 0, ypos = 0, xsize = scrnwid, ysize = scrnhig, vertlinewidth = 0, horlinewidth = 0, linevisible = True, outline = True):

        grid.__init__(self, cols, rows, xpos, ypos, xsize, ysize, vertlinewidth, horlinewidth, linevisible, outline);

        if gridtype == 'pixel':
            self.gridspots = [[pixel() for pg in range(self.rows)] for pgs in range(self.cols)];
        elif gridtype == 'palette':
            self.gridspots = [[palette() for pg in range(self.rows)] for pgs in range(self.cols)];
        elif gridtype == 'tools':
            self.gridspots = [[tools() for pg in range(self.rows)] for pgs in range(self.cols)]; #make a list of child classes for the grids
        elif gridtype == 'drawsizes':
            self.gridspots = [[drawsizes() for pg in range(self.rows)] for pgs in range(self.cols)];
        elif gridtype == 'exitgame':
            self.gridspots = [[exitgame() for pg in range(self.rows)] for pgs in range(self.cols)];
        elif gridtype == 'colourdisplay':
            self.gridspots = [[colourdisplay() for pg in range(self.rows)] for pgs in range(self.cols)];
        elif gridtype == 'undo':
            self.gridspots = [[undo() for pg in range(self.rows)] for pgs in range(self.cols)];
        elif gridtype == 'menu':
            self.gridspots = [[choose() for pg in range(self.rows)] for pgs in range(self.cols)];
        elif gridtype == 'saveload':
            self.gridspots = [[saveload() for pg in range(self.rows)] for pgs in range(self.cols)];

    def drawgrid(self, update):
        global drawcolour, drawmode, fontsize
        if update:
            mpos = pygame.mouse.get_pos();
            gridposx = int((mpos[0] - self.xpos) // self.xgap);
            gridposy = int((mpos[1] - self.ypos) // self.ygap);
            #editing the draw grid.
            #Same for all: get the position of clicking, turn the coordinate into a grid position, and get or change the grid position
            #load or save a file
                        
            if self.gridspots[0][0].spotype == 'pixel': #make sure its the right type of grid
                if (mpos[0] > self.xpos and mpos[0] < (self.xpos + self.xsize)) and (mpos[1] > self.ypos and mpos[1] < (self.ypos + self.ysize)):
                    if mbd:
                        glo.firstclick = True;
                        
                    if mbu == False and glo.firstclick == True: #save the grid before the user draws for an undo save
                        glo.firstclick = False;
                        bigtemplist = [];
                        for xps in range(self.cols):
                            templist = [];
                            for yps in range(self.rows):
                                templist.append(self.gridspots[xps][yps].colour); #save the grid into a list
                            bigtemplist.append(templist)
                        if len(glo.undolist) == 20: #max undos (set to -1 to have no limit)
                            del glo.undolist[0];
                        if bigtemplist not in glo.undolist and (glo.drawmode != 'pipette'):
                            glo.undolist.append(bigtemplist); #this makes it so that undo can be done several times
                    if glo.drawmode == 'draw' or glo.drawmode == 'erase':
                        if not mbu:
                            gridposx -= (glo.fontsize // 2); #this sets the position of the click to be half of the font size up and to the left, so that it can
                            gridposy -= (glo.fontsize // 2);    #just for loop and fill instead of looping through every row and column. This makes it so that
                            for xp in range(glo.fontsize):      #in order to create a new font size, just add it to the font size list at the beginning of the program
                                for yp in range(glo.fontsize):
                                    if glo.drawmode == 'draw':
                                        drawcl = glo.drawcolour; #draw on the screen and loop for the font size
                                    else:
                                        drawcl = WHITE;
                                    self.gridspots[clamp(gridposx + xp, self.xpos, self.cols - 1, '')][clamp(gridposy + yp, self.ypos, self.rows - 1, '')].colour = drawcl;
                    elif glo.drawmode == 'fill':
                        colr = self.gridspots[gridposx][gridposy].colour; #this doesnt quite work yet, so dont use it
                        fill(self, gridposx, gridposy, colr);
                    elif glo.drawmode == 'replace':
                        initcolour = self.gridspots[gridposx][gridposy].colour; #replace all the clicked colour tiles for the colour selected
                        for cl in self.gridspots:
                            for cls in cl:
                                if cls.colour == initcolour:
                                    cls.colour = glo.drawcolour;
                    elif glo.drawmode == 'pipette':
                        glo.drawcolour = self.gridspots[gridposx][gridposy].colour; #make the drawcolour whatever colour the user clicked on the canvas
                    elif glo.drawmode == 'clear':
                        for xp in range(self.cols):
                            for yp in range(self.rows):
                                self.gridspots[xp][yp].colour = glo.drawcolour; #clear the entire easel with the drawcolour

                if glo.isundo == True: #undo the last drawing made by looping through the last canvas save in the undolist
                    glo.isundo = False;
                    if len(glo.undolist) > 0:
                        for xpo in range(self.cols):
                            for ypo in range(self.rows):
                                self.gridspots[xpo][ypo].colour = glo.undolist[-1][xpo][ypo];
                        del glo.undolist[-1]; #delete the last item in the undo list so that you can undo even more stuff

                if glo.loadsave == True:
                    glo.loadsave = False;
                    save_file = open('save.txt', 'r');
                    if os.stat('save.txt').st_size != 0: #if the save file has something in it
                        self.cols = int(save_file.readline().strip()); #set rows and cols, and re-calculate xgap and ygap
                        self.rows = int(save_file.readline().strip());
                        self.xgap = self.xsize / self.cols;
                        self.ygap = self.ysize / self.rows;
                        #make sure that the loading grid is big enough or small enough by expanding or shrinking its size
                        while len(self.gridspots) < self.cols:
                            self.gridspots.append(pixel());
                        for gs in self.gridspots:
                            while len(gs) < self.rows:
                                self.gridspots.append(pixel());
                        
                        while len(self.gridspots) > self.cols:
                            del self.gridspots[-1];
                        for gs in self.gridspots:
                            while len(gs) > self.rows:
                                del gs[-1];
                        
                        c = 0;
                        r = 0;
                        for lines in save_file: #set all the pixels on the canvas to the save file
                            if r == self.rows:
                                r = 0;
                                c += 1;
                            self.gridspots[c][r].colour = tuple(map(float, lines.strip().split(', ')))
                            r += 1;

                if glo.save == True:
                    glo.save = False; #if saving the game, rewrite the whole save file, and save the current canvas
                    savefile = [];
                    savefile.append(str(self.cols) + '\n');
                    savefile.append(str(self.rows) + '\n');
                    for pg in range(self.cols):
                        for pgs in range(self.rows):
                            savefile.append((str(self.gridspots[pg][pgs].colour).strip('()') + '\n'));
                    with open('save.txt', 'w') as sfile:
                        sfile.writelines(savefile);

            #if exit button is hit
            if mbd:
                if self.gridspots[0][0].spotype == 'exitgame': #make sure its the right type of grid
                    if (mpos[0] > self.xpos and mpos[0] < (self.xpos + self.xsize)) and (mpos[1] > self.ypos and mpos[1] < (self.ypos + self.ysize)):
                        pygame.quit();
                        
                #change the colour to draw with
                elif self.gridspots[0][0].spotype == 'palette': #make sure its the right type of grid
                    if (mpos[0] > self.xpos and mpos[0] < (self.xpos + self.xsize)) and (mpos[1] > self.ypos and mpos[1] < (self.ypos + self.ysize)):
                        glo.drawcolour = self.gridspots[gridposx][gridposy].colour;
                        
                #change the draw mode
                elif self.gridspots[0][0].spotype == 'tools': #make sure its the right type of grid
                    if (mpos[0] > self.xpos and mpos[0] < (self.xpos + self.xsize)) and (mpos[1] > self.ypos and mpos[1] < (self.ypos + self.ysize)):
                        glo.drawmode = self.gridspots[gridposx][gridposy].mode;

                #change the draw size
                elif self.gridspots[0][0].spotype == 'drawsizes': #make sure its the right type of grid
                    if (mpos[0] > self.xpos and mpos[0] < (self.xpos + self.xsize)) and (mpos[1] > self.ypos and mpos[1] < (self.ypos + self.ysize)):
                        glo.fontsize = self.gridspots[gridposx][gridposy].font;

                #undo changed made to the canvas
                elif self.gridspots[0][0].spotype == 'undo': #make sure its the right type of grid
                    if (mpos[0] > self.xpos and mpos[0] < (self.xpos + self.xsize)) and (mpos[1] > self.ypos and mpos[1] < (self.ypos + self.ysize)):
                        glo.isundo = True;

                elif self.gridspots[0][0].spotype == 'saveload': #save or load the canvas
                    if (mpos[0] > self.xpos and mpos[0] < (self.xpos + self.xsize)) and (mpos[1] > self.ypos and mpos[1] < (self.ypos + self.ysize)):
                        if self.gridspots[gridposx][gridposy].slmode[1] == 'Save':
                            glo.save = True;
                        else:
                            glo.loadsave = True;

                #menu stuff
                if self.gridspots[0][0].spotype == 'menu': #make sure its the right type of grid
                    if (mpos[0] > self.xpos and mpos[0] < (self.xpos + self.xsize)) and (mpos[1] > self.ypos and mpos[1] < (self.ypos + self.ysize)):
                        if self.gridspots[gridposx][gridposy].size[1] == 'Start':
                            glo.ingame = True; #if start is clicked, start the drawing
                        else:
                            for sy in range(len(self.gridspots[0]) - 1): #highlight the size box in the menu
                                self.gridspots[0][sy].size[2] = False;
                                self.gridspots[0][sy].colour = BLACK;
                            self.gridspots[gridposx][gridposy].size[2] = True;
                            self.gridspots[gridposx][gridposy].colour = GRAY;
                    else:
                        for sy in range(len(self.gridspots[0]) - 1): #unhighlight them if clicked outside
                            self.gridspots[0][sy].size[2] = False;
                            self.gridspots[0][sy].colour = BLACK;

        #display the current colour
        if self.gridspots[0][0].spotype == 'colourdisplay':
            self.gridspots[0][0].colour = glo.drawcolour;
            win.blit(font.render('Colour', False, WHITE), (self.xpos - 150, self.ypos + 7))

        for rowsrep in range(len(self.gridspots)):
            for tilesrep in range(len(self.gridspots[rowsrep])): #draw all the tiles / pixels on the screen
                pygame.draw.rect(win, self.gridspots[rowsrep][tilesrep].colour, ((self.idrawx + 1 + (rowsrep * self.xgap)), (self.idrawy + (tilesrep * self.ygap)), math.ceil(self.xgap), math.ceil(self.ygap)));

        #draw the toolbar, and current mode
        if self.gridspots[0][0].spotype == 'tools':
            win.blit(font.render(glo.drawmode, False, WHITE), (self.xpos + (self.xgap * (self.cols + .25)), self.ypos))
            for tls in range(self.cols):
                win.blit(font.render(self.gridspots[tls][0].mode[0], False, WHITE), (self.xpos + (self.xgap * (tls) + (self.xgap / 4)), self.ypos + 2))

        #draw the font sizes, and current size
        elif self.gridspots[0][0].spotype == 'drawsizes':
            win.blit(font.render('px: ' + str(glo.fontsize), False, WHITE), (self.xpos + (self.xgap * (self.cols + .25)), self.ypos))
            for tls in range(self.cols):
                win.blit(font.render(str(self.gridspots[tls][0].font), False, WHITE), (self.xpos + (self.xgap * (tls) + 5), self.ypos + 2))

        #draw the "X"
        elif self.gridspots[0][0].spotype == 'exitgame':
            win.blit(font.render('X', False, WHITE), (self.xpos + 13, self.ypos + 8));

        #draw the undo and undo amount boxes and text
        elif self.gridspots[0][0].spotype == 'undo':
            win.blit(font.render(('Undos:' + str(len(glo.undolist))), False, WHITE), (self.xpos - 190, self.ypos + 7))
            win.blit(font.render('U', False, WHITE), (self.xpos + 13, self.ypos + 8));

        #draw the save / load grid
        elif self.gridspots[0][0].spotype == 'saveload':
            for sl in range(len(self.gridspots[0])):
                win.blit(font.render(self.gridspots[0][sl].slmode[1], False, WHITE), (self.xpos + 5, self.ypos + 8 + (sl * self.ygap)));

        #draw the menu grid at the beginning of the game
        elif self.gridspots[0][0].spotype == 'menu':
            for t in range(len(self.gridspots[0])):
                if t < len(self.gridspots[0]) - 1:
                    win.blit(font.render(str(self.gridspots[0][t].size[0]), False, WHITE), (self.xpos + 5, self.ypos + 8 + (t * self.ygap)));
                win.blit(font.render(self.gridspots[0][t].size[1], False, WHITE), (self.xpos + self.xsize + 5, self.ypos + 8 + (t * self.ygap)));
            win.blit(font.render('Choose Canvas Size', False, WHITE), (self.xpos - 150, self.ypos - 100));

        #draw every line between grid spots
        if self.linevisible:
            for repcol in range(self.cols+1):
                pygame.draw.line(win, WHITE, (self.idrawx + (repcol * self.xgap), self.idrawy), (self.idrawx + (repcol * self.xgap), self.fdrawy), self.vertlinewidth);

            for reprow in range(self.rows+1):
                pygame.draw.line(win, WHITE, (self.idrawx, self.idrawy + (reprow * self.ygap)), (self.fdrawx, self.idrawy + (reprow * self.ygap)), self.horlinewidth);
        #draw an outline of the grid
        elif self.outline:
            for repcol in [0, self.cols]:
                pygame.draw.line(win, WHITE, (self.idrawx + (repcol * self.xgap), self.idrawy), (self.idrawx + (repcol * self.xgap), self.fdrawy), self.vertlinewidth);

            for reprow in [0, self.rows]:
                pygame.draw.line(win, WHITE, (self.idrawx, self.idrawy + (reprow * self.ygap)), (self.fdrawx, self.idrawy + (reprow * self.ygap)), self.horlinewidth);

def drawgrids(drawlist,updt):
    win.fill(BLACK);
    for dl in drawlist:
        dl.drawgrid(updt);
    pygame.display.update(); #update the screen if the mouse is clicked

menu = True;
create = False;
indraw = False;
drawlist = [];
mbd = False;
mbu = False;


mn = pixelgrid('menu', 1, 3, (scrnwid / 2) - 80, (scrnhig / 2) - 60, 120, 180, 1, 1, True, False); #create the menu upon game start
drawgrids([mn], False); #draw the menu

while glo.ingame == False:
    for event in pygame.event.get():
        if (pygame.mouse.get_pressed()[0] == 1) or (event.type == pygame.MOUSEBUTTONDOWN) or (event.type == pygame.MOUSEBUTTONUP):
            mbu = False;
            if event.type == pygame.MOUSEBUTTONDOWN:
                mbd = True; #draw all the menu stuff, and check to see if the player clicks anything
            else:
                mbd = False;
            if event.type == pygame.MOUSEBUTTONUP:
                mbu = True;
        if event.type == pygame.KEYDOWN:
            for k in [pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9,pygame.K_0]:
                if event.key == k: #if the player types something, check to see if its one of the allowed keys, and change the text.
                    for st in range(len(mn.gridspots[0]) - 1):
                        if mn.gridspots[0][st].size[2] == True:
                            if len(str(mn.gridspots[0][st].size[0]) + '1') < 5:
                                mn.gridspots[0][st].size[0] = str(mn.gridspots[0][st].size[0]) + str((event.key) - 48);
            if event.key == pygame.K_BACKSPACE: #delete any text if there is any in the menu section
                for st in range(len(mn.gridspots[0]) - 1):
                    if mn.gridspots[0][st].size[2] == True:
                        if len(str(mn.gridspots[0][st].size[0])) > 0:
                            mn.gridspots[0][st].size[0] = str(mn.gridspots[0][st].size[0])[:-1];
            
        drawgrids([mn], True); #redraw the menu after changes have been made
    
#x = grid(gridtype, cols, rows, xpos, ypos, xsize, ysize, vertlinewidth, horlinewidth, linevisible) <-- format
gri = pixelgrid('pixel', int(mn.gridspots[0][0].size[0]), int(mn.gridspots[0][1].size[0]), 0, 0, scrnwid, scrnhig - 150, 1, 1, True, True);
palett = pixelgrid('palette', 70, 70, 4, scrnhig - 145, 140, 140, 1, 1, False, False);
colr = pixelgrid('colourdisplay', 1, 1, scrnwid - 109, scrnhig - 53, 50, 50, 1, 1, False, True);
tool = pixelgrid('tools', 6, 1, 150, scrnhig - 65, 240, 40, 1, 1, True, False);
drawsz = pixelgrid('drawsizes', len(fontlist), 1, 150, scrnhig - 125, len(fontlist) * 50, 40, 1, 1, True, False);
exitg = pixelgrid('exitgame', 1, 1, scrnwid - 53, scrnhig - 53, 50, 50, 1, 1, False, True);
und = pixelgrid('undo', 1, 1, scrnwid - 53, scrnhig - 147, 50, 50, 1, 1, False, True);
saveloa = pixelgrid('saveload', 1, 2, (scrnwid / 2) + 50, scrnhig - 120, 100, 100, 1, 1, True, False); #create all the necessities for the drawing game thing

glo.drawlist = [gri,palett,colr,tool,drawsz,exitg,und,saveloa]; #make a new drawlist for drawing the creen
drawgrids(glo.drawlist,False); #update the screen

inwait = True; #make sure that the user isnt doing anything. If this wasnt here, the player would automatically click the canvaas once at the beginning of the game.
while inwait:   #this is the cheapo way of a bug fix :)
    for event in pygame.event.get():
        inwait = True;
    else:
        inwait = False;

while glo.ingame: #if the user clicks, make changes, and update the screen.
    for event in pygame.event.get():
        if (pygame.mouse.get_pressed()[0] == 1) or (event.type == pygame.MOUSEBUTTONDOWN) or (event.type == pygame.MOUSEBUTTONUP):
            mbu = False;
            if event.type == pygame.MOUSEBUTTONDOWN:
                mbd = True;
            else:
                mbd = False;
            if event.type == pygame.MOUSEBUTTONUP:
                mbu = True;

            drawgrids(glo.drawlist,True);

pygame.quit()
