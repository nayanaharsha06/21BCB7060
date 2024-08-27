from flask import Flask, request, jsonify, render_template

class Figure:
    def __init__(self, name, player, row, col):
        self.name = name
        self.player = player
        self.row = row
        self.col = col

    def movement(self, dr, dc, board):
        new_r, new_c = self.row + dr, self.col + dc
        if 0 <= new_r < 5 and 0 <= new_c < 5:
            if board[new_r][new_c] is None:
                board[self.row][self.col] = None
                self.row, self.col = new_r, new_c
                board[new_r][new_c] = self
                return True
        return False

class Pawn(Figure):
    def movement(self, direction, board):
        directions = {'L': (-1, 0), 'R': (1, 0), 'F': (0, -1), 'B': (0, 1)}
        if direction in directions:
            dr, dc = directions[direction]
            return super().movement(dr, dc, board)
        return False

class Hero1(Figure):
    def movement(self, direction, board):
        directions = {'L': (-2, 0), 'R': (2, 0), 'F': (0, -2), 'B': (0, 2)}
        if direction in directions:
            dr, dc = directions[direction]
            return super().movement(dr, dc, board)
        return False

class Hero2(Figure):
    def movement(self, direction, board):
        directions = {'L': (-2, -2), 'R': (2, -2), 'F': (-2, -2), 'B': (2, 2)}
        if direction in directions:
            dr, dc = directions[direction]
            return super().movement(dr, dc, board)
        return False

class Game:
    def __init__(self):
        self.board = [[None for _ in range(5)] for _ in range(5)]
        self.players = {'A': [], 'B': []}
        self.turn = 'A'

    def start_game(self):
        # Set up the board with the correct layout
        self.players['A'] = [
            Pawn('P1', 'A', 0, 0),
            Pawn('P2', 'A', 0, 1),
            Hero1('H1', 'A', 0, 2),
            Hero2('H2', 'A', 0, 3),
            Pawn('P3', 'A', 0, 4)
        ]
        self.players['B'] = [
            Pawn('P1', 'B', 4, 0),
            Pawn('P2', 'B', 4, 1),
            Hero1('H1', 'B', 4, 2),
            Hero2('H2', 'B', 4, 3),
            Pawn('P3', 'B', 4, 4)
        ]
        for piece in self.players['A']:
            self.board[piece.row][piece.col] = piece
        for piece in self.players['B']:
            self.board[piece.row][piece.col] = piece

    def move(self, player, figure_name, direction):
        if player != self.turn:
            return False
        for piece in self.players[player]:
            if piece.name == figure_name:
                if piece.movement(direction, self.board):
                    self.turn = 'B' if self.turn == 'A' else 'A'
                    return True
        return False

    def curr_board_state(self):
        return [[None if cell is None else f"{cell.player}-{cell.name}" for cell in row] for row in self.board]

# Initialize the Flask application
app = Flask(__name__)

# Initialize the game instance
game_instance = Game()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    game_instance.start_game()
    return jsonify({"message": "Game started", "board_state": game_instance.curr_board_state()}), 200

@app.route('/move', methods=['POST'])
def make_move():
    data = request.json
    player = data.get('player')
    figure_name = data.get('figure_name')
    direction = data.get('direction')
    
    if not player or not figure_name or not direction:
        return jsonify({"error": "Missing parameters"}), 400
    
    success = game_instance.move(player, figure_name, direction)
    
    if success:
        return jsonify({"message": "Move successful", "board_state": game_instance.curr_board_state()}), 200
    else:
        return jsonify({"error": "Move failed"}), 400

@app.route('/board_state', methods=['GET'])
def get_board_state():
    return jsonify({"board_state": game_instance.curr_board_state()}), 200

if __name__ == '__main__':
    app.run(debug=True)
