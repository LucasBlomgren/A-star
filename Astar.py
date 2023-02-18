import pygame
import math
pygame.init()

width = 960
height = 960
screen = pygame.display.set_mode([width, height])
clock = pygame.time.Clock()
FPS = 240
run = True

node_size = 20
rows = width // node_size
cols = height // node_size

class Node():
    def __init__(self, y, x):
        self.obstacle = False
        self.neighbors = []
        self.color = [255,255,255]

        self.x_cell = x
        self.y_cell = y

        self.x_coord = self.x_cell * node_size
        self.y_coord = self.y_cell * node_size

        self.closed = None
        self.open = False
        self.path = False

        self.f_cost = 0
        self.h_cost = 0
        self.g_cost = float('inf')

        self.parent = None
        self.start = False
        self.end = False

        self.manhattan = True
    
    def reset(self):
        self.closed = None
        self.open = False
        self.path = False

        self.f_cost = 0
        self.h_cost = 0
        self.g_cost = float('inf')

        self.parent = None

    def make_obstacle(self):
        self.obstacle = True
        self.color = [0,0,0]
    
    def make_traversable(self):
        self.obstacle = False
        self.color = [255,255,255]

    def make_closed(self):
        self.closed = True
    
    def update_h_cost(self, end):

        if self.manhattan:
            self.h_cost = abs(self.x_cell - end[0]) + abs(self.y_cell - end[1])
        else: 
            self.h_cost = math.sqrt(math.pow(self.x_cell - end[0], 2) + math.pow(self.y_cell - end[1], 2))

    def update_f_cost(self):
        self.f_cost = self.g_cost + self.h_cost

    def draw(self):

        if not self.obstacle:

            if self.start:
                self.color = [255,255,0]

            elif self.end:
                self.color = [0,255,255]

            elif self.path:
                self.color = [102,0,204]
            
            elif self.open:
                self.color = [0,255,0]
            
            elif self.closed:
                self.color = [255,0,0]
            
            else:
                self.color = [255,255,255]
    
        pygame.draw.rect(screen, self.color, [self.x_coord, self.y_coord, node_size, node_size])

class Astar():
    def __init__(self):
        
        self.grid = self.create_nodes(rows, cols)

        self.start = None
        self.end = None
        self.open = []
        self.current = None
        self.path = []

        self.running = False
        self.realtime = False
        self.draw_path = False

        self.count = 0

    def pathfind(self, start, end):

        if start == None or end == None:
            return
        
        end_cell = end

        self.create_neighbors()

        for row in self.grid:
            for node in row:
                node.reset()
                node.update_h_cost(end_cell)

        self.start = self.grid[start[0]][start[1]]
        self.end = self.grid[end[0]][end[1]]

        self.start.g_cost = 0

        self.open = []
        self.open.append(self.start)
        self.start.closed = False
        self.start.open = True
    
        self.loop()
    
    def loop(self):

        self.running = True
        self.draw_path = False

        while True:

            if len(self.open) < 1:
                return
            
            self.open.sort(key = lambda i: i.f_cost)

            self.current = self.open[0]
            self.open.pop(0)
            self.current.open = False
            self.current.closed = True

            if self.current == self.end:

                self.path = []
                self.current = self.end
                while self.current != self.start:

                    self.path.append(self.current)
                    self.current = self.current.parent

                    if self.realtime:
                        self.current.path = True
                
                self.path.reverse()
                self.draw_path = True
                self.running = False
                return
            
            for neighbor in self.current.neighbors:
                if neighbor.obstacle == True or neighbor.closed == True:
                    continue
                
                if (self.current.g_cost + 1 < neighbor.g_cost) or neighbor.open == False:
                    if (self.current.g_cost + 1 < neighbor.g_cost):
                        neighbor.g_cost = self.current.g_cost + 1
                
                    neighbor.update_f_cost()
                    neighbor.parent = self.current

                    if neighbor.open == False:
                        self.open.append(neighbor)
                        neighbor.open = True

            if not self.realtime:
                return
            

    def create_nodes(self, rows, cols):
        #CREATE GRID
        grid = []
        y=0
        for _ in range(rows):
            row = []
            x=0
            for _ in range(cols):
                node = Node(x,y)
                row.append(node)
                x+=1
            y+=1
            grid.append(row)
        
        return grid

    def create_neighbors(self):

        #CLEAR NEIGHBORS
        for y, row in enumerate(self.grid):
            for x, node in enumerate(row):
                node.neighbors = []

        #CREATE NEIGHBORS
        for y, row in enumerate(self.grid):
            for x, node in enumerate(row):
                #NORTH
                if y > 0:
                    if self.grid[y-1][x].obstacle == False:
                        node.neighbors.append(self.grid[y-1][x])
                #WEST
                if x > 0:
                    if self.grid[y][x-1].obstacle == False:
                        node.neighbors.append(self.grid[y][x-1])
                #EAST
                if x < rows-1:
                    if self.grid[y][x+1].obstacle == False:
                        node.neighbors.append(self.grid[y][x+1])
                #SOUTH
                if y < cols-1:
                    if self.grid[y+1][x].obstacle == False:
                        node.neighbors.append(self.grid[y+1][x])
    
    def update(self):

        self.count += 1

        if self.draw_path and len(self.path) > 0 and self.count >= 5 and self.realtime == False:
            self.path[0].path = True
            self.path.pop(0)
            self.count = 0

        for row in self.grid:
            for node in row:
                node.draw()
        
        if self.running:
            self.loop()


def draw(grid):

    i=0
    for i in range(rows):
        pygame.draw.line(screen, [135,135,135], [0, i * node_size], [width, i * node_size])
        i+=1
    i=0
    for i in range(cols):
        pygame.draw.line(screen, [135,135,135], [i * node_size, 0], [i * node_size, height])
        i+=1
        
start = None
end = None

astar = Astar()

while run:

    screen.fill([255,255,255])
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                start = mx // node_size, my // node_size
                for row in astar.grid:
                    for node in row:
                        node.start = False
                astar.grid[start[0]][start[1]].start = True

                if start != None and end != None:
                    astar.pathfind(start, end)
            
            elif event.key == pygame.K_e:
                end = mx // node_size, my // node_size
                for row in astar.grid:
                    for node in row:
                        node.end = False
                astar.grid[end[0]][end[1]].end = True

                if start != None and end != None:
                    astar.pathfind(start, end)

            elif event.key == pygame.K_ESCAPE:
                run = False

            elif event.key == pygame.K_SPACE:
                astar.pathfind(start, end)
            
            elif event.key == pygame.K_q:
                astar.realtime = not astar.realtime
            
            elif event.key == pygame.K_a:
                for row in astar.grid:
                    for node in row:
                        node.manhattan = not node.manhattan
    
    mouse = pygame.mouse.get_pressed()
    if mouse[0]:
        astar.grid[mx // node_size][my // node_size].make_obstacle()
        astar.pathfind(start, end)

    if mouse[2]:
        astar.grid[mx // node_size][my // node_size].make_traversable()
        astar.pathfind(start, end)

    astar.update()
    draw(astar.grid)
    
    clock.tick(FPS)
    pygame.display.flip()
