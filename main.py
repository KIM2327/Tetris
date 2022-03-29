import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE, K_ESCAPE, K_LSHIFT
from tetris import *
import time

pygame.init()
SURFACE = pygame.display.set_mode([*Setting.display_size]) # 기본 화면크기 600*600.
pygame.display.set_caption("TETRIS")
FPSCLOCK = pygame.time.Clock()

# 초기 세팅
Main.SURFACE = SURFACE

def main():
    """main routine"""
    # Play, Board, Menu, Setting, Pause 객체를 Main class에 담는다.
    play = Play()
    board = Board()
    menu = Menu()
    setting = Setting()
    pause = Pause()
    Main.play = play
    Main.board = board
    Main.menu = menu
    Main.setting = setting
    Main.pause = pause
    # 처음에는 메인 메뉴를 출력한다.
    Main.Display = menu
    # 배경화면을 불러온다.
    background = pygame.image.load('./images/background_600.png')
    bg_play    = pygame.image.load('./images/bg_play_600.png')
    
    while True:
        # 배경화면을 출력한다.
        if   isinstance(Main.Display, Menu)     : SURFACE.blit(background, (0, 0))
        elif isinstance(Main.Display, Setting)  : SURFACE.blit(background, (0, 0))
        elif isinstance(Main.Display, Play)     : SURFACE.blit(bg_play, (0, 0))
        elif isinstance(Main.Display, Pause)    : SURFACE.blit(bg_play, (0, 0))
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    if   isinstance(Main.Display, Menu)     : menu.up()
                    elif isinstance(Main.Display, Setting)  : setting.up()
                    elif isinstance(Main.Display, Pause)    : pause.up()
                    elif isinstance(Main.Display, Play)     : play.rotate()
                elif event.key == K_DOWN:
                    if   isinstance(Main.Display, Menu)     : menu.down()
                    elif isinstance(Main.Display, Setting)  : setting.down()
                    elif isinstance(Main.Display, Pause)    : pause.down()
                    elif isinstance(Main.Display, Play)     : play.softDrop(); play.start_time = time.time()
                elif event.key == K_LEFT:
                    if   isinstance(Main.Display, Menu)     : pass
                    elif isinstance(Main.Display, Setting)  : pass
                    elif isinstance(Main.Display, Pause)    : pass
                    elif isinstance(Main.Display, Play)     : play.left()
                elif event.key == K_RIGHT:
                    if   isinstance(Main.Display, Menu)     : pass
                    elif isinstance(Main.Display, Setting)  : pass
                    elif isinstance(Main.Display, Pause)    : pass
                    elif isinstance(Main.Display, Play)     : play.right()
                elif event.key == K_SPACE:
                    if   isinstance(Main.Display, Menu)     : menu.select()
                    elif isinstance(Main.Display, Setting)  : setting.select()
                    elif isinstance(Main.Display, Pause)    : pause.select()
                    elif isinstance(Main.Display, Play)     : play.hardDrop(); play.start_time = time.time()
                elif event.key == K_LSHIFT:
                    if   isinstance(Main.Display, Menu)     : pass
                    elif isinstance(Main.Display, Setting)  : pass
                    elif isinstance(Main.Display, Pause)    : pass
                    elif isinstance(Main.Display, Play)     : play.hold(); play.start_time = time.time()
                elif event.key == K_ESCAPE:
                    if   isinstance(Main.Display, Menu)     : pass
                    elif isinstance(Main.Display, Setting)  : pass
                    elif isinstance(Main.Display, Pause)    : pass
                    elif isinstance(Main.Display, Play)     : Main.Display = pause
                    
        # 디스플레이
        Main.Display.activate()
        
        pygame.display.update()
        FPSCLOCK.tick(setting.FPS) # FPS 설정


if __name__ == '__main__':
    main()