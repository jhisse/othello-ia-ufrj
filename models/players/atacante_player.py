from models.move import Move
import logging
import random

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class AtacantePlayer:
    def __init__(self, color):
        self.color = color
        self.cache_board = {}
        self.depth = 7
        self.corners = [Move(1, 1), Move(1, 8), Move(8, 1), Move(8, 8)]

    @staticmethod
    def get_valid_moves(board, color):
        moves = []
        # Remover movimentos duplicados
        [moves.append(x) for x in board.valid_moves(color) if x not in moves]
        return moves

    def minimax_max_player(self, board, depth, a, b):
        moves = self.get_valid_moves(board, board.BLACK)

        # Se chegar ao final ou nao ter mais jogadas: parar
        if depth == 0 or len(moves) == 0:
            score_white, score_black = board.score()
            return score_black

        value = -9999
        for move in moves:
            # Realiza o movimento
            board_tmp = board.get_clone()
            board_tmp.play(move, board.BLACK)
            if self.cache_board.get(str(board_tmp)):
                score = self.cache_board[str(board_tmp)]
            else:
                score = self.minimax_min_player(board_tmp, depth - 1, a, b)
                self.cache_board[str(board_tmp)] = score
            # Exclui variável temporária
            del board_tmp

            value = max(value, score)
            a = max(a, value)
            if value >= b:
                break
        return value

    def minimax_min_player(self, board, depth, a, b):
        moves = self.get_valid_moves(board, board.WHITE)

        # Se chegar ao final ou nao ter mais jogadas: parar
        if depth == 0 or len(moves) == 0:
            score_white, score_black = board.score()
            return score_white

        value = 9999
        for move in moves:
            # Realiza o movimento
            board_tmp = board.get_clone()
            board_tmp.play(move, board.WHITE)
            if self.cache_board.get(str(board_tmp)):
                score = self.cache_board[str(board_tmp)]
            else:
                score = self.minimax_max_player(board_tmp, depth - 1, a, b)
                self.cache_board[str(board_tmp)] = score
            # Exclui variável temporária
            del board_tmp
            value = min(value, score)
            b = min(b, value)
            if value <= a:
                break
        return value

    def play(self, board):
        # Generate valid moves and remove duplicates
        valid_moves = self.get_valid_moves(board, self.color)

        if len(valid_moves) == 0:
            return

        best_move = valid_moves[0]
        board_tmp = board.get_clone()
        board_tmp.play(best_move, self.color)
        if self.color == board.BLACK:
            best_score = -9999
        else:
            best_score = 9999

        for move in valid_moves:
            if move in self.corners:
                best_move = move
                break
            board_tmp = board.get_clone()
            if self.color == board.BLACK:
                score = self.minimax_max_player(board_tmp, self.depth, -9999, 9999)
                if score > best_score:
                    best_move = move
                    best_score = score
                if score == best_score:
                    best_move = random.choice([best_move, move])
            else:
                score = self.minimax_min_player(board_tmp, self.depth, -9999, 9999)
                if score < best_score:
                    best_move = move
                    best_score = score
                if score == best_score:
                    best_move = random.choice([best_move, move])
            del board_tmp

        return best_move
