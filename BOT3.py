import chess
import chess.engine
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class StockfishChessBot:
    def __init__(self, stockfish_path, difficulty, bot_as_white=True):
        try:
            self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start Stockfish engine: {e}")
            self.engine = None

        self.board = chess.Board()
        self.difficulty = difficulty
        self.bot_as_white = bot_as_white
        self.selected_square = None  # Track the selected square

        # Set dimensions
        self.width = 400
        self.height = 400
        self.square_size = self.width // 8  # Each square is 50x50 pixels

        # Create GUI
        self.create_gui()

        # If the bot is white, make its first move
        if self.bot_as_white:
            self.make_bot_move()

    def create_gui(self):
        self.window = tk.Tk()
        self.window.title("Chess Bot")

        # Load background image
        bg_image = Image.open("C:/Users/Maahir/ChessBOT/background.jpg")
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Set background label
        self.bg_label = tk.Label(self.window, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height)
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")

        self.piece_images = {}  # Store references to piece images
        self.load_piece_images()  # Load piece images
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.window.mainloop()

    def load_piece_images(self):
        piece_images = {
            'p': r"C:\Users\Maahir\ChessBOT\images\bp.png", 'r': r"C:\Users\Maahir\ChessBOT\images\br.png", 'n': r"C:\Users\Maahir\ChessBOT\images\bn.png", 
            'b': r"C:\Users\Maahir\ChessBOT\images\bb.png", 'q': r"C:\Users\Maahir\ChessBOT\images\bq.png", 'k': r"C:\Users\Maahir\ChessBOT\images\bk.png",
            'P': r"C:\Users\Maahir\ChessBOT\images\wp.png", 'R': r"C:\Users\Maahir\ChessBOT\images\wr.png", 'N': r"C:\Users\Maahir\ChessBOT\images\wn.png", 
            'B': r"C:\Users\Maahir\ChessBOT\images\wb.png", 'Q': r"C:\Users\Maahir\ChessBOT\images\wq.png", 'K': r"C:\Users\Maahir\ChessBOT\images\wk.png"
        }
        
        for piece, image_path in piece_images.items():
            image = Image.open(image_path)
            piece_photo = ImageTk.PhotoImage(image.resize((50, 50)))
            self.piece_images[piece] = piece_photo  # Keep a reference to avoid garbage collection

    def draw_board(self):
        self.canvas.delete("all")
        # Draw squares
        for row in range(8):
            for col in range(8):
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                if (row + col) % 2 == 0:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#eeeed2")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#769656")

        # Draw pieces
        for row in range(8):
            for col in range(8):
                piece = self.board.piece_at(chess.square(col, 7 - row))  # Get the piece object correctly
                if piece is not None:  # Ensure the piece is not None
                    piece_image = self.piece_images[piece.symbol()]
                    x = col * self.square_size + self.square_size // 2
                    y = row * self.square_size + self.square_size // 2
                    self.canvas.create_image(x, y, image=piece_image)

    def on_canvas_click(self, event):
        x, y = event.x // self.square_size, event.y // self.square_size
        clicked_square = chess.square(x, 7 - y)  # Adjust for GUI coordinate system

        if self.selected_square is None:
            # Select the piece
            piece = self.board.piece_at(clicked_square)
            if piece is not None and piece.color == self.board.turn:
                self.selected_square = clicked_square  # Remember the selected square
        else:
            # Attempt to move the selected piece
            move = chess.Move(self.selected_square, clicked_square)
            if move in self.board.legal_moves:
                self.handle_user_move(move.uci())
                self.selected_square = None  # Reset selection after move
            else:
                messagebox.showinfo("Invalid Move", "Please select a valid move.")
                self.selected_square = None  # Reset selection on invalid move

    def handle_user_move(self, user_move):
        try:
            # User's move
            move = chess.Move.from_uci(user_move)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.update_board()

                # Bot's move
                if not self.bot_as_white:  # If bot is black, make its move now
                    bot_move = self.get_bot_move()
                    if bot_move:
                        self.board.push(bot_move)
                        self.update_board()
            else:
                messagebox.showinfo("Invalid Move", "Please select a valid move.")
        except Exception as e:
            print(f"Invalid move: {e}")

    def make_bot_move(self):
        # Bot's first move is handled in the user move function.
        pass

    def get_bot_move(self):
        if self.engine is not None:
            self.engine.configure({"Skill Level": self.difficulty})
            bot_move = self.engine.play(self.board, chess.engine.Limit(time=2.0))
            return bot_move.move
        return None

    def update_board(self):
        self.draw_board()
        if self.board.is_game_over():
            messagebox.showinfo("Game Over", f"Game Over! Result: {self.board.result()}")

    def __del__(self):
        if self.engine is not None:
            self.engine.quit()

# Paths to your Stockfish executable and piece images
stockfish_path = r"C:\Users\Maahir\ChessBOT\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"
diff = input("Pls enter difficulty level")
difficulty = diff  # Set difficulty level (0-20)
# Initialize the bot as white or black
bot = StockfishChessBot(stockfish_path, difficulty, bot_as_white=False)  # Change to True for white
