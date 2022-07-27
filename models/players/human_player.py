from models.move import Move


class HumanPlayer:
    def __init__(self, color):
        self.color = color

    def play(self, board):
        while True:
            try:
                rowInp = int(input("Linha: "))
                break
            except:
                print("Linha deve ser um número de 1 a 8\n")
                continue
        while True:
            try:
                colInp = int(input("Coluna: "))
                break
            except:
                print("Coluna deve ser um número de 1 a 8\n")
                continue
        move = Move(rowInp, colInp)
        while move not in board.valid_moves(self.color):
            print("Movimento invalido.Insira um valido")
            print(board)
            while True:
                try:
                    rowInp = int(input("Linha: "))
                    break
                except:
                    print("Linha deve ser um número de 1 a 8\n")
                    continue
            while True:
                try:
                    colInp = int(input("Coluna: "))
                    break
                except:
                    print("Coluna deve ser um número de 1 a 8\n")
                    continue
            move = Move(rowInp, colInp)
        return move
