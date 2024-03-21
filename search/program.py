# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress

from .core import PlayerColor, Coord, PlaceAction
from .utils import render_board

import math

import heapq

class Action:
    def __init__(self, Parent, numF, locs, numG, numH):
        self.Parent = Parent
        self.numF = numF
        self.locs = locs
        self.numG = numG
        self.numH = numH
    def __lt__(self, other):
        return self.numF < other.numF



def search(
    board: dict[Coord, PlayerColor],
    target: Coord
) -> list[PlaceAction] | None:
    """
    This is the entry point for your submission. You should modify this
    function to solve the search problem discussed in the Part A specification.
    See `core.py` for information on the types being used here.

    Parameters:
        `board`: a dictionary representing the initial board state, mapping
            coordinates to "player colours". The keys are `Coord` instances,
            and the values are `PlayerColor` instances.  
        `target`: the target BLUE coordinate to remove from the board.
    
    Returns:
        A list of "place actions" as PlaceAction instances, or `None` if no
        solution is possible.
    """

    # The render_board() function is handy for debugging. It will print out a
    # board state in a human-readable format. If your terminal supports ANSI
    # codes, set the `ansi` flag to True to print a colour-coded version!
    print(render_board(board, target, ansi=False))
    
    red_Loc = [] #存储红色坐标的坐标
    Curr_Empty = [] #目前没颜色的坐标
    blue_Loc = [] # 蓝色的坐标
    num_of_search = 0
    
    state = find_red(board)
    red_Loc= state[0]
    blue_Loc=state[1]


    # 找到了所有颜色为空的坐标
    Curr_Empty = find_Curr_empty(red_Loc, blue_Loc)
    
    #找到了红色坐标周围可以连接图形的坐标
    connect=[]
    for i in red_Loc:
        temp = check_around_2(i, Curr_Empty)
        connect.extend(temp)
        
    print(connect)
    #  creat instance of point
    
    # 遍历可以连接图形的坐标， 找到当前所有可以进行的action
    valid_action = []
    for i in connect:
        res = []
        res = relative_shape(i, Curr_Empty)
        valid_action.extend(res)
    
    print(valid_action)
    OpenAction = []
    closeList = []
    for loc in valid_action:
        current_fn = calculate_fn(target, num_of_search, loc)
        h = min(calculate_distance(i, target) for i in loc)
        heapq.heappush(OpenAction, Action(None, current_fn, loc, num_of_search, h))
    
   #while OpenAction:
    #   print(heapq.heappop(OpenAction).numF)
    """
    flag = False
    while OpenAction:
        currentNode = heapq.heappop(OpenAction)
        heapq.heappush(closeList, currentNode)

        for i in currentNode.locs:
           if i == target:
                flag == True
                break
        if flag:
           break

        (new_board, empty_list, updated_red) = update_state(board, currentNode)

        children = get_valid_action(empty_list, updated_red[0])
        for child in children:
            if i in closeList:
                continue
            numG = currentNode.numG+ 1
            numH = min(calculate_distance(loc, target) for loc in child)
            numF = child.g + child.h    
            if child in OpenAction:
                if child.g > num_of_search:
                    continue
            heapq.heappush(OpenAction, Action(currentNode,numF, child, numG, numH))  
    """
    
    # ...
    # ... (your solution goes here!)

    # ...

    # Here we're returning hardcoded" actions as an example of the expected
    # output format. Of course, you should instead return the result of your
    # search algorithm. Remember: if no solution is possible for a given input,
    # return `None` instead of a list.
    return [
        PlaceAction(Coord(2, 5), Coord(2, 6), Coord(3, 6), Coord(3, 7)),
        PlaceAction(Coord(1, 8), Coord(2, 8), Coord(3, 8), Coord(4, 8)),
        PlaceAction(Coord(5, 8), Coord(6, 8), Coord(7, 8), Coord(8, 8)),
    ]

def add_to_heap(valid_action, target, num_of_search, OpenAction):
    for loc in valid_action:
        current_fn = calculate_fn(target, num_of_search, loc)
        heapq.heappush(OpenAction, Action(None, current_fn, loc, num_of_search))
    return OpenAction
    

def get_valid_action(red_Loc, Curr_Empty):
    connect=[]
    for i in red_Loc:
        temp = check_around_2(i, Curr_Empty)
        connect.extend(temp)
    valid_action = []
    for i in connect:
        res = []
        res = relative_shape(i, Curr_Empty)
        valid_action.extend(res)
    return valid_action
    

def find_red(board):
    red_Loc = []
    blue_Loc = []
    for i in board.keys():
        if (board[i]== PlayerColor.RED):
            red_Loc.append(i)
        elif (board[i] == PlayerColor.BLUE):
           blue_Loc.append(i)
    return [red_Loc,blue_Loc]


def find_Curr_empty(red_Loc, blue_Loc):
    Curr_Empty = []
    for i in range(11):
        for j in range(11):
            loc = Coord(i,j)
            if loc in red_Loc or loc in blue_Loc:
                continue
            else:
                Curr_Empty.append(loc)
    return Curr_Empty

