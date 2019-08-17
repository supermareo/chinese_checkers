# coding=utf-8
# 控件封装
import pygame

STATE_NORMAL = 0
STATE_HOVER = 1
STATE_CLICKED = 2


class Button:
    IMG_DICT = {}

    # 按钮当前状态
    CUR_STATE = STATE_NORMAL

    def __init__(self, position, image_normal, size=(188, 69), image_pressed=None, image_hover=None, on_click=None,
                 sound=None):
        self.position = position
        self.size = size
        self.image_normal = image_normal
        self.image_hover = image_hover if image_hover is not None else image_normal
        self.image_pressed = image_pressed if image_pressed is not None else image_hover
        self.load_images()
        self.on_click = on_click
        self.sound = sound

    def load_image(self, path):
        if path not in self.IMG_DICT:
            image = pygame.image.load(path).convert_alpha()
            # 缩放到20*20大小
            image = pygame.transform.scale(image, self.size)
            self.IMG_DICT[path] = image

    def load_images(self):
        self.load_image(self.image_normal)
        self.load_image(self.image_hover)
        self.load_image(self.image_pressed)

    def dispatcher_mouse_event(self, event, point):
        # 如果是鼠标移动事件
        if event.type == pygame.MOUSEMOTION:
            if self.collision_detect(point):
                self.CUR_STATE = STATE_HOVER
            else:
                self.CUR_STATE = STATE_NORMAL
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.collision_detect(point):
                if self.sound is not None:
                    self.sound.play()
                self.CUR_STATE = STATE_CLICKED
                if self.on_click is not None:
                    # 调用点击回调方法
                    self.on_click()
            else:
                self.CUR_STATE = STATE_NORMAL

    def collision_detect(self, point):
        if self.position[0] <= point[0] <= (self.position[0] + self.size[0]) and \
                self.position[1] <= point[1] <= self.position[1] + self.size[1]:
            return True
        return False

    # 获取当前要绘制的图片
    def get_cur_image(self):
        return self.IMG_DICT[self.image_normal] if self.CUR_STATE is STATE_NORMAL \
            else self.IMG_DICT[self.image_hover] if self.CUR_STATE is STATE_HOVER \
            else self.IMG_DICT[self.image_pressed]
