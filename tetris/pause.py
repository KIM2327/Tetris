import sys
from .main import Main
from .setting import Setting
from .board import Block
import pygame, time

class Pause:
    """게임 중 중지 화면의 정보를 담고있는 class입니다."""
    color_activated = (255, 255, 255)
    color_deactivated = (100, 100, 100)
    list_menu = ['Restart/Unpause', 'Menu', 'Quit']
    list_location = [(100, 100 + i*50) for i in range(len(list_menu))]
    list_setting = []
    
    def __init__(self, x: str = 'Unpause') -> None:
        """
        Args:
            x (str, optional): 정지인지 게임이 끝났는지 구분. Only 'Restart' or 'Unpause'. Defaults to 'Unpause'.
        """
        self.current = 0
        Pause.list_menu[0] = x
    
    def up(self) -> None:
        """위로 커서를 옮깁니다."""
        self.current = (self.current - 1) % len(self.list_menu)
        
    def down(self) -> None:
        """아래로 커서를 옮깁니다."""
        self.current = (self.current + 1) % len(self.list_menu)
        
    def activate(self) -> None:
        """현재 진행중인 플레이 화면과 중지 메뉴 화면을 출력합니다."""
        # 블럭 출력
        for column in Main.board.board:
            for block in column:
                if block != None:
                    Main.SURFACE.blit(block.color, block.location)
        # 미노 출력
        for x, y in Main.play.mino_loc:
            block = Block(location=(x + Main.play.parallel[0], y + Main.play.parallel[1]), color=Main.play.mino_color)
            Main.SURFACE.blit(block.color, block.location)
        # 다음 Mino 출력
        for x, y in Main.play.nextmino[:-1]:
            block = Block(location=(x + 15, y + 2), color=Main.play.nextmino[-1])
            Main.SURFACE.blit(block.color, block.location)
        # Holded mino 출력
        for x, y in Main.play.holded_mino[:-1]:
            block = Block(location=(x + 15, y + 11), color=Main.play.holded_mino[-1])
            Main.SURFACE.blit(block.color, block.location)
        # 점수 출력
        Score = Setting.sysfont.render(str(Main.play.score).zfill(8), True, (255, 255, 255))
        Main.SURFACE.blit(Score, (445, 445))
        # 선택사항 출력
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
        if selected == 'Restart':
            Main.Display = Main.play
            # 초기화하고 재시작한다.
            self.__init__()
            Main.play.__init__()
            Main.board.__init__()
        elif selected == 'Unpause':
            Main.Display = Main.play
            Main.play.start_time = time.time() # 현재시간을 넘긴다.
        elif selected == 'Menu':
            Main.Display = Main.menu
            # 초기화하고 메뉴로 나간다.
            Main.play.__init__()
            Main.board.__init__()
        elif selected == 'Quit':
            pygame.quit(); sys.exit()