# coding=utf-8
import os
import re

import easygui
import pygame

from Model import *
from calculator import calc
from widgets import Button

pygame.init()

# 定义一些共用属性
# 尺寸
WINDOW = (1200, 670)
# 标题
TITLE = "国际数棋"
# 初始化界面与标题
SCREEN = pygame.display.set_mode(WINDOW)
pygame.display.set_caption(TITLE)

# 刷新相关
FPS = 30
CLOCK = pygame.time.Clock()

# 页面标识
PAGE_WELCOME = 0
PAGE_MODE = 1
PAGE_GAME = 2
PAGE_ABOUT = 3
# 当前页
CUR_PAGE = PAGE_WELCOME

# 游戏模式标识
GAME_MODE_STANDALONE = 0
GAME_MODE_INTERNET = 1
GAME_MODE_AI = 2
# 当前游戏模式
CUR_GAME_MODE = GAME_MODE_STANDALONE

PAGES_DATA = {
    PAGE_WELCOME: {
        "loaded": False
    },
    PAGE_MODE: {
        "loaded": False
    },
    PAGE_GAME: {
        "loaded": False
    },
    PAGE_ABOUT: {
        "loaded": False
    }
}

COLOR_WHITE = (255, 255, 255)

DEFAULT_BUTTON_SIZE = (251, 92)

########################################################################################################################
# 游戏界面需要的数据
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
# 线条宽度，默认2
LINE_WIDTH = 2
# 用到的一些颜色
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (22, 160, 133)
COLOR_YELLOW = (243, 156, 18)

# 加载字体，因为只用到了这一种，所以直接在这里加载就行了
FONT = pygame.font.Font("ext/fonts/msyh.ttf", 16)
FONT_HINT = pygame.font.Font("ext/fonts/msyh.ttf", 28)
FONT_HINT.set_bold(True)
FONT_SCORE = pygame.font.Font("ext/fonts/msyh.ttf", 20)
FONT_SCORE.set_bold(True)
# 存放图片名称与pygame img映射，image需要等pygame.display设置之后才能载入，所以这里只定义一个空dict
IMG_DICT = {}

# 弹框内容
DIALOG_TITLE = "运算方法"
DIALOG_MSG = "请输入一个合法的四则运算表达式，规则如下:\n" \
             "1.列表_REPLACE_0_中数字必须全部参与运算，且只能参与一次运算；\n" \
             "2.表达式可以使用 加 +、减 -、乘 *、除 / 和 括号 ();\n" \
             "3.运算结果必须等于_REPLACE_1_."

# 简单校验表达式，只能输入 数字、四则运算符、括号和空格
EXPRESSION_PATTERN = re.compile('[0-9()+\\-\\*/ ]+')

CHESSBOARD = None

DIALOG_FLAG = False

# 音效加载
pygame.mixer.init()
sound_select = pygame.mixer.Sound('ext/music/select.ogg')


# sound_wrong = pygame.mixer.Sound('ext/music/wrong.mp3')
# sound_jump = pygame.mixer.Sound('ext/music/jump.mp3')


# 游戏界面需要的数据
########################################################################################################################


########################################################################################################################
# 加载图片
def load_image(path, size=None):
    image = pygame.image.load(path).convert_alpha()
    if size is not None:
        image = pygame.transform.scale(image, size)
    return image


# 切换页面
def switch_page(dest):
    global CUR_PAGE
    CUR_PAGE = dest


# 绘制页面
def draw_page():
    if CUR_PAGE == PAGE_WELCOME:
        draw_page_welcome()
    elif CUR_PAGE == PAGE_MODE:
        draw_page_mode()
    elif CUR_PAGE == PAGE_GAME:
        draw_page_game()
    elif CUR_PAGE == PAGE_ABOUT:
        draw_page_about()


# 共用方法
########################################################################################################################


