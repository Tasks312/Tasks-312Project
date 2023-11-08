import json

EMPTY = 0
RED = 1
YELLOW = 2

class Gamestate:
    WIDTH = 7
    HEIGHT = 6

    SPOTS = WIDTH * HEIGHT

    def __init__(self, p1: str, p2: str):
        self.p1 = p1
        self.p2 = p2
        
        self.turn = RED

        self.over = False

        self.board = [EMPTY for _ in range(0, Gamestate.SPOTS)]
        self.heights = [0 for _ in range(0, Gamestate.HEIGHT)]

    def can_place(self, x: int):
        if (x < 0 or x >= Gamestate.WIDTH):
            return False
        
        return self.heights[x] < Gamestate.HEIGHT

    # useful for saving to database
    def as_obj(self):
        return {
            "player1": self.p1,
            "player2": self.p2,
            "turn": self.turn,
            "over": self.over,
            "board": self.board
        }

    # useful for sending to players
    def as_JSON(self):
        return json.dumps(self.as_obj())

    # places a thing and checks for win, returns True on successful place
    # sets self.over to True when win is detected
    def place(self, x: int):
        # this column is full! (or out of range)
        if (not self.can_place(x)):
            return False

        # place the marker
        height = self.heights[x]
        self.heights[x] += 1
        self.board[height * Gamestate.WIDTH + x] = self.turn

        # Win checking (sets self.Over = True)
        consecutive = 0

        # ---O---
        startX = max(x - 3, 0)
        endX = min(x + 3, Gamestate.WIDTH - 1)

        baseIdx = height * Gamestate.WIDTH
        for i in range(startX, endX + 1):
            if (self.board[baseIdx + i] == self.turn):
                consecutive += 1
                if (consecutive >= 4):
                    self.over = True
                    return True

            else:
                consecutive = 0

        # vertical |
        if (height >= 3):
            consecutive = 0

            
            startY = max(height - 3, 0)
            endY = min(height + 3, Gamestate.HEIGHT - 1)

            for i in range(startY, endY + 1):
                if (self.board[i * Gamestate.WIDTH + x] == self.turn):
                    consecutive += 1
                    if (consecutive >= 4):
                        self.over = True
                        return True

                else:
                    consecutive = 0

        consecutive = 0
        consecutived = 0

        # diag / and \
        for i in range(0, 7):
            cx = x + i - 3

            cuy = height + i - 3
            cdy = height - i + 3

            if (cx < 0 or cx >= Gamestate.WIDTH):
                continue

            # /
            if (cuy >= 0 and cuy < Gamestate.HEIGHT):
                if (self.board[cuy * Gamestate.HEIGHT + cx] == self.turn):
                    consecutive += 1
                    if (consecutive >= 4):
                        self.over = True
                        return True
                    
                else:
                    consecutive = 0

            # \
            if (cdy >= 0 and cdy < Gamestate.HEIGHT):
                if (self.board[cdy * Gamestate.HEIGHT + cx] == self.turn):
                    consecutived += 1
                    if (consecutived >= 4):
                        self.over = True
                        return True
                    
                else:
                    consecutived = 0

        return True

# useful for loading from database
def from_obj(obj):
    out = Gamestate(obj["player1"], obj["player2"])
    out.turn = obj["turn"]
    out.over = obj["over"]

    out.board = obj["board"]

    for y in range(0, Gamestate.HEIGHT):
        base = y * Gamestate.WIDTH
        for x in range(0, Gamestate.WIDTH):
            if (out.board[base + x] != EMPTY):
                out.heights[x] += 1

    return out


