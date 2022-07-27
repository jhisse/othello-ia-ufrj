from models.move import Move
import logging
import random

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class ZagueiroPlayer:
    def __init__(self, color):
        self.valid_moves = None
        self.move = None
        self.color = color

        # Dangerous corners if most important places is empty
        self.danger_corners = [
            Move(1, 2), Move(2, 1), Move(2, 2),  # First Corner
            Move(1, 7), Move(2, 7), Move(2, 8),  # Second Corner
            Move(8, 2), Move(7, 1), Move(7, 2),  # Third Corner
            Move(8, 7), Move(7, 7), Move(7, 8),  # Fourth Corner
        ]

        # Most stable pieces if corners filled
        self.stable_corners = [
            Move(1, 2), Move(2, 1),  # First Corner
            Move(1, 7), Move(2, 8),  # Second Corner
            Move(8, 2), Move(7, 1),  # Third Corner
            Move(8, 7), Move(7, 8),  # Fourth Corner
        ]

        # Center of board
        self.center_board = [
            Move(3, 3), Move(3, 4), Move(3, 5), Move(3, 6),
            Move(4, 3),                         Move(6, 6),
            Move(5, 3),                         Move(6, 6),
            Move(6, 3), Move(6, 4), Move(6, 5), Move(6, 6),
        ]

        # Most important places
        self.corners = [Move(1, 1), Move(1, 8), Move(8, 1), Move(8, 8)]

        # Danger zone
        self.danger_square = [
            Move(2, 2), Move(2, 3), Move(2, 4), Move(2, 5), Move(2, 6), Move(2, 7),
            Move(3, 2),                                                 Move(3, 7),
            Move(4, 2),                                                 Move(4, 7),
            Move(5, 2),                                                 Move(5, 7),
            Move(6, 2),                                                 Move(6, 7),
            Move(7, 2), Move(7, 3), Move(7, 4), Move(7, 5), Move(7, 6), Move(7, 7),
        ]

        # Bigger square
        self.bigger_square = [
            Move(1, 1), Move(1, 2), Move(1, 3), Move(1, 4), Move(1, 5), Move(1, 6), Move(1, 7), Move(1, 8),
            Move(2, 1),                                                                         Move(2, 8),
            Move(3, 1),                                                                         Move(3, 8),
            Move(4, 1),                                                                         Move(4, 8),
            Move(5, 1),                                                                         Move(5, 8),
            Move(6, 1),                                                                         Move(6, 8),
            Move(7, 1),                                                                         Move(7, 8),
            Move(8, 1), Move(8, 2), Move(8, 3), Move(8, 4), Move(8, 5), Move(8, 6), Move(8, 7), Move(8, 8),
        ]

    def score_index(self, board):
        if board.WHITE == self.color:
            return 0
        return 1

    def check_corners(self, move):
        if move == Move(1, 1):
            self.danger_corners.remove(Move(1, 2))
            self.danger_corners.remove(Move(2, 1))
            self.danger_corners.remove(Move(2, 2))
        elif move == Move(1, 8):
            self.danger_corners.remove(Move(1, 7))
            self.danger_corners.remove(Move(2, 7))
            self.danger_corners.remove(Move(2, 8))
        elif move == Move(8, 1):
            self.danger_corners.remove(Move(8, 2))
            self.danger_corners.remove(Move(7, 1))
            self.danger_corners.remove(Move(7, 2))
        elif move == Move(8, 8):
            self.danger_corners.remove(Move(8, 7))
            self.danger_corners.remove(Move(7, 7))
            self.danger_corners.remove(Move(7, 8))

    def check_center(self, move):
        if move in self.center_board:
            self.center_board.remove(move)

    def play(self, board):
        # Generate valid moves and remove duplicates
        valid_moves = []
        [valid_moves.append(x) for x in board.valid_moves(self.color) if x not in valid_moves]

        # Fill most important place in board if you can: corners
        for m in valid_moves:
            if m in self.corners:
                self.check_corners(m)
                return m

        # Make sure if you have valid moves
        if len(valid_moves) == 0:
            return
        logger.debug("------\nValid moves:")
        for m in valid_moves:
            logger.debug(m)

        # Avoid neighbors of most import place in board
        best_moves_1 = [move for move in valid_moves if move not in self.danger_corners]
        logger.debug("------\nBest moves:")
        for m in best_moves_1:
            logger.debug(m)

        # Prefer stable places in board if corner filled
        best_moves_2 = [move for move in best_moves_1 if move in self.stable_corners]
        logger.debug("------\nBest moves stables:")
        for m in best_moves_2:
            logger.debug(m)

        # Avoid dangerous square
        if len(best_moves_2):
            best_moves_3 = [move for move in best_moves_2 if move not in self.danger_square]
        else:
            best_moves_3 = [move for move in best_moves_1 if move not in self.danger_square]
        logger.debug("------\nBest moves remove danger square:")
        for m in best_moves_3:
            logger.debug(m)

        # Prefer center of board in beging game
        best_moves_4 = [move for move in best_moves_3 if move in self.center_board]
        logger.debug("------\nBest moves in center:")
        for m in best_moves_4:
            logger.debug(m)

        # Prefer bigger square when center is filled
        best_moves_5 = []
        if len(self.center_board) == 0 or len(best_moves_4) == 0:
            best_moves_5 = [move for move in best_moves_3 if move in self.bigger_square]
            logger.debug("------\nBest moves in bigger square:")
            for m in best_moves_5:
                logger.debug(m)

        if len(best_moves_5):
            possible_moves = best_moves_5
        elif len(best_moves_4):
            possible_moves = best_moves_4
        elif len(best_moves_3):
            possible_moves = best_moves_3
        elif len(best_moves_2):
            possible_moves = best_moves_2
        elif len(best_moves_1):
            possible_moves = best_moves_1
        else:
            possible_moves = valid_moves

        # Evitar flipar peças no início do jogo
        if len(self.center_board) and len(best_moves_4):
            # seleciona o candidato que flipa menos peças
            candidate = (9999, None)
            for m in possible_moves:
                copy_board = board.get_clone()
                copy_board.play(m, self.color)
                score = copy_board.score()[self.score_index(board)]
                logger.debug(m)
                logger.debug(score)
                del copy_board
                if score < candidate[0]:
                    logger.debug("Candidato:", m)
                    candidate = (score, m)
            move = candidate[1]
        else:
            move = random.choice(possible_moves)
        print("Move: ", move)

        self.check_center(move)

        return move