########################################################################################################################
# 欢迎页
# 加载欢迎页UI
def load_page_welcome_widgets():
    background = load_image('ext/images/start_background_0.png', WINDOW)
    buttons = []

    button_start = Button((int((WINDOW[0] - DEFAULT_BUTTON_SIZE[0]) / 2), 250), 'ext/images/start_white.png',
                          size=DEFAULT_BUTTON_SIZE,
                          image_hover='ext/images/start_red.png',
                          on_click=start_click, sound=sound_select)
    buttons.append(button_start)
    button_end = Button((int((WINDOW[0] - DEFAULT_BUTTON_SIZE[0]) / 2), 360), 'ext/images/end_white.png',
                        size=DEFAULT_BUTTON_SIZE,
                        image_hover='ext/images/end_red.png', on_click=end_click, sound=sound_select)
    buttons.append(button_end)
    button_author = Button((int((WINDOW[0] - DEFAULT_BUTTON_SIZE[0]) / 2), 470), 'ext/images/author_white.png',
                           size=DEFAULT_BUTTON_SIZE,
                           image_hover='ext/images/author_red.png', on_click=about_click, sound=sound_select)
    buttons.append(button_author)

    PAGES_DATA[CUR_PAGE]['widgets'] = {
        'background': background,
        'buttons': buttons
    }
    PAGES_DATA[CUR_PAGE]['loaded'] = True


# 点击开始按钮
def start_click():
    switch_page(PAGE_MODE)


# 点击结束按钮
def end_click():
    exit(0)


# 点击关于按钮
def about_click():
    switch_page(PAGE_ABOUT)
    # global DIALOG_FLAG
    # DIALOG_FLAG = True
    # easygui.msgbox('作者:\n\t张周阳 201702712004\n\t李吉言 201712712003', '关于作者')
    # DIALOG_FLAG = False


# 绘制欢迎页
def draw_page_welcome():
    # 如果页面数据还没有加载，先加载
    if not PAGES_DATA[CUR_PAGE]['loaded']:
        load_page_welcome_widgets()
    # 绘制界面
    SCREEN.fill(COLOR_WHITE)

    widgets = PAGES_DATA[CUR_PAGE]['widgets']
    background = widgets['background']
    SCREEN.blit(background, (0, 0))
    buttons = widgets['buttons']
    for button in buttons:
        SCREEN.blit(button.get_cur_image(), button.position)


# 欢迎页
######################################################################################################################

######################################################################################################################
# 关于页
def load_page_about_widgets():
    background = load_image('ext/images/about.jpg', WINDOW)
    buttons = []
    PAGES_DATA[CUR_PAGE]['widgets'] = {
        'background': background,
        'buttons': buttons
    }
    PAGES_DATA[CUR_PAGE]['loaded'] = True


def draw_page_about():
    if not PAGES_DATA[CUR_PAGE]['loaded']:
        load_page_about_widgets()
    # 绘制界面
    SCREEN.fill(COLOR_WHITE)
    widgets = PAGES_DATA[CUR_PAGE]['widgets']
    background = widgets['background']
    SCREEN.blit(background, (0, 0))


# 关于页
######################################################################################################################

######################################################################################################################
# 模式选择页
# 加载模式选择页UI
def load_page_mode_widgets():
    background = load_image('ext/images/start_background_0.png', WINDOW)
    buttons = []

    button_start = Button((int((WINDOW[0] - DEFAULT_BUTTON_SIZE[0]) / 2), 250), 'ext/images/standalone_white.png',
                          size=DEFAULT_BUTTON_SIZE,
                          image_hover='ext/images/standalone_red.png',
                          on_click=standalone_click, sound=sound_select)
    buttons.append(button_start)
    button_end = Button((int((WINDOW[0] - DEFAULT_BUTTON_SIZE[0]) / 2), 360), 'ext/images/Internet_white.png',
                        size=DEFAULT_BUTTON_SIZE,
                        image_hover='ext/images/Internet_red.png', on_click=internet_click, sound=sound_select)
    buttons.append(button_end)
    button_author = Button((int((WINDOW[0] - DEFAULT_BUTTON_SIZE[0]) / 2), 470), 'ext/images/ai_white.png',
                           size=DEFAULT_BUTTON_SIZE,
                           image_hover='ext/images/ai_red.png', on_click=ai_click, sound=sound_select)
    buttons.append(button_author)

    PAGES_DATA[CUR_PAGE]['widgets'] = {
        'background': background,
        'buttons': buttons
    }
    PAGES_DATA[CUR_PAGE]['loaded'] = True


# 点击单机模式
def standalone_click():
    switch_page(PAGE_GAME)
    global CUR_GAME_MODE
    CUR_GAME_MODE = GAME_MODE_STANDALONE


# 点击网络模式
def internet_click():
    global DIALOG_FLAG
    DIALOG_FLAG = True
    easygui.msgbox('暂不支持 网络模式', '提示')
    DIALOG_FLAG = False
    # switch_page(PAGE_GAME)
    # global CUR_GAME_MODE
    # CUR_GAME_MODE = GAME_MODE_INTERNET


