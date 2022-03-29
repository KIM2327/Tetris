from .main import Main
import pygame, math
from typing import List, Union

pygame.init()

class Setting:
    """설정 정보를 담고있는 class입니다.
    (현재 화면 크기 변경 미구현)"""
    # 초기 설정 (FPS, 난이도, 화면크기 등등)
    list_FPS        = [24, 30, 60, 75, 90, 120, 144]
    list_Difficulty = ['Easy', 'Normal', 'Hard']
    list_scale      = [1, 1.5, 2, 3]
    list_font_size  = [24, 36, 48, 72]
    FPS     = list_FPS[1]
    Difficulty = list_Difficulty[1]
    scale   = list_scale[1]
    font_size = list_font_size[1]
    base_height = base_width = 400
    display_size = tuple(map(math.trunc, [base_width*scale, base_height*scale]))
    sysfont = pygame.font.SysFont(None, 36)
    # 색상
    color_activated   = (255, 255, 255)
    color_deactivated = (100, 100, 100)
    # 설정 항목
    list_menu = ['   Screen Size', '   FPS', '   Difficulty', '<-Back to Menu']
    list_location = [(100, 100 + i*50) for i in range(len(list_menu))]
    # 현재 설정된 값
    list_setting          = ['{} x {}(x{})'.format(*display_size, scale), str(FPS), Difficulty]
    list_setting_location = [(350, 100 + i*50) for i in range(len(list_setting))]
    
    def __init__(self) -> None:
        self.current = 0
    
    def up(self) -> None:
        """위로 커서를 옮깁니다."""
        self.current -= 1
        if self.current < 0:
            self.current = len(self.list_menu) - 1
        
    def down(self) -> None:
        """아래로 커서를 옮깁니다."""
        self.current += 1
        if self.current >= len(self.list_menu):
            self.current = 0
        
    def activate(self):
        """Setting을 출력합니다."""
        list_font = [ # 선택된 항목만 흰색으로 한다.
            self.sysfont.render(selected, True, self.color_activated) if self.current == i else
            self.sysfont.render(selected, True, self.color_deactivated)
            for i, selected in enumerate(self.list_menu)
        ]
        for i in range(len(self.list_menu)):
            Main.SURFACE.blit(list_font[i], self.list_location[i])
            
        list_font = [ # 선택된 항목만 흰색으로 한다.
            self.sysfont.render(selected, True, self.color_activated) if self.current == i else
            self.sysfont.render(selected, True, self.color_deactivated)
            for i, selected in enumerate(self.list_setting)
        ]
        for i in range(len(self.list_setting)):
            Main.SURFACE.blit(list_font[i], self.list_setting_location[i])
    
    @classmethod
    def apply(cls):
        """변경된 설정 사항들을 적용합니다."""
        cls.display_size = tuple(map(math.trunc, [cls.base_width*cls.scale, cls.base_height*cls.scale]))
        # cls.list_location = [(cls.display_size[0] // 2 - 100, 100 + i*50) for i in range(len(cls.list_menu))]
        cls.list_setting = ['{} x {}(x{})'.format(*cls.display_size, cls.scale), str(cls.FPS), cls.Difficulty]
        cls.list_setting_location = [(cls.list_location[i][0] + 250, 100 + i*50) for i in range(len(cls.list_setting))]
        # cls.sysfont = pygame.font.SysFont(None, cls.font_size)
        pygame.display.set_mode(cls.display_size)
    
    @staticmethod
    def next_level(current: Union[int, float, str],
                   type_list: List[Union[int, float, str]],
                   ) -> Union[int, float, str]:
        """다음 단계를 가져옵니다.

        Args:
            current (Union[int, float, str]): 현재 설정 사항.
            type_list (List[Union[int, float, str]]): 해당 설정의 모든 단계별 정보가 담긴 List.

        Returns:
            Union[int, float, str]: 다음 단계값.
        """
        index = type_list.index(current)
        if current == type_list[-1]: # 제일 높을 때는 가장 낮게 설정한다.
            next_ = type_list[0]
        else:
            next_ = type_list[index + 1]
        return next_
    
    # 각 메뉴별 기능 구현
    def select(self) -> None:
        "해당 메뉴를 선택합니다."
        selected = self.list_menu[self.current]
        # 현재 설정을 확인하고 한 단계 높게 설정하거나 메인 메뉴로 돌아간다.
        if   selected == '   Screen Size':
            Setting.scale = self.next_level(self.scale, self.list_scale)
            # Setting.font_size = self.next_level(self.font_size, self.list_font_size)
            self.apply()
        elif selected == '   FPS':
            Setting.FPS = self.next_level(self.FPS, self.list_FPS)
            self.apply()
        elif selected == '   Difficulty':
            Setting.Difficulty = self.next_level(self.Difficulty, self.list_Difficulty)
            self.apply()
        elif selected == '<-Back to Menu':
            Main.Display = Main.menu