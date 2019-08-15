# coding=utf-8
import pygame
import os
from Model import *

# 页面内部padding=40
SCREEN_PADDING = 40
# 宽 = 高 = 15
SIZE = 15
# 水平方向单位距离
HORIZONTAL_GAP = 80
# 垂直方向单位距离
VERTICAL_GAP = 40
# 棋子半径
CHESSMAN_RADIUS = 10
# 界面宽高，高度预留30用于文字绘制
WIDTH = SCREEN_PADDING * 2 + (SIZE - 1) * HORIZONTAL_GAP
HEIGHT = SCREEN_PADDING * 2 + (SIZE - 1) * VERTICAL_GAP + 30
# 线条宽度，默认2
LINE_WIDTH = 2
# 用到的一些颜色
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (22, 160, 133)
COLOR_YELLOW = (243, 156, 18)
# 初始化pygame
pygame.init()
# 加载字体，因为只用到了这一种，所以直接在这里加载就行了
FONT = pygame.font.Font("ext/fonts/msyh.ttf", 16)
# 存放图片名称与pygame img映射，image需要等pygame.display设置之后才能载入，所以这里只定义一个空dict
IMG_DICT = {}

screen = None
CHESSBOARD = None


# 加载用到的图片资源
def load_imgs():
    image_files = os.listdir('ext/imgs')
    for image_file in image_files:
        image = pygame.image.load("ext/imgs/" + image_file).convert_alpha()
        # 缩放到20*20大小
        pygame.transform.scale(image, (20, 20))
        IMG_DICT[image_file.split('.')[0]] = image


# 计算行列点在界面上的实际绘制位置
def calc_position(row_col):
    row, col = row_col
    x = SCREEN_PADDING + HORIZONTAL_GAP * col
    y = SCREEN_PADDING + VERTICAL_GAP * row
    return x, y


# 计算行列文字在界面上的实际绘制位置
def calc_text_position(row_col):
    position = calc_position(row_col)
    return position[0] - 5, position[1] - 11


# 计算行列棋子在界面上的实际绘制位置
def calc_chessman_position(row_col):
    position = calc_position(row_col)
    return position[0] - 20, position[1] - 20


# 点击的点是否在棋子内部，即点击棋子
def touched(chessman_row_col, clicked_position):
    chess_center = calc_position(chessman_row_col)
    x, y = chess_center
    cx, cy = clicked_position
    # 求两点直线距离的平方，radius之所以加5是为了微调范围，点击边缘可以被识别
    return pow(cx - x, 2) + pow(cy - y, 2) <= pow(CHESSMAN_RADIUS + 5, 2)


# 处理点击事件
# clicked_position - 点击的位置(x,y)
def process_click(clicked_position):
    # 遍历棋子
    for chessman in CHESSBOARD.get_selectable_chessman_list():
        print(chessman)
        if touched(chessman.get_row_col(), clicked_position):
            CHESSBOARD.click_chessman(chessman)
            break


# 绘制老家，是一个填充颜色的三角形
def draw_homes(homes):
    for home in homes:
        points = home['points']
        color = home['color']
        positions = [calc_position(point) for point in points]
        pygame.draw.polygon(screen, color, positions)


# 绘制棋盘线条
def draw_lines(lines):
    for line in lines:
        pygame.draw.line(screen, COLOR_BLACK, calc_position(line[0]), calc_position(line[1]), LINE_WIDTH)


# 绘制圆圈
def draw_circle(position, radius, line_width=1, fill=COLOR_WHITE, line_fill=COLOR_BLACK):
    pygame.draw.circle(screen, fill, position, radius * 2)
    pygame.draw.circle(screen, line_fill, position, radius * 2, line_width)


# 绘制文字
def draw_text(row_col, text):
    text_surface = FONT.render(text, True, COLOR_BLACK)
    screen.blit(text_surface, (calc_text_position(row_col)))


# 绘制棋盘上可以摆棋子的位置
def draw_map(game_map):
    for row_index, row in enumerate(game_map):
        for col_index, val in enumerate(row):
            if val is None:
                continue
            row_col = (row_index, col_index)
            position = calc_position(row_col)
            draw_circle(position, CHESSMAN_RADIUS)
            # 如果值不是-1，则还要再绘制一下文字
            if val is not -1:
                draw_text(row_col, str(val))


# 绘制一颗棋子
def draw_chessman(chessman):
    row_col = chessman.get_row_col()
    position = calc_chessman_position(row_col)
    image = IMG_DICT[chessman.image]
    screen.blit(image, position)


def draw_image(row_col, image):
    position = calc_chessman_position(row_col)
    image = IMG_DICT[image]
    screen.blit(image, position)


# 绘制一组
def draw_chessman_list(chessman_list):
    for chessman in chessman_list:
        draw_chessman(chessman)
        if CHESSBOARD.SELECTED_CHESSMAN and chessman.get_row_col() == CHESSBOARD.SELECTED_CHESSMAN.get_row_col():
            draw_image(chessman.get_row_col(), 'o0')


# 绘制棋盘
def draw_game_board():
    screen.fill(COLOR_WHITE)
    # 最底层，绘制两边的老家-两个三角
    draw_homes(CHESSBOARD.homes)
    # 倒数第二层-绘制棋盘最底层的线条
    draw_lines(CHESSBOARD.board_lines)
    # 倒数第三层-绘制棋盘上可以摆棋子的位置-圆圈
    draw_map(CHESSBOARD.game_map)
    # 最上层，绘制按钮
    # 绘制蓝方棋子
    draw_chessman_list(CHESSBOARD.get_chessman_list(CHESSBOARD.PLAYER_BLUE))
    # 绘制红方棋子
    draw_chessman_list(CHESSBOARD.get_chessman_list(CHESSBOARD.PLAYER_RED))


if __name__ == '__main__':
    # 页面绘制的fps设置，防止绘制过频繁性能下降
    fps = 10
    clock = pygame.time.Clock()
    # 运行中的标识，设置为false后游戏停止
    running_flag = True

    # 设置屏幕尺寸
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # 设置标题
    pygame.display.set_caption('国际数棋')
    # 背景填充
    screen.fill(COLOR_WHITE)
    # 加载图片资源
    load_imgs()

    # 初始化棋盘
    CHESSBOARD = ChessBoard()

    while running_flag:
        # 限制绘制频率
        clock.tick(fps)
        # 处理事件
        for event in pygame.event.get():
            # 检查是否关闭窗口
            if event.type == pygame.QUIT:
                running_flag = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                process_click(pygame.mouse.get_pos())

        draw_game_board()

        # 刷新屏幕
        pygame.display.flip()
