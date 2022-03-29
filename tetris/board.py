import pygame
from pygame import Surface
from typing import Iterable, Tuple, List, Union

class Block:
    """Board의 블럭을 생성하는 class입니다."""
    block_size = 24
    def __init__(self, location: Iterable[int], color: Surface) -> None:
        """
        Args:
            location (Iterable): 블럭 위치(길이 2).
            color (str): 블럭 색상.
        """
        iterator = iter(location)
        self.location : Tuple[int] = (24+24*next(iterator), 48+24*next(iterator))
        self.color    : Surface = color

# 블럭 색상 정보
block_size  = Block.block_size
blue        = pygame.image.load('./images/blue_%s.png'          % (block_size))
light_green = pygame.image.load('./images/light_green_%s.png'   % (block_size))
orange      = pygame.image.load('./images/orange_%s.png'        % (block_size))
purple      = pygame.image.load('./images/purple_%s.png'        % (block_size))
red         = pygame.image.load('./images/red_%s.png'           % (block_size))
sky_blue    = pygame.image.load('./images/sky_blue_%s.png'      % (block_size))
yellow      = pygame.image.load('./images/yellow_%s.png'        % (block_size))
grey        = pygame.image.load('./images/grey_%s.png'          % (block_size))

class Board:
    """플레이 중 보이는 12 * 22 크기의 보드판 정보를 담고있는 class입니다."""
    def __init__(self) -> None:
        """기본 보드판을 만들고 테두리 블럭을 생성합니다."""
        # 테두리 12 * 22
        # 내부   10 * 20
        self.board = [[None for _ in range(22)] for _ in range(12)]
        # 테두리(회색) 블럭
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (i == 0 or i == len(self.board)-1 or j == len(self.board[i])-1) and j != 0:
                    self.addBlock(i, j, grey)
            
    def __str__(self):
        return str(self.board)
    
    def row(self, index: int) -> List[Union[Block, None]]:
        """해당 y좌표의 행을 리스트로 가져옵니다.

        Args:
            index (int): 행 번호.

        Returns:
            List[Union[Block, None]]: 행.
        """
        return [column[index] for column in self.board]
    
    def column(self, index: int) -> List[Union[Block, None]]:
        """해당 x좌표의 열을 리스트로 가져옵니다.

        Args:
            index (int): 열 번호.

        Returns:
            List[Union[Block, None]]: 열.
        """
        return self.board[index]
    
    def addBlock(self, x: int, y: int, color: Surface) -> None:
        """보드판에 블럭 정보를 담아 저장합니다.

        Args:
            x (int): 열 번호.
            y (int): 행 번호.
            color (Surface): 색생 정보.
        """
        self.board[x][y] = Block(location=(x, y), color=color)
        
    def delBlock(self, x: int, y: int) -> None:
        """해당 위치에 있는 블럭 정보를 삭제합니다.

        Args:
            x (int): 열 번호.
            y (int): 행 번호.
        """
        self.board[x][y] = None
        
    def delLine(self, y: int) -> None:
        """해당 라인(행)의 블럭을 삭제합니다.

        Args:
            y (int): 행 번호.
        """
        for j in range(1, len(self.board)-1):
            for k in range(y, 0, -1):
                if k != 1 and isinstance(self.board[j][k-1], Block):
                    self.addBlock(j, k, color=self.board[j][k-1].color)
                else:
                    self.board[j][k] = None