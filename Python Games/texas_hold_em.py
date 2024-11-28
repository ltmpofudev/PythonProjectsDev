from PIL import Image, ImageTk
import os
import time
import tkinter as tk
from tkinter import messagebox
import random
from typing import List, Tuple, Dict
import math

class Card:
    def __init__(self, suit: str, value: str):
        self.suit = suit
        self.value = value
        
    def __str__(self):
        return f"{self.value} of {self.suit}"
        
    def get_numeric_value(self) -> int:
        values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
                 '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        return values[self.value]

class CardWidget(tk.Canvas):
    def __init__(self, master, card, width=100, height=150, *args, **kwargs):
        super().__init__(master, width=width, height=height, *args, **kwargs)
        self.card = card
        self.width = width
        self.height = height
        self.configure(bg='white', highlightthickness=1, highlightbackground='black')
        self._draw_card()
        
    def _draw_card(self):
        # Card border
        self.create_rectangle(5, 5, self.width-5, self.height-5, 
                               fill='white', outline='black', width=2)
        
        # Color based on suit
        color = 'red' if self.card.suit in ['Hearts', 'Diamonds'] else 'black'
        
        # Top left value
        self.create_text(15, 20, text=self._format_value(self.card.value), 
                         fill=color, font=('Arial', 16, 'bold'))
        
        # Bottom right value (inverted)
        self.create_text(self.width-15, self.height-20, text=self._format_value(self.card.value), 
                         fill=color, font=('Arial', 16, 'bold'), angle=180)
        
        # Draw suit
        self._draw_suit(color)
        
    def _format_value(self, value):
        # Special handling for face cards and 10
        if value == '10':
            return '10'
        elif value in ['J', 'Q', 'K', 'A']:
            return value
        return value
    
    def _draw_suit(self, color):
        # Center coordinates
        cx, cy = self.width // 2, self.height // 2
        
        if self.card.suit == 'Hearts':
            self._draw_heart(cx, cy, color)
        elif self.card.suit == 'Diamonds':
            self._draw_diamond(cx, cy, color)
        elif self.card.suit == 'Clubs':
            self._draw_club(cx, cy, color)
        elif self.card.suit == 'Spades':
            self._draw_spade(cx, cy, color)
        
    def _draw_heart(self, cx, cy, color):
        # Draw a heart shape
        points = [
            cx, cy-20, 
            cx-20, cy-40, 
            cx-10, cy-50, 
            cx, cy-40,
            cx+10, cy-50,
            cx+20, cy-40,
        ]
        self.create_polygon(points, fill=color, outline=color)
        
    def _draw_diamond(self, cx, cy, color):
        # Draw a diamond shape
        points = [
            cx, cy-25,
            cx-15, cy,
            cx, cy+25,
            cx+15, cy
        ]
        self.create_polygon(points, fill=color, outline=color)
        
    def _draw_club(self, cx, cy, color):
        # Draw a club shape with three circles and a stem
        r = 10  # radius
        self.create_oval(cx-r, cy-r, cx+r, cy+r, fill=color, outline=color)
        self.create_oval(cx-r-10, cy, cx+r-10, cy+2*r, fill=color, outline=color)
        self.create_oval(cx+r-10, cy, cx+3*r-10, cy+2*r, fill=color, outline=color)
        self.create_rectangle(cx-2, cy+2*r, cx+2, cy+2*r+20, fill=color, outline=color)
        
    def _draw_spade(self, cx, cy, color):
        # Draw a spade shape
        points = [
            cx, cy-25,
            cx-20, cy+10,
            cx-10, cy+20,
            cx, cy+10,
            cx+10, cy+20,
            cx+20, cy+10
        ]
        self.create_polygon(points, fill=color, outline=color)
        self.create_rectangle(cx-2, cy+20, cx+2, cy+35, fill=color, outline=color)

class Deck:
    def __init__(self):
        self.cards = []
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for suit in suits:
            for value in values:
                self.cards.append(Card(suit, value))
                
    def shuffle(self):
        random.shuffle(self.cards)
        
    def draw(self) -> Card:
        return self.cards.pop()

class Player:
    def __init__(self, name: str, chips: int = 1000, is_ai: bool = False):
        self.name = name
        self.chips = chips
        self.hand = []
        self.is_ai = is_ai
        self.current_bet = 0
        self.folded = False
        
    def receive_card(self, card: Card):
        self.hand.append(card)
        
    def clear_hand(self):
        self.hand = []
        
    def make_decision(self, current_bet: int, pot: int, community_cards: List[Card]) -> Tuple[str, int]:
        if self.is_ai:
            return self._ai_decision(current_bet, pot, community_cards)
        return None, 0
        
    def _ai_decision(self, current_bet: int, pot: int, community_cards: List[Card]) -> Tuple[str, int]:
        # Simple AI logic
        hand_strength = random.random()  # In a real implementation, evaluate hand strength
        
        if hand_strength < 0.3:
            return 'fold', 0
        elif hand_strength < 0.7:
            if current_bet > self.chips // 4:
                return 'fold', 0
            return 'call', current_bet
        else:
            raise_amount = min(current_bet * 2, self.chips)
            return 'raise', raise_amount

class PokerGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Texas Hold'em Poker")
        self.master.geometry("1200x800")
        
        self.create_home_screen()
        
    def create_home_screen(self):
        self.home_frame = tk.Frame(self.master)
        self.home_frame.pack(expand=True)
        
        title = tk.Label(self.home_frame, text="Texas Hold'em Poker", font=('Arial', 24))
        title.pack(pady=20)
        
        play_button = tk.Button(self.home_frame, text="Play Game", command=self.start_game)
        play_button.pack(pady=10)
        
        quit_button = tk.Button(self.home_frame, text="Quit", command=self.master.quit)
        quit_button.pack(pady=10)
        
    def start_game(self):
        self.home_frame.destroy()
        self.setup_game()
        self.create_game_screen()
        self.play_round()
        
    def setup_game(self):
        self.deck = Deck()
        self.pot = 0
        self.current_bet = 0
        self.community_cards = []
        self.players = [
            Player("You", 1000, False),
            Player("AI 1", 1000, True),
            Player("AI 2", 1000, True),
            Player("AI 3", 1000, True)
        ]
        self.current_player_index = 0
        
    def create_game_screen(self):
        self.game_frame = tk.Frame(self.master)
        self.game_frame.pack(expand=True, fill='both')
        
        # Community cards area
        self.community_frame = tk.Frame(self.game_frame)
        self.community_frame.pack(pady=20)
        
        # Player hands area
        self.player_frame = tk.Frame(self.game_frame)
        self.player_frame.pack(pady=20)
        
        # Action buttons
        self.action_frame = tk.Frame(self.game_frame)
        self.action_frame.pack(pady=20)
        
        self.fold_button = tk.Button(self.action_frame, text="Fold", command=lambda: self.player_action("fold"))
        self.fold_button.pack(side=tk.LEFT, padx=5)
        
        self.call_button = tk.Button(self.action_frame, text="Call", command=lambda: self.player_action("call"))
        self.call_button.pack(side=tk.LEFT, padx=5)
        
        self.raise_button = tk.Button(self.action_frame, text="Raise", command=lambda: self.player_action("raise"))
        self.raise_button.pack(side=tk.LEFT, padx=5)
        
        # Info display
        self.info_label = tk.Label(self.game_frame, text="")
        self.info_label.pack(pady=10)
        
    def update_display(self):
        # Clear previous displays
        for widget in self.community_frame.winfo_children():
            widget.destroy()
        for widget in self.player_frame.winfo_children():
            widget.destroy()
            
        # Show community cards
        tk.Label(self.community_frame, text="Community Cards:").pack()
        community_card_frame = tk.Frame(self.community_frame)
        community_card_frame.pack()
        for card in self.community_cards:
            CardWidget(community_card_frame, card).pack(side=tk.LEFT, padx=5)
        
        # Show player's hand
        tk.Label(self.player_frame, text="Your Hand:").pack()
        player_hand_frame = tk.Frame(self.player_frame)
        player_hand_frame.pack()
        for card in self.players[0].hand:
            CardWidget(player_hand_frame, card).pack(side=tk.LEFT, padx=5)
        
        # Update info
        info_text = f"Pot: ${self.pot} | Current Bet: ${self.current_bet}"
        self.info_label.config(text=info_text)
        
    def player_action(self, action: str):
        player = self.players[0]
        
        if action == "fold":
            player.folded = True
        elif action == "call":
            bet_amount = self.current_bet - player.current_bet
            player.chips -= bet_amount
            self.pot += bet_amount
            player.current_bet = self.current_bet
        elif action == "raise":
            raise_amount = self.current_bet * 2
            player.chips -= raise_amount
            self.pot += raise_amount
            self.current_bet = raise_amount
            player.current_bet = raise_amount
            
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.play_round()
        
    def play_round(self):
        if len(self.community_cards) == 0:
            self.deal_initial_cards()
        elif len(self.community_cards) == 3:
            self.community_cards.append(self.deck.draw())  # Turn
        elif len(self.community_cards) == 4:
            self.community_cards.append(self.deck.draw())  # River
        else:
            self.end_round()
            return
            
        self.update_display()
        
        # AI players' turns
        while self.current_player_index != 0:
            player = self.players[self.current_player_index]
            if player.is_ai and not player.folded:
                action, amount = player.make_decision(self.current_bet, self.pot, self.community_cards)
                if action == "fold":
                    player.folded = True
                elif action == "call":
                    player.chips -= amount
                    self.pot += amount
                    player.current_bet = self.current_bet
                elif action == "raise":
                    player.chips -= amount
                    self.pot += amount
                    self.current_bet = amount
                    player.current_bet = amount
                    
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            
        self.update_display()
        
    def deal_initial_cards(self):
        self.deck.shuffle()
        # Deal two cards to each player
        for _ in range(2):
            for player in self.players:
                player.receive_card(self.deck.draw())
        # Deal flop
        self.community_cards = [self.deck.draw() for _ in range(3)]
        
    def end_round(self):
        # Simple winner determination (can be expanded with proper hand evaluation)
        active_players = [p for p in self.players if not p.folded]
        if len(active_players) == 1:
            winner = active_players[0]
        else:
            winner = random.choice(active_players)  # Simplified winner selection
            
        winner.chips += self.pot
        messagebox.showinfo("Round End", f"{winner.name} wins ${self.pot}!")
        
        # Reset for next round
        self.pot = 0
        self.current_bet = 0
        self.community_cards = []
        self.current_player_index = 0
        for player in self.players:
            player.clear_hand()
            player.folded = False
            player.current_bet = 0
            
        self.play_round()

if __name__ == "__main__":
    root = tk.Tk()
    game = PokerGame(root)
    root.mainloop()
