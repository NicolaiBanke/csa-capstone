from random import randint
from heapq import heappop, heappush
from sort import *
#can't import inf in my version of python
inf = 1e+140

#including and argument to set the number of moves made whe mowing
def mow(grid, i, j, mow_number):
  directions = ["U", "D", "L", "R"]
  while directions:
    directions_index = randint(0, len(directions) - 1)
    direction = directions.pop(directions_index)
    if direction == "U":
      if i - mow_number < 0:
        continue
      elif grid[i - mow_number][j] == "wall":
        for m in range(1, mow_number + 1):
          grid[i - m][j] = 'empty'
        mow(grid, i - mow_number, j, mow_number)
    elif direction == "D":
      if i + mow_number >= len(grid):
        continue
      elif grid[i + mow_number][j] == 'wall':
        for m in range(1, mow_number + 1):
          grid[i + m][j] = 'empty'
        mow(grid, i + mow_number, j, mow_number)
    elif direction == "L":
      if j - mow_number < 0:
        continue
      elif grid[i][j - mow_number] == 'wall':
        for m in range(1, mow_number + 1):
          grid[i][j - m] = 'empty'
        mow(grid, i, j - mow_number, mow_number)
    else:
      if j + mow_number >= len(grid[0]):
        continue
      elif grid[i][j + mow_number] == 'wall':
        for m in range(1, mow_number + 1):
          grid[i][j + m] = 'empty'
        mow(grid, i, j + mow_number, mow_number)

#including an argument to set how often the swag is dropped
def explore_maze(grid, start_i, start_j, swag, swag_frequency):
  grid_copy = [row[:] for row in grid]
  bfs_queue = [[start_i, start_j]]
  directions = ['U', 'D', 'L', 'R']
  
  while bfs_queue:
    i, j = bfs_queue.pop(0)
    if randint(1, 100) <= swag_frequency and grid[i][j] != 'start':
      grid[i][j] = swag[randint(0, len(swag) - 1)]
    grid_copy[i][j] = 'visited'
    for direction in directions:
      explore_i, explore_j = i, j
      if direction == 'U':
        explore_i = i - 1
      elif direction == 'D':
        explore_i = i + 1
      elif direction == 'L':
        explore_j = j - 1
      else:
        explore_j = j + 1
      if explore_i < 0 or explore_j < 0 or explore_i >= len(grid) or explore_j >= len(grid[0]):
        continue
      elif grid_copy[explore_i][explore_j] != 'visited' and grid_copy[explore_i][explore_j] != 'wall':
        bfs_queue.append([explore_i, explore_j])
  grid[i][j] = 'end'

def build_maze(m, n, swag, mow_number, swag_frequency):
  grid = [["wall" for j in range(n)] for i in range(m)]
  start_i = randint(0, m - 1)
  start_j = randint(0, n - 1)
  grid[start_i][start_j] = "start"
  mow(grid, start_i, start_j, mow_number)
  explore_maze(grid, start_i, start_j, swag, swag_frequency)
  return grid

def print_maze(grid):
  for row in grid:
    printable_row = ""
    for cell in row:
      if cell == 'wall':
        char = '|'
      elif cell == 'empty':
        char = ' '
      else:
        char = cell[0]
      printable_row += char
    print(printable_row)

#based on the print_maze function above this function prints the maze with a given path
def print_solved_maze(grid, solution):
  grid_copy = [row[:] for row in grid]
  for point in solution:
    if grid_copy[point[0]][point[1]] != "start" and grid_copy[point[0]][point[1]] != "end":
      grid_copy[point[0]][point[1]] = 'path'
      
  for row in grid_copy:
    printable_row = ""
    for cell in row:
      if cell == 'wall':
        char = '|'
      elif cell == 'empty':
        char = ' '
      elif cell == 'path':
        char = '*'
      else:
        char = cell[0]
      printable_row += char
    print(printable_row)