# 点击ai模式
def ai_click():
    global DIALOG_FLAG
    DIALOG_FLAG = True
    easygui.msgbox('暂不支持 智能模式', '提示')
    DIALOG_FLAG = False
    # switch_page(PAGE_GAME)
    # global CUR_GAME_MODE
    # CUR_GAME_MODE = GAME_MODE_AI


def draw_page_mode():
    # 如果页面数据还没有加载，先加载
    if not PAGES_DATA[CUR_PAGE]['loaded']:
        load_page_mode_widgets()
    # 绘制界面
    SCREEN.fill(COLOR_WHITE)

    widgets = PAGES_DATA[CUR_PAGE]['widgets']
    background = widgets['background']
    SCREEN.blit(background, (0, 0))
    buttons = widgets['buttons']
    for button in buttons:
        SCREEN.blit(button.get_cur_image(), button.position)


# 模式选择页
######################################################################################################################

######################################################################################################################
# 游戏页

# 加载用到的图片资源
def load_imgs():
    # 已经加载过了
    if len(IMG_DICT) > 0:
        return
    image_files = os.listdir('ext/images/chessman')
    for image_file in image_files:
        image = pygame.image.load("ext/images/chessman/" + image_file).convert_alpha()
        # 缩放到20*20大小
        # image = pygame.transform.scale(image, (20, 20))
        IMG_DICT[image_file.split("/")[-1].split('.')[0]] = image


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


# valid_nums 可以使用的数字列表
# expression 用户输入的表达式
def check_expression(valid_nums, expression):
    # 不满足表达式格式
    if not EXPRESSION_PATTERN.fullmatch(expression):
        return False
    # 去掉操作符号与括号，只留数字
    new_expression = expression.replace('+', ' ').replace('-', ' ') \
        .replace('*', ' ').replace('/', ' ').replace('(', ' ').replace(')', ' ')
    # 去除空格，只保留数字
    new_num_list = list(map(lambda x: int(x), filter(lambda x: x != '', new_expression.split(' '))))
    new_num_list.sort()
    valid_nums.sort()
    return valid_nums.__eq__(new_num_list)


def show_calc_dialog(dest_val, components, error_msg=None):
    global DIALOG_FLAG
    DIALOG_FLAG = True
    # 用户输入的表达式
    message = DIALOG_MSG.replace('_REPLACE_0_', str(components)).replace('_REPLACE_1_', str(dest_val))
    if error_msg:
        message += '\n' + error_msg
    expression = easygui.enterbox(message, DIALOG_TITLE)
    DIALOG_FLAG = False
    # 用户没输入，点了取消
    if expression is None:
        CHESSBOARD.CURRENT_SELECTED_CHESSMAN = None
    # 用户输入了，进行计算
    else:
        expression_valid = check_expression(components, expression)
        if not expression_valid:
            show_calc_dialog(dest_val, components, '表达式有误，请重新输入')
        else:
            result = calc(expression)
            # 输入的表达式格式
            if result is None:
                show_calc_dialog(dest_val, components, '表达式有误，请重新输入')
            # 输入的表达式计算出来的结果不为0
            elif result != dest_val:
                show_calc_dialog(dest_val, components, '结果不正确，请重新输入')
            # 正确，跳特么的
            else:
                sound_select.play()
                CHESSBOARD.jump()


# 处理点击事件
# clicked_position - 点击的位置(x,y)
def process_click(clicked_position):
    click_result = None
    # 遍历棋子
    for chessman in CHESSBOARD.get_selectable_chessman_list():
        if touched(chessman.get_row_col(), clicked_position):
            sound_select.play()
            click_result = CHESSBOARD.click_chessman(chessman)
    if click_result is not None:
        from_chessman = click_result[0]
        to_chessman = click_result[1]
        # 四则运算哟啊求出的值
        dest_val = from_chessman.val
        # 参与计算的项
        components = click_result[2]
        print(from_chessman, to_chessman, components)
        show_calc_dialog(dest_val, components)


# 绘制老家，是一个填充颜色的三角形
def draw_homes(homes):
    for home in homes:
        points = home['points']
        color = home['color']
        positions = [calc_position(point) for point in points]
        pygame.draw.polygon(SCREEN, color, positions)


# 绘制棋盘线条
def draw_lines(lines):
    for line in lines:
        pygame.draw.line(SCREEN, COLOR_BLACK, calc_position(line[0]), calc_position(line[1]), LINE_WIDTH)


