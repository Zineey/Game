import random as random    
import pygame as pygame
import sys
from tkinter import messagebox


pygame.init()                      
pygame.display.set_caption('Dijkstra? More like Dijka papasa')
clock = pygame.time.Clock()                   
height, width = 650, 650

screen = pygame.display.set_mode((height,width))
running = True                                 
row = 10
column = 10                         

TileWidth = width//column    
TileHeight = height//row
TileMargin = 2

BLACK = (0, 0, 0)                            
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)

class MapTile(object):                      
    def __init__(self, Name, Column, Row):
        self.Name = Name
        self.Column = Column
        self.Row = Row

class Goal(object):
    def __init__(self, Name, Column, Row):
        self.Name = Name    
        self.Column = Column
        self.Row = Row

class Character(object):                   
    def __init__(self, Name, Column, Row):
        self.Name = Name    
        self.Column = Column
        self.Row = Row

    def Move(self, Direction): 
        if Direction == "UP":
            if self.Row > 0:  
                if self.CollisionCheck("UP") == False:      
                    self.Row -= 1 
                if self.Win() == True:
                    messagebox.showinfo("Game Over", "You Win!")
                    # sys.exit()  
                
        elif Direction == "LEFT":
            if self.Column > 0:
                if self.CollisionCheck("LEFT") == False:
                    self.Column -= 1
                if self.Win() == True: 
                    messagebox.showinfo("Game Over", "You Win!")
                    # sys.exit() 
                
        elif Direction == "RIGHT":
            if self.Column < column-1:
                if self.CollisionCheck("RIGHT") == False:
                    self.Column += 1
                if self.Win() == True:
                    messagebox.showinfo("Game Over", "You Win!")
                    # sys.exit()  
                
        elif Direction == "DOWN":
            if self.Row < row-1:
                if self.CollisionCheck("DOWN") == False:
                    self.Row += 1
                if self.Win() == True:
                    messagebox.showinfo("Game Over", "You Win!")
                    # sys.exit()  
                
        Map.mapUpdate()       

    def CollisionCheck(self, Direction):  
        if Direction == "UP":
            if len(Map.Grid[self.Column][(self.Row)-1]) > 1:
                # print(len(Map.Grid[self.Column][(self.Row)-1]))
                return True
        elif Direction == "LEFT":
            if len(Map.Grid[self.Column-1][(self.Row)]) > 1:
                return True
        elif Direction == "RIGHT":
            if len(Map.Grid[self.Column+1][(self.Row)]) > 1:
                return True
        elif Direction == "DOWN":
            if len(Map.Grid[self.Column][(self.Row)+1]) > 1:
                return True
        return False
    
    def Win(self):
        if self.Column == Map.Goal.Column and self.Row == Map.Goal.Row:
            return True
        
    def Location(self):
        print("Coordinates: " + str(self.Column) + ", " + str(self.Row))


class Map():
    global row, column

    Grid = []
    # Creating grid
    for Rows in range(row):    
        Grid.append([])
        for Columns in range(column):
            Grid[Rows].append([])

    # Player Spawn
    playerRow = random.randint(0, row - 1)      
    playerColumn = random.randint(0, column - 1)
    playerPos = Character("Player", playerColumn, playerRow)

    #Goal
    goalRow = random.randint(0, row - 1)      
    goalColumn = random.randint(0, column - 1)
    Goal = Goal("Goal", goalColumn, goalRow)     
    Grid[goalColumn][goalRow].append(Goal)     

    # Floors/Available Paths
    for Rows in range(row):    
        for Columns in range(column):
            TempTile = MapTile("Floor", Columns, Rows)
            if TempTile.Column  == Goal.Column and TempTile.Row == Goal.Row:
                pass
            else:
                Grid[Columns][Rows].append(TempTile)



    #Placing Random Walls
    for i in range(50):
        RandomRow = random.randint(0, row - 1)
        RandomColumn = random.randint(0, column - 1)
        TempTile = MapTile("Wall", RandomColumn, RandomRow)
        Grid[RandomColumn][RandomRow].append(TempTile)
        


    def mapUpdate(self):
        for Columns in range(column):      
            for Rows in range(row):
                for i in range(len(Map.Grid[Columns][Rows])):
                    if Map.Grid[Columns][Rows][i].Column != Columns:
                        Map.Grid[Columns][Rows].remove(Map.Grid[Columns][Rows][i])
                    elif Map.Grid[Columns][Rows][i].Name == "Player":
                        Map.Grid[Columns][Rows].remove(Map.Grid[Columns][Rows][i])
        Map.Grid[int(Map.playerPos.Column)][int(Map.playerPos.Row)].append(Map.playerPos)

Map = Map()

while running:
    for event in pygame.event.get():            
        if event.type == pygame.QUIT:           
            running = False             
            pygame.quit()     
            sys.exit()   
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            Pos = pygame.mouse.get_pos()
            Column = Pos[0] // (TileWidth + TileMargin)  #Translating the position of the mouse into rows and columns
            Row = Pos[1] // (TileHeight + TileMargin)
            print(str(Row) + ", " + str(Column))

            for i in range(len(Map.Grid[Column][Row])):
                print(str(Map.Grid[Column][Row][i].Name))  #print stuff that inhabits that square

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        Map.playerPos.Move("UP")
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        Map.playerPos.Move("DOWN")
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        Map.playerPos.Move("LEFT")
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        Map.playerPos.Move("RIGHT")

    # Tile Grid
    screen.fill((0,0,0))                        
    for Rows in range(row):                 
        for Columns in range(column): 
            Color = WHITE  
            for i in range(0, len(Map.Grid[Columns][Rows])):
                # Wall
                if Map.Grid[Columns][Rows][i].Name == "Wall":
                    Color = BROWN
                # Goal
                if Map.Grid[Columns][Rows][i].Name == "Goal":
                    Color = BLUE
                # Player 
                if Map.Grid[Columns][Rows][i].Name == "Player":
                    Color = GREEN
                    
            # Map Grid
            # Color = WHITE
            pygame.draw.rect(screen, Color ,[Columns * TileWidth, #left
                                            Rows * TileHeight, #top
                                            TileWidth - TileMargin,
                                            TileHeight - TileMargin])
            

    clock.tick(10)   
    Map.mapUpdate()                        
    pygame.display.flip()
    