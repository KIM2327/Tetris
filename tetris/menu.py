import sys
from .main import Main
from .setting import Setting
import pygame, time

class Menu:
    """메인화면의 정보를 담고있는 class입니다."""
    color_activated = (255, 255, 255)
    color_deactivated = (100, 100, 100)
    list_menu = ['Start', 'Settings', 'Quit']
    list_location = [(100, 100 + i*50) for i in range(len(list_menu))]
    list_setting = []
    
    def __init__(self) -> None:
        self.current = 0
    
    def up(self) -> None:
        """위로 커서를 옮깁니다."""
        self.current = (self.current - 1) % len(self.list_menu)
        
    def down(self) -> None:
        """아래로 커서를 옮깁니다."""
        self.current = (self.current + 1) % len(self.list_menu)
        
    def activate(self) -> None:
        """Menu를 출력합니다."""
        list_font = [ # 선택된 항목만 흰색으로 한다.
            Setting.sysfont.render(selected, True, self.color_activated) if self.current == i else
            Setting.sysfont.render(selected, True, self.color_deactivated)
            for i, selected in enumerate(self.list_menu)
        ]
        for i in range(len(self.list_menu)):
            Main.SURFACE.blit(list_font[i], self.list_location[i])
    
    # 각 메뉴별 기능 구현
    def select(self) -> None:
        "해당 메뉴를 선택합니다."
        selected = self.list_menu[self.current]
        if   selected == 'Start'   : # 현재시간을 넘기고 게임을 시작합니다.
            Main.Display = Main.play
            Main.play.__init__()
        elif selected == 'Settings': # 세팅 메뉴에 들어갑니다.
            Main.Display = Main.setting 
        elif selected == 'Quit'    : # 게임을 종료합니다.
            pygame.quit(); sys.exit()