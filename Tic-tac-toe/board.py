class Emoji:
    CROSS = "❌"
    ZERO = "⭕"
    EMPTY = "⬜️"
    NUMBERS = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]


class Emotion:
    @staticmethod
    def add_exclamation(row_s):
        return f"❗️{row_s}❗️"

    @staticmethod
    def add_happiness(row_s):
        return f"🥳{row_s}🥳"

    @staticmethod
    def add_indifference(row_s):
        return f"😐{row_s}😐"


class Board:
    def __init__(self, size: int, count):
        self.size = size
        self.field = self.create_field(size)
        self.count_to_win = count  # количество фигур для победы

    def create_field(self, size: int) -> list:
        """
        :param size: размер поля
        :return: представление поля в виде двумерного массива
        """
        return [[Emoji.EMPTY for _ in range(size)] for __ in range(size)]

    def set_figure(self, stage, cordinates):
        try:
            if self.field[cordinates[1]][cordinates[0]] != Emoji.EMPTY:
                print(Emotion.add_exclamation('Эта клетка уже занята'))
                return 0
            figure = Emoji.CROSS if stage % 2 == 0 else Emoji.ZERO
            self.field[cordinates[1]][cordinates[0]] = figure
            return 1
        except IndexError:
            print(Emotion.add_exclamation('Указаны неверные координаты'))
            return 0

    def _emodji_trace(self, x_start, y_start, x_direction, y_direction):
        """
        Вспомогательная функция для check_win.
        Двигаемся по полю начиная с x_start; y_start в указанном направлении
        пока не зайдём за границу поля, попутно собирая находщиеся внутри значения
        в строку
        :param x_start: отсюда начинается движение
        :param y_start: отсюда начинается движение
        :param x_direction: на это значение меняется координата
        :param y_direction: на это значение меняется координата
        :return: Возвращает sting, состоящую из эмодзи
        """
        trace = ""
        while 0 <= x_start < self.size and 0 <= y_start < self.size:
            trace += self.field[y_start][x_start]
            x_start += x_direction
            y_start += y_direction
        return trace

    def check_win(self, cordinates):
        """
        :param cordinates: координаты фигуры, которую поставили последней
        :return: стока с указанием победителя или False
        """
        x, y = cordinates

        # посчитаем по диагонали с левого верхнего в правый нижний
        x_start, y_start = x - min(x, y), y - min(x, y)
        trace1 = self._emodji_trace(x_start, y_start, 1, 1)
        # print(trace1)

        # посчитаем по диагонали с правого верхнего в левый нижний
        offset = min(self.size - 1 - x, y)
        x_start, y_start = x + offset, y - offset
        trace2 = self._emodji_trace(x_start, y_start, -1, 1)
        # print(trace2)

        # посчитаем горизонталь слева на право
        trace3 = self._emodji_trace(0, y, 1, 0)
        # print(trace3)

        # посчитаем вертикаль сверху вниз
        trace4 = self._emodji_trace(x, 0, 0, 1)
        # print(trace4)

        all_traces = [trace1, trace2, trace3, trace4]

        if any(Emoji.ZERO * self.count_to_win in trace for trace in all_traces):
            return f"{Emotion.add_happiness('Нолики победили')}"
        elif any(Emoji.CROSS * self.count_to_win in trace for trace in all_traces):
            return f"{Emotion.add_happiness('Крестики победили')}"
        return False

    def check_draw(self, stage):
        if stage == self.size ** 2:
            return True
        return False

    def print_field(self):
        header = f"⬜️|{'|'.join([Emoji.NUMBERS[i] for i in range(self.size)])}|"
        print(header)
        for i in range(self.size):
            print(f"{Emoji.NUMBERS[i]}|{'|'.join(self.field[i])}|")