# 绘制圆圈
def draw_circle(position, radius, line_width=1, fill=COLOR_WHITE, line_fill=COLOR_BLACK):
    pygame.draw.circle(SCREEN, fill, position, radius * 2)
    pygame.draw.circle(SCREEN, line_fill, position, radius * 2, line_width)


# 绘制文字
def draw_text(row_col, text):
    text_surface = FONT.render(text, True, COLOR_BLACK)
    SCREEN.blit(text_surface, (calc_text_position(row_col)))


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
    SCREEN.blit(image, position)


def draw_image(row_col, image):
    position = calc_chessman_position(row_col)
    image = IMG_DICT[image]
    SCREEN.blit(image, position)


# 绘制一组
def draw_chessman_list(chessman_list):
    for chessman in chessman_list:
        draw_chessman(chessman)
        if CHESSBOARD.SELECTED_CHESSMAN and chessman.get_row_col() == CHESSBOARD.SELECTED_CHESSMAN.get_row_col():
            draw_image(chessman.get_row_col(), 'o0')


# 绘制棋盘
def draw_game_board():
    widgets = PAGES_DATA[CUR_PAGE]['widgets']
    background = widgets['background']
    SCREEN.blit(background, (0, 0))
    # 最底层，绘制两边的老家-两个三角
    draw_homes(CHESSBOARD.homes)
    # 倒数第二层-绘制棋盘最底层的线条
    draw_lines(CHESSBOARD.board_lines)
    # 绘制界面提示文字
    draw_hints()
    # 倒数第三层-绘制棋盘上可以摆棋子的位置-圆圈
    draw_map(CHESSBOARD.game_map)
    # 最上层，绘制按钮
    # 绘制蓝方棋子
    draw_chessman_list(CHESSBOARD.get_chessman_list(CHESSBOARD.PLAYER_BLUE))
    # 绘制红方棋子
    draw_chessman_list(CHESSBOARD.get_chessman_list(CHESSBOARD.PLAYER_RED))
    # 绘制叫停按钮
    buttons = widgets['buttons']
    CHESSBOARD.BLUE_STOP = True
    CHESSBOARD.RED_STOP = True
    # 可以叫停，且当前用户操作，才展示叫停按钮
    if CHESSBOARD.BLUE_STOP and CHESSBOARD.CUR_PLAYER == CHESSBOARD.PLAYER_BLUE:
        SCREEN.blit(buttons[0].get_cur_image(), buttons[0].position)
    if CHESSBOARD.RED_STOP and CHESSBOARD.CUR_PLAYER == CHESSBOARD.PLAYER_RED:
        SCREEN.blit(buttons[1].get_cur_image(), buttons[1].position)


# 绘制界面提示文字
def draw_hints():
    # 执子提示
    player = '蓝方执子' if CHESSBOARD.CUR_PLAYER == CHESSBOARD.PLAYER_BLUE else '黄方执子'
    color = COLOR_BLUE if CHESSBOARD.CUR_PLAYER == CHESSBOARD.PLAYER_BLUE else COLOR_YELLOW
    text_surface = FONT_HINT.render(player, True, color)
    # 分数提示
    scores = CHESSBOARD.scores()
    SCREEN.blit(text_surface, (WINDOW[0] / 2 - 58, WINDOW[1] / 2 - 33))

    text_surface = FONT_SCORE.render(f'蓝方得分: {scores[CHESSBOARD.PLAYER_BLUE]}', True, COLOR_BLUE)
    SCREEN.blit(text_surface, (WINDOW[0] / 2 - 60, WINDOW[1] - 55))
    text_surface = FONT_SCORE.render(f'黄方得分: {scores[CHESSBOARD.PLAYER_RED]}', True, COLOR_YELLOW)
    SCREEN.blit(text_surface, (WINDOW[0] / 2 - 60, WINDOW[1] - 35))