def check_around_2(i, empty_list):
    visited_list = []
    up = Coord(i.r - 1, i.c) if i.r-1 >= 0 else Coord(10, i.c)
    left = Coord(i.r, i.c - 1) #if i.c-1 >= 0 else Coord(i.r, 10)
    right = Coord(i.r, i.c + 1) #if i.c-1 >= 10 else Coord(i.r, 0)
    down = Coord(i.r + 1, i.c) if i.r+1 <= 10 else Coord(0,i.c)
    if left in empty_list:
        visited_list.append(left)
    if right in empty_list:
        visited_list.append(right)
    if up in empty_list:
        visited_list.append(up)
    if down in empty_list:
        visited_list.append(down)
    return visited_list        




# 所有相对位置的坐标
tetromino_shape = {
    'I': [[(0, 0), (0, 1), (0, 2), (0, 3)], [(0, 0), (1, 0), (2, 0), (3, 0)]],
    'O': [[(0, 0), (0, 1), (1, 0), (1, 1)]],
    'T': [[(0, 0), (0, 1), (-1, 1), (1, 1)], [(0, 0), (-1,0), (1, 0), (0, 1)],
          [(0, 0), (0, 1), (0, 2), (1, 1)], [(-1, 1), (0, 0), (0, 1), (0, 2)]],
    'J': [[(0, 0), (1, 0), (2, 0), (2, -1)], [(0, 0), (1, 0), (1, 1), (1, 2)],
          [(0, 0), (0, 1), (2, 0), (1, 0)], [(0, 0), (0, 1), (0, 2), (1, 2)]],
    'L': [[(0, 0), (1, 0), (2, 0), (2, 1)], [(0, 0), (0, 1), (0, 2), (1, 0)],
          [(0, 0), (0, 1), (1, 1), (2,1 )], [(0, 0), (0, 1), (0, 2), (-1, 2)]],
    'Z': [[(0, 0), (0, 1), (1, 1), (1, 2)], [(0, 0), (0, 1), (1, 0), (-1, 1)]],
    'S': [[(0, 0), (0, 1), (-1, 1), (-1, 2)], [(0, 0), (-1, 0), (0, 1), (1, 1)]]
}

#对于每个图形的相对位置， 进行检测
def relative_shape(coord,Non_color):
    res = []
    for shapes in tetromino_shape.values():
        # shape 是[(),(),(),()]一组图形的坐标
        for shape in shapes:
            list = return_shape(shape, coord, Non_color)
            if len(list) != 0:
                res.extend(list)
            #print(list)
    return res
            

# 单个坐标的对于一个图形内部的四种位移
def return_shape(shape, loc, Non_color):
    res=[]
    #loc 是贴着红色的坐标
    #Non_ color 是当前没颜色的坐标
    # 将图形中的一组坐标中四个坐标都作为相对位置的起点（0，0）
    for i in range(len(shape)):
        temp = shape[i]
        t1 = loc.r - temp[0] if loc.r - temp[0]>= 0 else (loc.r - temp[0])+10
        t2 = loc.c - temp[1] if loc.c - temp[0]>= 0 else (loc.c - temp[0])+10
        single_loc= []
        flag = True
        for j in shape:
            temp1 = t1 + j[0] if t1 + j[0]<=10 else t1 + j[0] -10-1 
            temp2 = t2 + j[1] if t2+ j[1] <=10 else t2 + j[1] -10-1 
            if temp1 < 0: temp1 += 10
            if temp2 < 0: temp2 += 10
            single_loc.append(Coord(temp1,temp2))
        # 查看生成的四个坐标是否都在Non-color中
        if single_loc:
            for z in single_loc:
                if not(z in Non_color):
                    flag = False
        if flag:
            res.append(single_loc)
    return res
        
def calculate_distance(loc1, loc2):
    distance = math.sqrt(abs(loc1.r-loc2.r) + abs(loc1.c-loc2.c))
    return distance

def calculate_fn(target, g, locs):
    h = min(calculate_distance(loc, target) for loc in locs)
    f = g + h
    return f

def update_state(board, action):
        new_board = update_board(board, action) # find the board after change the color of location of action to red
        update = find_red(new_board) # after change, find the red_list and blue_list
        new_empty_list = find_Curr_empty(update[0], update[1]) # find the location without color
        eliminated_board = eliminate_line(new_empty_list) # check if there exist row or column can be eliminated and eliminate
        update = find_red(eliminated_board) # after eliminate, find the red and blue list
        new_empty_list_1 = find_Curr_empty(update[0], update[1]) # update the empty list after eliminated
        return [eliminated_board, new_empty_list_1, update]




def update_board(board, action):
    # change color of location when we get a action
    for i in action:
        board[i] == 'r' 
    return board


def eliminate_line(empty_list, board):
    r =[]
    c =[]
    for i in range(11):
        flag_r = True
        flag_c = True
        # determine if  ith column is all empty list
        for j in range(11):
            loc = Coord(i,j)
            if not (loc in empty_list):
                flag_c = False
                break
        # determine if ith row is all in empty list
        for z in range(11):
            loc =  Coord(z,i)
            if not(loc in empty_list):
                flag_r = False
                break
        if not flag_r:
            r.append(i)
        if not flag_c:
            c.append(i)
    for i in r:
        for j in board.keys():
            if board[j].r == i:
                board[j] == None
    for i in c:
        for j in board.keys():
            if board[j].c == i:
                board[j] == None
    return board

    



    
