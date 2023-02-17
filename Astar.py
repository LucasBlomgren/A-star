import pygame
import math
pygame.init()

width = 960
height = 960
screen = pygame.display.set_mode([width, height])
clock = pygame.time.Clock()
FPS = 60
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
        self.g_cost = 0

        self.parent = None
        self.start = False
        self.end = False
    
    def reset(self):
        self.closed = None
        self.open = False
        self.path = False

        self.f_cost = 0
        self.h_cost = 0
        self.g_cost = 0

        self.parent = None

        if not self.obstacle and not self.start and not self.end:
            self.color = [255,255,255]

    def make_obstacle(self):
        self.obstacle = True
        self.color = [0,0,0]
    
    def make_traversable(self):
        self.obstacle = False
        self.color = [255,255,255]

    def make_closed(self):
        self.closed = True
    
    def update_h_cost(self, end):
        self.h_cost = math.sqrt(math.pow(self.x_cell - end[0], 2) + math.pow(self.y_cell - end[1], 2))

    def update_f_cost(self):
        self.f_cost = self.g_cost + self.h_cost

    def draw(self):
        
        if self.path:
           self.color = [102,0,204]
        elif self.open:
            self.color = [0,255,0]
        elif self.closed:
            self.color = [255,0,0]
        elif self.start:
            self.color = [255,128,0]
        elif self.end:
            self.color = [0,0,255]
        elif not self.obstacle:
            self.color = [255,255,255]

        pygame.draw.rect(screen, self.color, [self.x_coord, self.y_coord, node_size, node_size])

def pathfind(grid, start, end):

    if start == None or end == None:
        return
    
    end_cell = end

    create_neighbors(grid)

    for row in grid:
        for node in row:
            node.reset()
            node.update_h_cost(end_cell)

    start = grid[start[0]][start[1]]
    end = grid[end[0]][end[1]]

    open = []
    closed = []
    open.append(start)
    start.closed = False
    start.open = True

    while True:

        if len(open) < 1:
            return

        open.sort(key = lambda i: i.f_cost)

        current = open[0]
        open.pop(0)
        closed.append(current)
        current.open = False
        current.closed = True

        if current == end:

            path = []
            current = end
            while current != start:

                path.append(current)
                current.path = True
                current = current.parent
            return
        
        for neighbor in current.neighbors:
            if neighbor.obstacle == True or neighbor.closed == True:
                continue
            
            if (current.g_cost + 1 < neighbor.g_cost) or neighbor.open == False:
                if (current.g_cost + 1 < neighbor.g_cost):
                    neighbor.g_cost = current.g_cost + 1
            
                neighbor.update_f_cost()
                neighbor.parent = current

                if neighbor.open == False:
                    open.append(neighbor)
                    neighbor.open = True

def create_nodes(rows, cols):
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

def create_neighbors(grid):

    #CLEAR NEIGHBORS
    for y, row in enumerate(grid):
        for x, node in enumerate(row):
            node.neighbors = []

    #CREATE NEIGHBORS
    for y, row in enumerate(grid):
        for x, node in enumerate(row):
            #NORTH
            if y > 0:
                if grid[y-1][x].obstacle == False:
                    node.neighbors.append(grid[y-1][x])
            #WEST
            if x > 0:
                if grid[y][x-1].obstacle == False:
                    node.neighbors.append(grid[y][x-1])
            #EAST
            if x < rows-1:
                if grid[y][x+1].obstacle == False:
                    node.neighbors.append(grid[y][x+1])
            #SOUTH
            if y < cols-1:
                if grid[y+1][x].obstacle == False:
                    node.neighbors.append(grid[y+1][x])
    
def draw(grid):
    screen.fill([255,255,255])

    for row in grid:
        for node in row:
            node.draw()

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

grid = create_nodes(rows, cols)

while run:

    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                start = mx // node_size, my // node_size
                for row in grid:
                    for node in row:
                        node.start = False
                grid[start[0]][start[1]].start = True
            
            elif event.key == pygame.K_e:
                end = mx // node_size, my // node_size
                for row in grid:
                    for node in row:
                        node.end = False
                grid[end[0]][end[1]].end = True

            elif event.key == pygame.K_ESCAPE:
                run = False

            elif event.key == pygame.K_SPACE:
                pathfind(grid, start, end)
            
            elif event.key == pygame.K_c:
                for row in grid:
                    for node in row:
                        node.reset()
    
    mouse = pygame.mouse.get_pressed()
    if mouse[0]:
        grid[mx // node_size][my // node_size].make_obstacle()

    if mouse[2]:
        grid[mx // node_size][my // node_size].make_traversable()

    
    draw(grid)
    
    clock.tick(FPS)
    pygame.display.flip()
