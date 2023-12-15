from board import Board, Emotion


class Game:
    def __init__(self):
        size = int(input("Сторона поля ? "))
        if not 2 <= size <= 11:
            print(Emotion.add_exclamation("Должно выполняться условие 2 <= size <= 11"))
            self.__init__()

        count = int(input("Количество фигур в ряд ? "))
        if count > size:
            print(Emotion.add_exclamation("Должно выполняться условие count_to_win <= size"))
            self.__init__()

        self.board = Board(size, count)

        # счётчик, который увеличивается после каждого хода
        # если чётный - ход крестиков
        self.stage = 0

        self.game_loop()

    def game_loop(self):
        self.board.print_field()
        while True:
            cordinates = list(map(int, input(f"Ход {'крестиков' if self.stage % 2 == 0 else 'ноликов'}."
                                             f" Введите координаты по оси x и y через пробел: ").split()))

            success = self.board.set_figure(self.stage, cordinates)  # Был ли сделан ход
            if success:
                self.board.print_field()
                self.stage += 1

                win = self.board.check_win(cordinates)
                if win:
                    print(win)
                    if input('Хотите сыгать ещё? Y/N ') == 'Y':
                        self.__init__()
                    break

                if self.board.check_draw(self.stage):
                    print(Emotion.add_indifference('Ничья'))
                    if input('Хотите сыгать ещё? Y/N ') == 'Y':
                        self.__init__()
                    break


g = Game()
