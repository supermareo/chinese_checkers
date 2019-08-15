# coding=utf-8
from math import pow


# 棋子类
class Chessman:
    # 红方
    PLAYER_RED = -1
    # 蓝方
    PLAYER_BLUE = 1

    def __init__(self, row, col, val, role):
        # 所在行
        self.row = row
        # 所在列
        self.col = col
        # 值
        self.val = val
        # 所属角色-属于哪个玩家-红-1/蓝1/轮空0
        self.role = role
        # 根据所属玩家和值，计算出显示的图片
        self.image = f'{"b" if role == self.PLAYER_BLUE else "y"}{val}'

    def get_row_col(self):
        return self.row, self.col

    def __str__(self):
        return f'({self.row},{self.col}) - {self.val} - {self.role}'


# 棋盘类
class ChessBoard:
    # 红方
    PLAYER_RED = -1
    # 蓝方
    PLAYER_BLUE = 1
    # 空闲
    EMPTY = 0

    # 当前玩家-初始为蓝方
    CUR_PLAYER = PLAYER_BLUE
    # 已选中的棋子-初始无选中
    SELECTED_CHESSMAN = None
    # 当前选中的棋子-初始无选中
    CURRENT_SELECTED_CHESSMAN = None

    def __init__(self):
        # 初始化棋盘
        self.__init_game_map__()
        # 初始化棋子
        self.__init_chessman__()

    # 初始化棋子
    def __init_chessman__(self):
        self.chessman_list = []
        for row_index, row in enumerate(self.game_map):
            for col_index, item in enumerate(row):
                if item is not None:
                    if item == -1:
                        # 值为-1的轮空
                        self.chessman_list.append(Chessman(row_index, col_index, item, self.EMPTY))
                    else:
                        if col_index > 7:
                            # 右侧红方
                            self.chessman_list.append(Chessman(row_index, col_index, item, self.PLAYER_RED))
                        else:
                            # 左侧蓝方
                            self.chessman_list.append(Chessman(row_index, col_index, item, self.PLAYER_BLUE))

    # 初始化游戏地图
    def __init_game_map__(self):
        # 几个分数点
        self.pos_val_dict = {
            (7, 0): 0,
            (6, 1): 9,
            (8, 1): 8,
            (5, 2): 5,
            (7, 2): 6,
            (9, 2): 7,
            (4, 3): 4,
            (6, 3): 3,
            (8, 3): 2,
            (10, 3): 1,

            (7, 14): 0,
            (6, 13): 9,
            (8, 13): 8,
            (5, 12): 5,
            (7, 12): 6,
            (9, 12): 7,
            (4, 11): 4,
            (6, 11): 3,
            (8, 11): 2,
            (10, 11): 1
        }
        self.game_map = []
        for row_index in range(15):
            start = 7 - row_index
            if start < 0:
                start = -1 * start
            count = 8 - start
            row = [None for _ in range(15)]
            for i in range(count):
                col_index = start + i * 2
                row[col_index] = -1 if (row_index, col_index) not in self.pos_val_dict else self.pos_val_dict[
                    (row_index, col_index)]
            self.game_map.append(row)
        # 线条也初始化一下
        self.__init_lines__()
        self.__init_homes_()

    # 初始化棋盘线条
    def __init_lines__(self):
        self.board_lines = []
        for row in range(0, 15):
            if 0 <= row < 8:
                self.board_lines.append(((row, 7 - row), (7 + row, 14 - row)))
            if 7 <= row < 15:
                self.board_lines.append(((row, row - 7), (row - 7, row)))
        for col in range(1, 14):
            start_row = (7 - col if col <= 7 else col - 7)
            end_row = start_row + (col if col <= 7 else 14 - col) * 2
            self.board_lines.append(((start_row, col), (end_row, col)))

    # 初始化红蓝两方的家-填充颜色的三角形
    def __init_homes_(self):
        self.homes = []
        # 蓝方
        self.homes.append({'points': [(7, 0), (4, 3), (10, 3)], 'color': (22, 160, 133)})
        # 红方
        self.homes.append({'points': [(7, 14), (4, 11), (10, 11)], 'color': (243, 156, 18)})

    # 获取棋子列表，如果没有指定role，返回所有
    def get_chessman_list(self, role=None):
        return list(filter(lambda x: x if role is None else x.role == role, self.chessman_list))

    # 可到达的方向
    @staticmethod
    def reachable_direction(from_pos, to_pos):
        row1, col1 = from_pos
        row2, col2 = to_pos
        # 上下左右
        if col1 == col2 or row1 == row2:
            return False
        # 右上|右下|左下|左上
        if pow(row1 - row2, 2) == pow(col1 - col2, 2):
            return True
        return False

    # 获取可选的棋子
    def get_selectable_chessman_list(self):
        # 如果是第一个，必须得选自己的棋子
        if self.SELECTED_CHESSMAN is None:
            return self.get_chessman_list(self.CUR_PLAYER)
        # 第二个，则必须选择空白的位置
        empty_chessman_list = self.get_chessman_list(self.EMPTY)
        # 而且，必须在选中的棋子的 上|右上|右|右下|下|左下|左|左上 方向之一
        return list(
            filter(lambda x: self.reachable_direction(self.SELECTED_CHESSMAN.get_row_col(), x.get_row_col()),
                   empty_chessman_list))

    # 点击了棋子
    def click_chessman(self, chessman):
        # 首次选中，则给SELECTED_CHESSMAN赋值
        if self.SELECTED_CHESSMAN is None:
            self.SELECTED_CHESSMAN = chessman
        else:
            self.CURRENT_SELECTED_CHESSMAN = chessman
            # 判断这个位置是否能直接跳过来，如果能，将SELECTED_CHESSMAN跳到该位置
            # # 值
            # self.val = val
            # # 所属角色-属于哪个玩家-红-1/蓝1/轮空0
            # self.role = role
            # # 根据所属玩家和值，计算出显示的图片
            # self.image = f'{"b" if role == self.PLAYER_BLUE else "y"}{val}'
            new_chessman_list = []
            for chessman in self.get_chessman_list():
                row, col = chessman.get_row_col()
                if (row, col) == self.SELECTED_CHESSMAN.get_row_col():
                    new_chessman_list.append(Chessman(row, col, -1, self.EMPTY))
                elif (row, col) == self.CURRENT_SELECTED_CHESSMAN.get_row_col():
                    new_chessman_list.append(
                        Chessman(row, col, self.SELECTED_CHESSMAN.val, self.CUR_PLAYER))
                else:
                    new_chessman_list.append(chessman)
            self.chessman_list.clear()
            for chessman in new_chessman_list:
                self.chessman_list.append(chessman)

            # 清空选中
            self.SELECTED_CHESSMAN = None
            self.CURRENT_SELECTED_CHESSMAN = None
            # 切换玩家
            self.CUR_PLAYER = self.PLAYER_RED if self.CUR_PLAYER == self.PLAYER_BLUE else self.PLAYER_BLUE
