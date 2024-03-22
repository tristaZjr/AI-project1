# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress

from .core import PlayerColor, Coord, PlaceAction
from .utils import render_board

import math

import heapq

class Action:
    def __init__(self, Parent, numF, locs, numG, numH, H2):
        self.Parent = Parent
        self.numF = numF
        self.locs = locs
        self.numG = numG
        self.numH = numH
        self.H2 = H2
    def __lt__(self, other):
        return (self.numH + self.H2) < (other.numH + other.H2)



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
    num_of_search = 1 # G
    
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
    OpenAction = []
    for i in connect:
        res = relative_shape(i, Curr_Empty)
        # 遍历当下结果， 将i作为parent， 记录在内， num_of_search 初始值为1
        for j in res:
            action = creat_Action([i],j, target, num_of_search, Curr_Empty)
            heapq.heappush(OpenAction, action)
      
    # 查看priority heap中的f值
    closeList = []
    while OpenAction:
       print(heapq.heappop(OpenAction).numF)
    
    
    flag = False
    while OpenAction:
        currentNode = heapq.heappop(OpenAction)
        heapq.heappush(closeList, currentNode)
        num_of_search +=1

        for i in currentNode.locs:
           if i == target:
                flag == True
                break
        if flag:
           break
        
        #什么时候更新board， 是否需要重新赋值， 尚且不明
        (board, Curr_Empty, update) = update_state(board, currentNode)

        # 已在函数内部构件好，action，此时的children是[Action]
        children = get_valid_action(update[0], Curr_Empty, target, num_of_search, currentNode)
        for child in children:
            if child in closeList:
                continue  
            if child in OpenAction:
                if child.numG > num_of_search:
                    continue
            else :
                heapq.heappush(OpenAction, action)  
    
    
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

# 创建Action对象
def creat_Action(parent, loc, target, num_of_search, empty_list):
    current_H = calculate_H(target, loc) ## 距离row/ column最短的地方, 返回值是[sign， 距离row或者column最短距离]
    print(current_H)
    H1 = current_H[1] #距离row或者col最短的距离
    H2 = calculate_H2(empty_list,target, current_H[0]) # 用sign去判断是算row所占格子的数量还是column所占格子
    current_fn = calculate_F(num_of_search, H1, H2) # num_of_search: G
    action = Action(parent, current_fn, loc, num_of_search, H1, H2)
    return action


# 计算target行或者列没有颜色的数量
def calculate_H2(empty_list, target, row_or_column):
    row = target.r 
    column = target.c
    num_c =0 
    num_r = 0
    # 通过遍历empty——list里面的坐标， 找到emptylist中target行或者列的坐标
    for i in empty_list:
        if i.c == column:
            num_c +=1
        if i.r == row:
            num_r +=1
    if row_or_column > 0: # 选择行中空白的还是列中空白的， 同过计算H1的值
        return num_r
    if row_or_column < 0:
        return num_c
    # 如果说到row和column的距离一样， 选择待填数量小的
    return min(num_c, num_r)
     

    
# 得到所有可用的action， 用于搜索算法的循环中
def get_valid_action(red_Loc, Curr_Empty, target, num_of_search, parent):
    connect=[]
    for i in red_Loc:
        temp = check_around_2(i, Curr_Empty)
        connect.extend(temp)
    valid_action = []
    for i in connect:
        res = relative_shape(i, Curr_Empty)
        for j in res:
           action = creat_Action(parent,j,target, num_of_search, Curr_Empty)
           valid_action.append(action)
    # 返回一个action的list
    return valid_action
    

# 从一个board 中找到所有的red

def find_red(board):
    red_Loc = []
    blue_Loc = []
    for i in board.keys():
        if (board[i]== PlayerColor.RED):
            red_Loc.append(i)
        elif (board[i] == PlayerColor.BLUE):
           blue_Loc.append(i)
    return [red_Loc,blue_Loc]

# 从一个board 中找到所有的empty值

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

# 找到红色周围所有的没颜色的值
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



# 计算H， 用每一组坐标中跟row 或者column最近的坐标计算距离
def calculate_H(target, locs):
    print(locs)
    row  = min(abs(loc.r-target.r) for loc in locs)
    col = min(abs(loc.c - target.c) for loc in locs)
    # 如果说row比col的距离少， 返回正数， 加上value
    if row < col:
        return [1,row]
    # 离col的距离少，返回负数作为sign， 后跟value
    elif col > row:
        return [-1,col]
    # 俩者一样， 返回0， 给一个value就行
    else:
        return [0, col]
    

# 计算F的值， F=H1 + H2
def calculate_F(G, H1, H2):
    f = H1 + H2
    return f

#更新现有的board， 未测试版（不知道有无bug）
def update_state(board, action):
        new_board = update_board(board, action) # find the board after change the color of location of action to red
        update = find_red(new_board) # after change, find the red_list and blue_list
        new_empty_list = find_Curr_empty(update[0], update[1]) # find the location without color

        # 检查是否有行或者列需要被消除
        eliminated_board = eliminate_line(new_empty_list) # check if there exist row or column can be eliminated and eliminate
        update = find_red(eliminated_board) # after eliminate, find the red and blue list
        new_empty_list_1 = find_Curr_empty(update[0], update[1]) # update the empty list after eliminated
        return (eliminated_board, new_empty_list_1, update)


def update_board(board, action):
    # change color of location when we get a action
    for i in action:
        board[i] == 'r' 
    return board

# 用empty_list检查是否有一行/列全都不在empty_list中， 如果有，消掉
def eliminate_line(empty_list, board):
    r =[]
    c =[]
    # 10行/列， 一行一行查
    for i in range(11):
        flag_r = True
        flag_c = True
        # determine if ith column is all empty list
        # 如果在empty_list里面找到了一列中任何一个坐标， flag为false， 说明该行/列未填满
        for j in range(11):
            loc = Coord(i,j)
            if loc in empty_list:
                flag_c = False
                break
        # determine if ith row is all in empty list
        for z in range(11):
            loc =  Coord(z,i)
            if loc in empty_list:
                flag_r = False
                break
        # 如果flag循环过后， flag依旧为True， 说明一行/列都有颜色， 可以被消除
        if flag_r:
            r.append(i)
        if flag_c:
            c.append(i)
    # 更改board的颜色
    if r:
        for i in r:
            for j in board.keys():
                if board[j].r == i:
                    board[j] == None
    if c:
        for i in c:
            for j in board.keys():
                if board[j].c == i:
                    board[j] == None
    return board

    



    
