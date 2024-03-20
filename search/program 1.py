# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress

from .core import PlayerColor, Coord, PlaceAction
from .utils import render_board


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
    num_red = 0 #红色的数量
    Curr_Empty = [] #目前没颜色的坐标
    blue_Loc = [] # 蓝色的坐标
    
    #loop 找红蓝坐标
    for i in board.keys():
        if (board[i]== PlayerColor.RED):
            red_Loc.append(i)
            num_red +=1
        elif (board[i] == PlayerColor.BLUE):
           blue_Loc.append(i)
    
    # 找到了所有颜色为空的坐标
    Curr_Empty = find_Curr_empty(red_Loc, blue_Loc)
    
    #找到了红色坐标周围可以连接图形的坐标
    connect=[]
    for i in red_Loc:
        connect.extend(check_around_2(i, Curr_Empty))
    print(connect)
    
    # 遍历可以连接图形的坐标， 找到当前所有可以进行的action
    for i in connect:
        res = []
        res = relative_shape(i, Curr_Empty)
        print(res)
        
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
    up = Coord(i.r - 1, i.c) if i.r-1 >= 0 else Coord(10-1, i.c)
    left = Coord(i.r, i.c - 1)
    right = Coord(i.r, i.c + 1)
    down = Coord(i.r + 1, i.c) if i.r+1 <= 10 else Coord(0+1,i.c)
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
    'Z': [[(0, 0), (0, 1), (-1, 1), (-1, 2)], [(0, 0), (1, 0), (1, 1), (2, 1)]],
    'S': [[(0, 0), (0, 1), (-1, 1), (-1, 2)], [(0, 0), (1, 0), (1, 1), (2, 1)]]
}

#对于每个图形的相对位置， 进行检测
def relative_shape(coord,Non_color):
    res = []
    for shapes in tetromino_shape.values():
        # shape 是[(),(),(),()]一组图形的坐标
        for shape in shapes:
            list = return_shape(shape, coord, Non_color)
            if len(list) != 0:
                res.append(list)
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
        
            
    
