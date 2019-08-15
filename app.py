# coding=utf-8
import os
from math import pow

import pygame

# 页面内部padding=50
SCREEN_PADDING = 50
# 宽 = 高 = 15
SIZE = 15
# 水平方向单位距离
HORIZONTAL_GAP = 100
# 垂直方向单位距离
VERTICAL_GAP = 50
# 棋子半径
PIECE_RADIUS = 10
# 界面宽高
WIDTH = SCREEN_PADDING * 2 + (SIZE - 1) * HORIZONTAL_GAP
HEIGHT = SCREEN_PADDING * 2 + (SIZE - 1) * VERTICAL_GAP
# 初始化屏幕
pygame.init()
# 文字字体
FONT = pygame.font.Font("ext/fonts/msyh.ttf", 16)
# 加载图片文件
IMG_DICT = {}

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)


# 计算位置
def position(row, col):
    x = SCREEN_PADDING + HORIZONTAL_GAP * col
    y = SCREEN_PADDING + VERTICAL_GAP * row
    return (x, y)


# 文字绘制的位置，需要微调使居中
def font_position(row, col):
    pos = position(row, col)
    return (pos[0] - 5, pos[1] - 11)


# 棋子上图片位置
def piece_img_position(piece_pos):
    row, col = piece_pos
    x, y = position(row, col)
    return (x - 20, y - 20)


# 0        7
# 1      6   8
# 2    5   7   9
# 3  4   6   8   10
def init_pieces():
    piece_val_dict = {
        (7, 0): {'val': '0', 'role': 'b'},
        (6, 1): {'val': '9', 'role': 'b'},
        (8, 1): {'val': '8', 'role': 'b'},
        (5, 2): {'val': '5', 'role': 'b'},
        (7, 2): {'val': '6', 'role': 'b'},
        (9, 2): {'val': '7', 'role': 'b'},
        (4, 3): {'val': '4', 'role': 'b'},
        (6, 3): {'val': '3', 'role': 'b'},
        (8, 3): {'val': '2', 'role': 'b'},
        (10, 3): {'val': '1', 'role': 'b'},

        (7, 14): {'val': '0', 'role': 'y'},
        (6, 13): {'val': '9', 'role': 'y'},
        (8, 13): {'val': '8', 'role': 'y'},
        (5, 12): {'val': '5', 'role': 'y'},
        (7, 12): {'val': '6', 'role': 'y'},
        (9, 12): {'val': '7', 'role': 'y'},
        (4, 11): {'val': '4', 'role': 'y'},
        (6, 11): {'val': '3', 'role': 'y'},
        (8, 11): {'val': '2', 'role': 'y'},
        (10, 11): {'val': '1', 'role': 'y'}
    }

    result = []
    pieces_array = []
    for row in range(15):
        start = 7 - row
        if start < 0:
            start = -1 * start
        count = 8 - start
        array = [-1 for x in range(15)]
        for i in range(count):
            array[start + i * 2] = 1
        pieces_array.append(array)

    for index_row, row in enumerate(pieces_array):
        new_row = []
        for index_col, piece in enumerate(row):
            if piece == -1:
                new_row.append({'display': False})
            else:
                position = (index_row, index_col)
                if position in piece_val_dict:
                    extra = piece_val_dict[position]
                    new_row.append(
                        {'display': True, 'pos': (index_row, index_col), 'val': extra['val'], 'role': extra['role']})
                else:
                    new_row.append({'display': True, 'pos': (index_row, index_col)})
        result.append(new_row)
    return result


def init_boards():
    # 初始化棋子数组
    pieces = init_pieces()
    board_config = {
        'pieces': pieces,
        'fill': [
            {
                'pos1': position(7, 0),
                'pos2': position(4, 3),
                'pos3': position(10, 3),
                'color': (22, 160, 133)
            },
            {
                'pos1': position(7, 14),
                'pos2': position(4, 11),
                'pos3': position(10, 11),
                'color': (243, 156, 18)
            }
        ]
    }
    return board_config


def draw_line(screen, start, end, width=1, color=COLOR_BLACK):
    pygame.draw.line(screen, color, start, end, width)


