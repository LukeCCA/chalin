import random


class Piece:
    def __init__(self, shape, loc: tuple):
        self.shape = shape
        self._loc = loc

    def show(self):
        shape = [[' ', ' ', ' '],
                 [' ', ' ', ' '],
                 [' ', ' ', ' ']]
        for i, j in self.shape:
            shape[i][j] = 1


class Puzzle:
    def __init__(self, shape: tuple):
        self.row, self.col = shape
        self._get_random_puzzle()

    def get_piece(self):
        loc = random.choice(self._puzzle_connect.keys())
        puzzle_shape = set(self._puzzle_connect.pop(loc))
        return Piece(puzzle_shape, loc)

    def _get_random_puzzle(self):
        self._puzzle_connect = {}
        self._puzzle_record = {}
        for r in range(self.row):
            for c in range(self.col):
                r_idx = (r * 2) + 1
                c_idx = (c * 2) + 1
                self._puzzle_connect[(r, c)] = [(1, 1)]
                self._puzzle_record[(r_idx, c_idx)] = True

                if self._is_right_edge(c) & self._is_upper_edge(r):
                    self._puzzle_connect[(r, c)] += [(2, 1), (2, 2), (1, 2)]
                    self._puzzle_record[(r_idx + 1, c_idx)] = True
                    self._puzzle_record[(r_idx + 1, c_idx + 1)] = True
                    self._puzzle_record[(r_idx, c_idx + 1)] = True
                    if not self._puzzle_record.get((r_idx - 1, c_idx + 1),
                                                   False):
                        self._puzzle_connect[(r, c)] += [(0, 2)]
                        self._puzzle_record[(r_idx - 1, c_idx + 1)] = True

                elif self._is_right_edge(c):
                    self._puzzle_connect[(r, c)] += [(1, 2)]
                    self._puzzle_record[(r_idx, c_idx + 1)] = True
                    if not self._puzzle_record.get((r_idx - 1, c_idx + 1),
                                                   False):
                        self._puzzle_connect[(r, c)] += [(0, 2)]
                        self._puzzle_record[(r_idx - 1, c_idx + 1)] = True

                elif self._is_upper_edge(r):
                    self._puzzle_connect[(r, c)] += [(2, 1)]
                    self._puzzle_record[(r_idx + 1, c_idx)] = True
                    if not self._puzzle_record.get((r_idx + 1, c_idx - 1),
                                                   False):
                        self._puzzle_connect[(r, c)] += [(2, 0)]
                        self._puzzle_record[(r_idx + 1, c_idx - 1)] = True

                self._puzzle_connect[(r, c)] += \
                    self._generate_choose_set(r_idx, c_idx)

    def _generate_choose_set(self, r_idx, c_idx):
        choose_set = []
        if not self._puzzle_record.get((r_idx - 1, c_idx + 1), False):
            choose_set.append(((r_idx - 1, c_idx + 1),
                               (0, 2)))

        if not self._puzzle_record.get((r_idx, c_idx + 1), False):
            choose_set.append(((r_idx, c_idx + 1),
                               (1, 2)))

        if not self._puzzle_record.get((r_idx + 1, c_idx + 1), False):
            choose_set.append(((r_idx + 1, c_idx + 1),
                               (2, 2)))

        if not self._puzzle_record.get((r_idx + 1, c_idx), False):
            choose_set.append(((r_idx + 1, c_idx),
                               (2, 1)))

        if not self._puzzle_record.get((r_idx + 1, c_idx - 1), False):
            choose_set.append(((r_idx + 1, c_idx - 1),
                               (2, 0)))
        pick_num = min(len(choose_set), random.randint(1, 3))
        choose_set += random.choices(choose_set, k=pick_num)

        if not self._puzzle_record.get((r_idx, c_idx - 1), False):
            choose_set.append(((r_idx, c_idx - 1),
                               (1, 0)))
        if not self._puzzle_record.get((r_idx - 1, c_idx - 1), False):
            choose_set.append(((r_idx - 1, c_idx - 1),
                               (0, 0)))
        if not self._puzzle_record.get((r_idx - 1, c_idx), False):
            choose_set.append(((r_idx - 1, c_idx),
                               (0, 1)))
        puzzle_shape = []
        for loc, shape in choose_set:
            self._puzzle_record[loc] = True
            puzzle_shape.append(shape)

        return puzzle_shape

    def _is_left_edge(self, c):
        return (c == 0)

    def _is_right_edge(self, c):
        return (c == (self.col - 1))

    def _is_upper_edge(self, r):
        return (r == (self.row - 1))

    def _is_lower_edge(self, r):
        return (r == 0)


def fitwith(puz1, puz2):
    r1, c1 = puz1._loc
    r2, c2 = puz2._loc
    dist = max(abs(r1 - r2), abs(c1 - c2))
    if dist == 1:
        return True
    else:
        return False
