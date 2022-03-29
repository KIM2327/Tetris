from .main import Main
from .setting import Setting
from .board import Block, blue, light_green, orange, purple, red, sky_blue, yellow
import time, math, random
from typing import Tuple, List

class Play:
    # 4 x 4 블럭
    I_mino = (2, 0), (2, 1), (2, 2), (2, 3), sky_blue
    O_mino = (1, 1), (1, 2), (2, 1), (2, 2), yellow
    Z_mino = (0, 1), (1, 1), (1, 2), (2, 2), red
    S_mino = (1, 1), (2, 1), (0, 2), (1, 2), light_green
    J_mino = (2, 0), (2, 1), (1, 2), (2, 2), orange
    L_mino = (1, 0), (1, 1), (1, 2), (2, 2), blue
    T_mino = (1, 1), (1, 2), (1, 3), (2, 2), purple
    
    def __init__(self) -> None:
        self.start_time = time.time()
        # self.bag = {self.I_mino, self.O_mino, self.Z_mino, self.S_mino, self.J_mino, self.L_mino, self.T_mino} # 순서가 고정되는 현상 발생
        self.bag = [self.I_mino, self.O_mino, self.Z_mino, self.S_mino, self.J_mino, self.L_mino, self.T_mino]
        random.shuffle(self.bag)
        self.nextMino()
        self.holded_mino = self.nextmino
        self.nextMino()
        self.setMino()
        self.parallel = [4, -1]
        self.setDifficulty()
        
    def setDifficulty(self):
        """난이도를 설정한다."""
        difficulty = Setting.Difficulty
        if   difficulty == 'Easy':
            self.score      = 0
            self.drop_time  = 0.3 # sec
        elif difficulty == 'Normal':
            self.score      = 200
            self.drop_time  = 0.2
        elif difficulty == 'Hard':
            self.score      = 400
            self.drop_time  = 0.15
        
    def nextMino(self) -> None: # 7-bag rule
        """7-bag 규칙을 이용해서 다음 Mino를 가져옵니다."""
        self.nextmino = self.bag.pop()
        if self.bag == []:
            self.bag = [self.I_mino, self.O_mino, self.Z_mino, self.S_mino, self.J_mino, self.L_mino, self.T_mino]
            random.shuffle(self.bag) # 리스트 요소들의 순서를 섞는다.
        
    def setMino(self) -> None:
        """다음 Mino를 현재 Mino로 바꾸고 다음 Mino를 새로 설정합니다."""
        self.mino_loc   = self.nextmino[:-1]
        self.mino_color = self.nextmino[-1]
        self.nextMino()
        
    def isBlocked(self, changed_loc: Tuple[Tuple[int, int]], x: int = 0, y: int = 0) -> bool:
        """블럭을 상하좌우로 x, y만큼 움직였을 때 변형 가능한지 판단하는 method입니다.

        Args:
            changed_loc (Tuple[Tuple[int, int]]): 변형 후 Mino.
            x (int): 좌우측 확인 범위.
            y (int): 상하 확인 범위.

        Returns:
            bool: 변형 가능 여부.
        """
        for i, j in changed_loc:
            if Main.board.board[i + self.parallel[0] + x][j + self.parallel[1] + y] != None:
                return True
        return False
        
    def rotate(self): # Clockwise
        """시계 방향으로 회전 시킵니다."""
        def rotation(loc: Tuple[int, int]) -> Tuple[int, int]:
            """복소수 연산을 이용하여 회전시킵니다."""
            c = complex(loc[0], loc[1])
            c -= 1.5 + 1.5j
            c *= 1j # 시계방향 *반시계 방향은 -1j를 곱해준다.
            c += 1.5 + 1.5j
            return tuple(map(math.trunc, (c.real, c.imag)))
        # 회전했을 때 (좌우로 2칸까지) 가로막는 블럭이 있는지 확인한고 없으면 회전한다.
        rotated = tuple(map(rotation, self.mino_loc))
        for x in (0, -1, 1, -2, 2):
            if not self.isBlocked(rotated, x):
                self.mino_loc = rotated
                self.parallel[0] += x
                break
    
    def left(self):
        """좌측으로 이동합니다."""
        if not self.isBlocked(self.mino_loc, -1):
            self.parallel[0] -= 1
    
    def right(self):
        """우측으로 이동합니다."""
        if not self.isBlocked(self.mino_loc, 1):
            self.parallel[0] += 1

    def softDrop(self) -> bool:
        """아래 이동합니다."""
        if self.isBlocked(self.mino_loc, y=1):
            self.mino_to_board()
            self.parallel = [4, -1]
            return False
        else:
            self.parallel[1] += 1
            return True
        
    def mino_to_board(self):
        """Mino를 Board로 보내고 다음 Mino를 불러옵니다."""
        for i, j in self.mino_loc:
            Main.board.addBlock(i + self.parallel[0], j + self.parallel[1], self.mino_color)
        # 블럭라인 제거 후 점수 추가 및 난이도 조정
        for i in range(1, len(Main.board.column(0))-1):
            if None not in Main.board.row(i):
                Main.board.delLine(i)
                self.score += 10
                if   self.score >= 600: self.drop_time = 0.12 # Very Hard
                elif self.score >= 400: self.drop_time = 0.15 # Hard
                elif self.score >= 200: self.drop_time = 0.2  # Normal
        self.setMino()
    
    def hardDrop(self):
        """Mino블럭을 가장 아래로 내립니다."""
        while self.softDrop():
            pass
    
    def hold(self): # Shift
        """현재 블럭을 홀드합니다."""
        holded_mino = [*self.mino_loc, self.mino_color]
        # 홀드했을 때 (좌우로 2칸까지) 가로막는 블럭이 있는지 확인하고 없으면 홀드한다.
        for x in (0, -1, 1, -2, 2):
            if not self.isBlocked(self.holded_mino[:-1], x):
                self.mino_loc, self.mino_color = [*self.holded_mino[:-1]], self.holded_mino[-1]
                self.holded_mino = tuple(holded_mino)
                self.parallel[0] += x
                break
        
    def activate(self):
        # 자동 드롭
        drop_count = int((time.time() - self.start_time) / self.drop_time)
        self.start_time += drop_count * self.drop_time
        for i in range(drop_count):
            self.softDrop()
        # 블럭 출력
        for column in Main.board.board:
            for block in column:
                if block != None:
                    Main.SURFACE.blit(block.color, block.location)
        # 미노 출력
        for x, y in self.mino_loc:
            block = Block(location=(x + self.parallel[0], y + self.parallel[1]), color=self.mino_color)
            Main.SURFACE.blit(block.color, block.location)
        # 다음 Mino 출력
        for x, y in self.nextmino[:-1]:
            block = Block(location=(x + 15, y + 2), color=self.nextmino[-1])
            Main.SURFACE.blit(block.color, block.location)
        # Holded mino 출력
        for x, y in self.holded_mino[:-1]:
            block = Block(location=(x + 15, y + 11), color=self.holded_mino[-1])
            Main.SURFACE.blit(block.color, block.location)
        # 점수 출력
        Score = Setting.sysfont.render(str(self.score).zfill(8), True, (255, 255, 255))
        Main.SURFACE.blit(Score, (445, 445))
        # 패배
        if Main.board.board[5][1] or Main.board.board[6][1]:
            Main.pause.__init__('Restart')
            Main.Display = Main.pause
            
        