def draw_circle(screen, position, radius, line_width=1, fill=COLOR_WHITE, line_fill=COLOR_BLACK):
    pygame.draw.circle(screen, fill, position, radius * 2)
    pygame.draw.circle(screen, line_fill, position, radius * 2, line_width)


def draw_piece(screen, piece_config):
    pos = piece_config['pos']
    if 'state' in piece_config and piece_config['state'] == 'pressed':
        fill = (255, 234, 167)
    else:
        fill = COLOR_WHITE

    draw_circle(screen, position(pos[0], pos[1]), 10, line_width=2, fill=fill)

    if 'val' in piece_config and piece_config['val'] is not '':
        val = piece_config['val']
        role = piece_config['role']
        text_surface = FONT.render(val, True, COLOR_BLACK)
        screen.blit(text_surface, (font_position(pos[0], pos[1])))
        img = IMG_DICT[f'{role}{val}.png']
        screen.blit(img, piece_img_position(pos))

    if 'state' in piece_config and piece_config['state'] == 'pressed':
        img = IMG_DICT[f'o1.png']
        screen.blit(img, piece_img_position(pos))


def draw_triangle(screen, pos1, pos2, pos3, fill):
    pygame.draw.polygon(screen, fill, [pos1, pos2, pos3])


# 绘制游戏界面
def draw_game_board(screen, board_config):
    # 白色填充背景色
    screen.fill(COLOR_WHITE)
    # 画棋盘
    # 两侧填充色
    fill_list = board_config['fill']
    for fill in fill_list:
        draw_triangle(screen, fill['pos1'], fill['pos2'], fill['pos3'], fill['color'])
    # 棋盘线条
    for row in range(7, 15):
        draw_line(screen, position(row, row - 7), position(row - 7, row), width=2)
    for row in range(0, 8):
        draw_line(screen, position(row, 7 - row), position(7 + row, 14 - row), width=2)
    for col in range(1, 14):
        start_row = (7 - col if col <= 7 else col - 7)
        end_row = start_row + (col if col <= 7 else 14 - col) * 2
        draw_line(screen, position(start_row, col), position(end_row, col), width=2)
    # 棋子
    pieces = board_config['pieces']
    for row in pieces:
        for piece in row:
            if not piece['display']:
                continue
            draw_piece(screen, piece)


# 点击的点是否在棋子范围内
def touch(piece, radius, clicked_pos):
    row, col = piece['pos']
    x, y = position(row, col)
    cx, cy = clicked_pos
    # 求两点直线距离的平方，radius之所以加5是为了微调范围，点击边缘可以被识别
    if pow(cx - x, 2) + pow(cy - y, 2) <= pow(radius + 5, 2):
        return True
    return False


# 获取点击的棋子
def get_clicked_piece(clicked_pos, board_config):
    all_pieces = board_config['pieces']
    for row in all_pieces:
        for piece in row:
            if not piece['display']:
                continue
            if touch(piece, 10, clicked_pos):
                piece['state'] = 'pressed'
                return piece
    return None


# 清空选中
def clear_pressed(board_config):
    all_pieces = board_config['pieces']
    for row in all_pieces:
        for piece in row:
            piece['state'] = None


# 处理鼠标点击事件
def process_mouse_click(clicked_pos, board_config):
    clear_pressed(board_config)
    clicked_piece = get_clicked_piece(clicked_pos, board_config)
    if clicked_piece is not None:
        print('点击棋子', clicked_piece)


if __name__ == '__main__':
    # 设置一个定时器，用于固定时间刷新屏幕，而不是一直不停的刷新，浪费CPU资源
    FPS = 10
    clock = pygame.time.Clock()
    # 运行标识
    running = True

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('跳棋')
    screen.fill(COLOR_WHITE)
    # 加载图片资源
    imgs = os.listdir('ext/imgs')
    for one in imgs:
        img = pygame.image.load("ext/imgs/" + one).convert_alpha()
        pygame.transform.scale(img, (20, 20))
        IMG_DICT[one] = img

    board_config = init_boards()
    while running:
        # 设置屏幕刷新频率
        clock.tick(FPS)

        # 处理不同事件
        for event in pygame.event.get():
            # 检查是否关闭窗口
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                process_mouse_click(pygame.mouse.get_pos(), board_config)

        # 绘制界面
        draw_game_board(screen, board_config)

        # 刷新屏幕
        pygame.display.flip()
