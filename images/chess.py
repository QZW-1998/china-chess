import sys

import pygame
import pygame
from pygame.locals import *


class Chess(object):
    def __init__(self, screen, chess_name, row, col):
        self.screen = screen
        self.name = chess_name  # 新增棋子名称属性
        self.image = pygame.image.load("imgs/s1/" + chess_name + ".png")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.set_pos(row, col)  # 改为方法调用

    def set_pos(self, row, col):
        """设置棋子的屏幕坐标"""
        self.row = row
        self.col = col
        self.top_left = (110 + col * 65, 125 + row * 53)

    def show(self):
        self.screen.blit(self.image, self.top_left)


class ChessBoard(object):
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("imgs/s2/bg.png")
        self.image = pygame.transform.scale(self.image, (600, 600))
        self.top_left = (100, 100)
        self.selected_chess = None  # 当前选中的棋子
        self.current_player = 'red'  # 当前玩家
        self.create_chess()

    def show_chess(self):
        for row in self.chess_map:
            for chess in row:
                if chess:
                    chess.show()

    def show_chessboard_and_chess(self):
        """显示棋盘和棋子（合并方法）"""
        self.show()  # 显示棋盘
        self.show_chess()  # 显示棋子

    # ... 保持原有 show 方法不变 .
    def show(self):
        self.screen.blit(self.image, self.top_left)

    def create_chess(self):
        # 初始化棋子布局（二维数组）
        self.chess_map = [
            [None] * 9 for _ in range(10)
        ]
        init_layout = [
            ["b_c", "b_m", "b_x", "b_s", "b_j", "b_s", "b_x", "b_m", "b_c"],
            ["", "", "", "", "", "", "", "", ""],
            ["", "b_p", "", "", "", "", "", "b_p", ""],
            ["b_z", "", "b_z", "", "b_z", "", "b_z", "", "b_z"],
            ["", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", ""],
            ["r_z", "", "r_z", "", "r_z", "", "r_z", "", "r_z"],
            ["", "r_p", "", "", "", "", "", "r_p", ""],
            ["", "", "", "", "", "", "", "", ""],
            ["r_c", "r_m", "r_x", "r_s", "r_j", "r_s", "r_x", "r_m", "r_c"],
        ]
        for row in range(10):
            for col in range(9):
                if init_layout[row][col]:
                    self.chess_map[row][col] = Chess(
                        self.screen, init_layout[row][col], row, col)

    def get_click_pos(self, mouse_pos):
        """将鼠标点击位置转换为棋盘坐标"""
        x, y = mouse_pos
        col = (x - 110) // 65
        row = (y - 125) // 53
        if 0 <= row < 10 and 0 <= col < 9:
            return (row, col)
        return None

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        """移动规则验证（基础示例）"""
        chess = self.chess_map[start_row][start_col]
        target = self.chess_map[end_row][end_col]

        if not chess:
            return False  # 起点没有棋子

        # 基础规则检查
        if not chess or (target and chess.name[0] == target.name[0]):
            return False  # 不能吃己方棋子

        # 根据不同棋子类型验证移动规则
        # 棋子名称格式为
        # 获取棋子类型(如'p'表示炮，'m'表示马，'x'表示象，'s'表示士，'j'表示将，'z'表示卒，'c'表示车)
        piece_type = chess.name[-1]

        # 根据棋子类型调用相应的验证函数
        if piece_type == 'c':  # 车
            return self.validate_chariot(start_row, start_col, end_row, end_col)
        elif piece_type == 'm':  # 马
            return self.validate_horse(start_row, start_col, end_row, end_col)
        elif piece_type == 'x':  # 象
            return self.validate_elephant(start_row, start_col, end_row, end_col)
        elif piece_type == 's':  # 士
            return self.validate_guard(start_row, start_col, end_row, end_col)
        elif piece_type == 'j':  # 将
            return self.validate_general(start_row, start_col, end_row, end_col)
        elif piece_type == 'p':  # 炮
            return self.validate_cannon(start_row, start_col, end_row, end_col)
        elif piece_type == 'z':  # 卒
            return self.validate_soldier(start_row, start_col, end_row, end_col)

        # 其他棋子类型..
        return False

    def validate_chariot(self, start_row, start_col, end_row, end_col):
        """车移动规则验证"""
        # 直线移动
        if start_row != end_row and start_col != end_col:
            return False

        # 路径检查
        step = 1 if end_row > start_row else -1 if end_row < start_row else 0
        if step == 0:  # 横向移动
            step = 1 if end_col > start_col else -1
            for col in range(start_col + step, end_col, step):
                if self.chess_map[start_row][col]:
                    return False
        else:  # 纵向移动
            for row in range(start_row + step, end_row, step):
                if self.chess_map[row][start_col]:
                    return False
        return True

    def validate_horse(self, start_row, start_col, end_row, end_col):
        """马移动规则验证"""
        dx = abs(end_col - start_col)
        dy = abs(end_row - start_row)
        if not ((dx == 1 and dy == 2) or (dx == 2 and dy == 1)):
            return False

        # 蹩马腿检查
        if dx == 2:
            mid_col = (start_col + end_col) // 2
            if self.chess_map[start_row][mid_col]:
                return False
        else:
            mid_row = (start_row + end_row) // 2
            if self.chess_map[mid_row][start_col]:
                return False
        return True

    def validate_elephant(self, start_row, start_col, end_row, end_col):
        """象移动规则验证"""
        # 1. 检查是否为田字移动
        dx = abs(end_col - start_col)
        dy = abs(end_row - start_row)
        if not (dx == 2 and dy == 2):
            return False  # 不是田字移动

        # 2. 检查是否过河
        if self.chess_map[start_row][start_col].name.startswith('b'):  # 黑象
            if end_row > 4:  # 黑象不能过河
                return False
        else:  # 红象
            if end_row < 5:  # 红象不能过河
                return False

        # 3. 检查象眼是否被阻挡
        mid_row = (start_row + end_row) // 2
        mid_col = (start_col + end_col) // 2
        if self.chess_map[mid_row][mid_col]:
            return False  # 象眼被阻挡

        return True

    def validate_guard(self, start_row, start_col, end_row, end_col):
        """士移动规则验证"""
        # 1. 检查是否在九宫格内
        if self.chess_map[start_row][start_col].name.startswith('s'):  # 黑士
            if not (0 <= end_row <= 2 and 3 <= end_col <= 5):
                return False  # 黑士不能出九宫格
        else:  # 红士
            if not (7 <= end_row <= 9 and 3 <= end_col <= 5):
                return False  # 红士不能出九宫格

        # 2. 检查是否为斜线移动一格
        dx = abs(end_col - start_col)
        dy = abs(end_row - start_row)
        if not (dx == 1 and dy == 1):
            return False  # 不是斜线移动一格

        return True

    def validate_general(self, start_row, start_col, end_row, end_col):
        """将军移动规则验证"""
        # 1. 检查是否在九宫格内
        if self.chess_map[start_row][start_col].name.startswith('j'):  # 黑将
            if not (0 <= end_row <= 2 and 3 <= end_col <= 5):
                return False  # 黑将不能出九宫格
        else:  # 红将
            if not (7 <= end_row <= 9 and 3 <= end_col <= 5):
                return False  # 红将不能出九宫格

        # 2. 检查是否为直线移动一个格
        dx = abs(end_col - start_col)
        dy = abs(end_row - start_row)
        if not (dx + dy == 1):
            return False  # 不是直线移动

        return True

    # 炮移动规则验证
    def validate_cannon(self, start_row, start_col, end_row, end_col):
        """炮移动规则验证"""
        # 黑炮
        # 1. 检查是否为直线移动
        if start_row != end_row and start_col != end_col:
            return False

        # 2. 计算路径上的棋子数量
        count = 0
        if start_row == end_row:  # 横向移动
            step = 1 if end_col > start_col else -1
            for col in range(start_col + step, end_col, step):
                if self.chess_map[start_row][col]:
                    count += 1

        else:  # 纵向移动
            step = 1 if end_row > start_row else -1
            for row in range(start_row + step, end_row, step):
                if self.chess_map[row][start_col]:
                    count += 1

        # 3. 判断是否合法
        target = self.chess_map[end_row][end_col]
        if target:  # 吃子时需要隔一个棋子
            return count == 1
        else:  # 不吃子时不能有棋子阻挡
            return count == 0

        # 兵移动规则验证
        def validate_soldier(self, start_row, start_col, end_row, end_col):
            """兵移动规则验证"""
            dx = abs(end_col - start_col)  # 横向移动距离
            dy = end_row - start_row  # 纵向移动距离（有方向）

            # 获取棋子名称
            piece = self.chess_map[start_row][start_col]

            # 黑兵规则
            if piece.name.startswith('b'):
                if start_row >= 5:  # 黑兵未过河
                    # 只能向前走一步，不能左右移动
                    if not ((dy == 1 and dx == 0) or (dy == 0 and dx == 1)):
                        return False
                else:  # 黑兵过河
                    # 只能向前走一步，或者左右移动一格
                    if not (dy == 1 and dx == 0):
                        return False

            # 红兵规则
            elif piece.name.startswith('r'):
                if start_row <= 4:  # 红兵未过河
                    # 只能向前走一步，不能左右移动
                    if not ((dy == -1 and dx == 0) or (dy == 0 and dx == 1)):
                        return False
                else:  # 红兵过河
                    # 只能向前走一步，或者左右移动一格
                    if not (dy == -1 and dx == 0):
                        return False

            return True

    def move_chess(self, start_pos, end_pos):
        """执行棋子移动"""
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        chess = self.chess_map[start_row][start_col]

        # 执行移动
        self.chess_map[end_row][end_col] = chess
        self.chess_map[start_row][start_col] = None
        chess.set_pos(end_row, end_col)

        # 切换玩家
        self.current_player = 'black' if self.current_player == 'red' else 'red'
        self.selected_chess = None


def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption('中国象棋')
    clock = pygame.time.Clock()

    chessboard = ChessBoard(screen)
    background = pygame.image.load('imgs/s2/bg.jpg')
    background = pygame.transform.scale(background, (1000, 800))

    while True:
        # 事件处理
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = chessboard.get_click_pos(pygame.mouse.get_pos())
                if pos:
                    row, col = pos
                    if chessboard.selected_chess:
                        # 尝试移动棋子
                        if chessboard.is_valid_move(*chessboard.selected_chess, row, col):
                            chessboard.move_chess(chessboard.selected_chess, (row, col))
                        else:
                            chessboard.selected_chess = None
                    else:
                        # 选择棋子
                        chess = chessboard.chess_map[row][col]
                        if chess and chess.name.startswith(chessboard.current_player[0]):
                            chessboard.selected_chess = (row, col)

        # 绘制
        screen.blit(background, (0, 0))
        chessboard.show_chessboard_and_chess()

        # 绘制选中状态
        if chessboard.selected_chess:
            row, col = chessboard.selected_chess
            pygame.draw.rect(screen, (255, 0, 0),
                             (110 + col * 65 - 5, 125 + row * 53 - 5, 70, 60), 3)

        pygame.display.flip()
        clock.tick(60)  # 限制帧率


if __name__ == '__main__':
    main()