def load_page_game_widgets():
    load_imgs()
    # 初始化棋盘
    global CHESSBOARD
    CHESSBOARD = ChessBoard()

    background = load_image('ext/images/start_background_1.jpg', WINDOW)
    buttons = []
    button_stop_blue = Button((20, 20), 'ext/images/pause_white.png',
                              size=(int(DEFAULT_BUTTON_SIZE[0] / 2), int(DEFAULT_BUTTON_SIZE[1] / 2)),
                              image_hover='ext/images/pause_red.png',
                              on_click=stop_blue_click)
    buttons.append(button_stop_blue)
    button_stop_yellow = Button((WINDOW[0] - 170, 20), 'ext/images/pause_white.png',
                                size=(int(DEFAULT_BUTTON_SIZE[0] / 2), int(DEFAULT_BUTTON_SIZE[1] / 2)),
                                image_hover='ext/images/pause_red.png',
                                on_click=stop_yellow_click)
    buttons.append(button_stop_yellow)

    PAGES_DATA[CUR_PAGE]['widgets'] = {
        'background': background,
        'buttons': buttons
    }
    PAGES_DATA[CUR_PAGE]['loaded'] = True


def stop_blue_click():
    scores = CHESSBOARD.scores()
    score_blue = scores[CHESSBOARD.PLAYER_BLUE]
    score_yellow = scores[CHESSBOARD.PLAYER_RED]
    winner = '恭喜蓝方获得胜利' if score_blue > score_yellow else '恭喜黄方获得胜利' if score_yellow > score_blue else '本局和棋'
    global DIALOG_FLAG
    DIALOG_FLAG = True
    easygui.msgbox(f'蓝方得分:{score_blue}\n黄方得分:{score_yellow}\n{winner}', '游戏结束')
    DIALOG_FLAG = False
    del PAGES_DATA[CUR_PAGE]
    PAGES_DATA[CUR_PAGE] = {'loaded': False}
    switch_page(PAGE_WELCOME)


def stop_yellow_click():
    scores = CHESSBOARD.scores()
    score_blue = scores[CHESSBOARD.PLAYER_BLUE]
    score_yellow = scores[CHESSBOARD.PLAYER_RED]
    winner = '恭喜蓝方获得胜利' if score_blue > score_yellow else '恭喜黄方获得胜利' if score_yellow > score_blue else '本局和棋'
    global DIALOG_FLAG
    DIALOG_FLAG = True
    easygui.msgbox(f'蓝方得分:{score_blue}\n黄方得分:{score_yellow}\n{winner}', '游戏结束')
    DIALOG_FLAG = False
    del PAGES_DATA[CUR_PAGE]
    PAGES_DATA[CUR_PAGE] = {'loaded': False}
    switch_page(PAGE_WELCOME)


def draw_page_game():
    # 如果页面数据还没有加载，先加载
    if not PAGES_DATA[CUR_PAGE]['loaded']:
        load_page_game_widgets()
    draw_game_board()


# 游戏页
######################################################################################################################

# 分发点击事件
def dispatcher_click(event, position):
    if (CUR_PAGE == PAGE_WELCOME or CUR_PAGE == PAGE_MODE) and PAGES_DATA[CUR_PAGE]['loaded']:
        buttons = PAGES_DATA[CUR_PAGE]['widgets']['buttons']
        for button in buttons:
            button.dispatcher_mouse_event(event, position)
    elif CUR_PAGE == PAGE_GAME:
        buttons = PAGES_DATA[CUR_PAGE]['widgets']['buttons']
        if CHESSBOARD.BLUE_STOP and CHESSBOARD.CUR_PLAYER == CHESSBOARD.PLAYER_BLUE:
            buttons[0].dispatcher_mouse_event(event, position)
        if CHESSBOARD.RED_STOP and CHESSBOARD.CUR_PLAYER == CHESSBOARD.PLAYER_RED:
            buttons[1].dispatcher_mouse_event(event, position)
        process_click(position)
    elif CUR_PAGE == PAGE_ABOUT:
        switch_page(PAGE_WELCOME)


# 分发移动事件
def dispatcher_move(event, position):
    if PAGES_DATA[CUR_PAGE]['loaded']:
        buttons = PAGES_DATA[CUR_PAGE]['widgets']['buttons']
        for button in buttons:
            button.dispatcher_mouse_event(event, position)


if __name__ == '__main__':
    # 加载背景音乐
    pygame.mixer.music.load('ext/music/bgm.mp3')
    # 播放
    pygame.mixer.music.play(-1, 0.0)
    while True:
        CLOCK.tick(FPS)
        # 处理事件
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            # 检查是否关闭窗口
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                dispatcher_click(event, mouse_pos)
            elif event.type == pygame.MOUSEMOTION:
                dispatcher_move(event, mouse_pos)

        if DIALOG_FLAG:
            continue

        draw_page()
        pygame.display.flip()
