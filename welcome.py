# # coding=utf-8
# import pygame
# import os
#
# # 页面内部padding=40
# SCREEN_PADDING = 40
# # 宽 = 高 = 15
# SIZE = 15
# # 水平方向单位距离
# HORIZONTAL_GAP = 80
# # 垂直方向单位距离
# VERTICAL_GAP = 40
# # 界面宽高，高度预留30用于文字绘制
# WIDTH = SCREEN_PADDING * 2 + (SIZE - 1) * HORIZONTAL_GAP
# HEIGHT = SCREEN_PADDING * 2 + (SIZE - 1) * VERTICAL_GAP + 30
#
# IMG_DICT = {}
#
# # 初始化pygame
# pygame.init()
#
#
# def load_imgs():
#     image_files = os.listdir('ext/imgs')
#     for image_file in image_files:
#         image = pygame.image.load("ext/welcome/" + image_file).convert_alpha()
#         # # 缩放到20*20大小
#         # pygame.transform.scale(image, (20, 20))
#         IMG_DICT[image_file.split('.')[0]] = image
#
#
# def process_click(clicked_pos):
#     pass
#
#
# if __name__ == '__main__':
#     # 页面绘制的fps设置，防止绘制过频繁性能下降
#     fps = 10
#     clock = pygame.time.Clock()
#     # 运行中的标识，设置为false后游戏停止
#     running_flag = True
#
#     # 设置屏幕尺寸
#     screen = pygame.display.set_mode((WIDTH, HEIGHT))
#     # 设置标题
#     pygame.display.set_caption('国际数棋')
#     # 加载图片资源
#     load_imgs()
#
#     while running_flag:
#         # 限制绘制频率
#         clock.tick(fps)
#
#         # 处理事件
#         for event in pygame.event.get():
#             # 检查是否关闭窗口
#             if event.type == pygame.QUIT:
#                 running_flag = False
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 process_click(pygame.mouse.get_pos())
#
#         # 刷新屏幕
#         pygame.display.flip()