#values assigned to the different items that can be picked up with disirable items having negative values to minimize path
swag_values = {
  "start": 0, 
  "end": 0,
  "empty": 0,
  'candy corn': -2,
  'werewolf': 2,
  'pumpkin pie': -1,
  'yams': -2,
  'quorthon minion': 1,
  'nog': -1,
  'rancor': 3,
  'twix': -4,
  'uruk-hai': 4,
  'ice cream': -5,
  'oreos': -2,
  'aids needle': 5,
  'diamond': -6,
  'fuck buddy': -3,
  'gold': -6,
  'heckler': 1,
  'jamba juice': -1,
  'kickboxer': 2,
  'lamb chops': -3,
  'zoso symbol': -4,
  'x-man': 3,
  'vegetables': -1,
  'beer': -5,
  'medusa': 6
}

swag = list(swag_values.keys())
swag.remove("start")
swag.remove("empty")
swag.remove("end")

#find the coordinates (i, j) of a point labeled with the argument point
def find_point(maze, point):
  for i in range(len(maze)):
    for j in range(len(maze[i])):
      if maze[i][j] == point:
        return i, j

#given a point (i, j) this returns the labels of the point's four neighbors in the grid
def find_neighbors(i, j):
  neighbors = [
    maze[i+1][j] if i + 1 < len(maze) else None,
    maze[i-1][j] if i > 0 else None,
    maze[i][j+1] if j + 1 < len(maze[0]) else None,
    maze[i][j-1] if j > 0 else None
  ]
  return neighbors

#returns True if the point (i j) is an intersection as defined in the return statement
def is_intersection(i, j):
  if maze[i][j] == "wall":
    return False
  neighbors = find_neighbors(i, j)
  return neighbors.count("wall") + neighbors.count(None) < 2

#returns True if the point (i j) is a blind alley as defined in the return statement
def is_blind_alley(i, j):
  if maze[i][j] == "wall" or (maze[i][j] == "start" or maze[i][j] == "end"):
    return False
  neighbors = find_neighbors(i, j)
  return neighbors.count("wall") + neighbors.count(None) == 3

#goes around clockwise to find the neighbors of (i, j) that are free to step on
def find_free_neighbors(i, j, maze):
  maze_copy = [row[:] for row in maze]
  free_neighbors = []
  if j + 1 < len(maze_copy[i]):
    if maze_copy[i][j+1] != "wall" and maze_copy[i][j+1] != "visited":
      free_neighbors.append((i, j+1))
  
  if i - 1 >= 0:
    if maze_copy[i-1][j] != "wall" and maze_copy[i-1][j] != "visited":
      free_neighbors.append((i-1, j))
  
  if j - 1 >= 0:
    if maze_copy[i][j-1] != "wall" and maze_copy[i][j-1] != "visited":
      free_neighbors.append((i, j-1))
  
  if i + 1 < len(maze_copy):
    if maze_copy[i+1][j] != "wall" and maze_copy[i+1][j] != "visited":
      free_neighbors.append((i+1, j))
    
  return free_neighbors

#takes a maze and represents it as a graph data structure 
def graph(maze):
  start = (find_point(maze, "start"), "start")
  vertices = {}
  #each point that isn't a wall is mapped to a list of its free neighbors with their corresponding value in the grid
  for i in range(len(maze)):
    for j  in range(len(maze[i])):
      if maze[i][j] != "wall":
        free_neighbors = find_free_neighbors(i, j, maze)
        vertices[(i, j)] = [(free_neighbor, maze[free_neighbor[0]][free_neighbor[1]]) for free_neighbor in free_neighbors]

  #the vertices need to be fixed so that any two neighbors don't point to each other in order to make the graph directed
  to_be_fixed = [start]
  while to_be_fixed:
    current_point = to_be_fixed.pop(0)
    next_points = vertices[current_point[0]]
    for next_point in next_points:
      if current_point in vertices[next_point[0]]:
        vertices[next_point[0]].remove(current_point)
      to_be_fixed.append(next_point)
  return vertices

