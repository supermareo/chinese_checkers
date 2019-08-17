# coding=utf-8
import easygui
import pygame

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
# PAGE_ABOUT = 3
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
    }
}

COLOR_WHITE = (255, 255, 255)

DEFAULT_BUTTON_SIZE = (251, 92)


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


# 共用方法
########################################################################################################################


########################################################################################################################
# 加载欢迎页UI
def load_page_welcome_widgets():
    background = load_image('ext/images/start_background_0.png', WINDOW)
    buttons = []

    button_start = Button((int((WINDOW[0] - DEFAULT_BUTTON_SIZE[0]) / 2), 250), 'ext/images/start_white.png',
                          size=DEFAULT_BUTTON_SIZE,
                          image_hover='ext/images/start_red.png',
                          on_click=start_click)
    buttons.append(button_start)
    button_end = Button((int((WINDOW[0] - DEFAULT_BUTTON_SIZE[0]) / 2), 360), 'ext/images/end_white.png',
                        size=DEFAULT_BUTTON_SIZE,
                        image_hover='ext/images/end_red.png', on_click=end_click)
    buttons.append(button_end)
    button_author = Button((int((WINDOW[0] - DEFAULT_BUTTON_SIZE[0]) / 2), 470), 'ext/images/author_white.png',
                           size=DEFAULT_BUTTON_SIZE,
                           image_hover='ext/images/author_red.png', on_click=about_click)
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
    easygui.msgbox('Name:superychen\nEmail:superychen@gmail.com', '关于作者')


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
# 模式选择页
# 加载模式选择页UI
def load_page_mode_widgets():
    background = load_image('ext/images/start_background_0.png', WINDOW)
    buttons = []

    button_start = Button((int((WINDOW[0] - DEFAULT_BUTTON_SIZE[0]) / 2), 250), 'ext/images/standalone_white.png',
                          size=DEFAULT_BUTTON_SIZE,
                          image_hover='ext/images/standalone_red.png',
                          on_click=standalone_click)
    buttons.append(button_start)
    button_end = Button((int((WINDOW[0] - DEFAULT_BUTTON_SIZE[0]) / 2), 360), 'ext/images/Internet_white.png',
                        size=DEFAULT_BUTTON_SIZE,
                        image_hover='ext/images/Internet_red.png', on_click=internet_click)
    buttons.append(button_end)
    button_author = Button((int((WINDOW[0] - DEFAULT_BUTTON_SIZE[0]) / 2), 470), 'ext/images/ai_white.png',
                           size=DEFAULT_BUTTON_SIZE,
                           image_hover='ext/images/ai_red.png', on_click=ai_click)
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
    easygui.msgbox('暂不支持 网络模式', '提示')
    # switch_page(PAGE_GAME)
    # global CUR_GAME_MODE
    # CUR_GAME_MODE = GAME_MODE_INTERNET


# 点击ai模式
def ai_click():
    easygui.msgbox('暂不支持 智能模式', '提示')
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


def draw_page_game():
    pass


# 分发点击事件
def dispatcher_click(event, position):
    if (CUR_PAGE == PAGE_WELCOME or CUR_PAGE == PAGE_MODE) and PAGES_DATA[CUR_PAGE]['loaded']:
        buttons = PAGES_DATA[CUR_PAGE]['widgets']['buttons']
        for button in buttons:
            button.dispatcher_mouse_event(event, position)


# 分发移动事件
def dispatcher_move(event, position):
    if (CUR_PAGE == PAGE_WELCOME or CUR_PAGE == PAGE_MODE) and PAGES_DATA[CUR_PAGE]['loaded']:
        buttons = PAGES_DATA[CUR_PAGE]['widgets']['buttons']
        for button in buttons:
            button.dispatcher_mouse_event(event, position)


if __name__ == '__main__':

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

        draw_page()

        pygame.display.flip()