#dijkstra's algorithm is modified to also include and ending point and return the entire path and swag collected along the way
def dijkstra_with_paths(graph_maze, start, end):
  distances_and_paths = {}
  collected_swag = []
  for vertex in graph_maze:
    distances_and_paths[vertex] = [inf, [start]]
  distances_and_paths[start][0] = 0
  vertices_to_explore = [(0, start)]
  
  while vertices_to_explore:
    current_distance, current_vertex = heappop(vertices_to_explore)
    for free_neighbor, swag_item in graph_maze[current_vertex]:
      swag_weight = swag_values[swag_item]
      new_distance = current_distance + swag_weight
      new_path = distances_and_paths[current_vertex][1] + [free_neighbor]
      
      if new_distance < distances_and_paths[free_neighbor][0]:
        distances_and_paths[free_neighbor][0] = new_distance
        distances_and_paths[free_neighbor][1] = new_path
        
        if swag_values[swag_item] < 0:
          collected_swag.append(swag_item)
        heappush(vertices_to_explore, (new_distance, free_neighbor))
  collected_swag = merge_sort(collected_swag)
  return distances_and_paths[end], collected_swag

#manhattan heuristic
def heuristic(start, end):
  start_i, start_j = start
  end_i, end_j = end
  i_distance = abs(start_i - end_i)
  j_distance = abs(start_j - end_j)
  return (i_distance + j_distance)

def euclidean_heuristic(start, end):
  start_i, start_j = start
  end_i, end_j = end
  i_distance2 = (start_i - end_i)**2
  j_distance2= (start_j - end_j)**2
  return (i_distance2 + j_distance2)**.5


def a_star(graph_maze, start, end, heuristic):
  distances_and_paths = {}
  collected_swag = []
  for vertex in graph_maze:
    distances_and_paths[vertex] = [inf, [start]]
  distances_and_paths[start][0] = 0
  vertices_to_explore = [(0, start)]
  
  while vertices_to_explore and distances_and_paths[end][0] == inf:
    current_distance, current_vertex = heappop(vertices_to_explore)
    for free_neighbor, swag_item in graph_maze[current_vertex]:
      swag_weight = swag_values[swag_item]
      new_distance = current_distance + swag_weight + heuristic(free_neighbor, end)
      new_path = distances_and_paths[current_vertex][1] + [free_neighbor]
      
      if new_distance < distances_and_paths[free_neighbor][0]:
        distances_and_paths[free_neighbor][0] = new_distance
        distances_and_paths[free_neighbor][1] = new_path
        
        if swag_values[swag_item] < 0:
          collected_swag.append(swag_item)
        heappush(vertices_to_explore, (new_distance, free_neighbor))
  
  collected_swag = merge_sort(collected_swag)
  return distances_and_paths[end], collected_swag

#size of the maze
m, n = 20, 20
swag_frequency = 60

#scale the swag_values to the size of the maze so that the effect of the heuristic becomes more apparent
for key, value in swag_values.items():
  swag_values[key] = value

maze = build_maze(m, n, swag, 2, swag_frequency)
graph_maze = graph(maze)
print_maze(maze)

start = find_point(maze, "start")
end = find_point(maze, "end")
dijk = dijkstra_with_paths(graph_maze, start, end)
a = a_star(graph_maze, start, end, heuristic)

print("|" + 10*"-" + "Dijkstra" + 10*"-" + "|")
print("Solution is {0} steps long".format(len(dijk[0][1])))
print("Found {0} swag items".format(len(dijk[1])))

print_solved_maze(maze, dijk[0][1])


print("|" + 10*"-" + "A*" + 10*"-" + "|")
print("Solution is {0} steps long".format(len(a[0][1])))
print("Found {0} swag items".format(len(a[1])))

print_solved_maze(maze, a[0][1])