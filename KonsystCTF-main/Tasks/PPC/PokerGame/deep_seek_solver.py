import socket
import random
import time

HOST = '127.0.0.1'
PORT = 10001

class PokerBot:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.combinations = {
            'high_card': 0,
            'pair': 1,
            'flush': 2
        }
    
    def connect(self):
        self.socket.connect((HOST, PORT))
        print(self.socket.recv(1024).decode())  # Приветственное сообщение
    
    def play_round(self):
        while True:
            data = self.socket.recv(1024).decode()
            if not data:
                break
            
            print(f"[Server]: {data.strip()}")
            
            if "Place your bet" in data:
                # Ставим минимальную ставку для минимизации рисков
                bet = 10
                self.socket.sendall(f"{bet}\n".encode())
                print(f"[Bot]: Bet {bet}")
            
            elif "Your hand:" in data:
                # Парсим карты игрока
                hand = data.split(":")[1].strip().split(", ")
                hand_score = self.evaluate_hand(hand)
                
                # Выбираем действие на основе силы руки
                if hand_score >= self.combinations['pair']:
                    action = "raise"
                else:
                    action = random.choice(["fold", "call"])  # Иногда блефуем
                
                self.socket.sendall(f"{action}\n".encode())
                print(f"[Bot]: Action {action}")
            
            elif "Congratulations!" in data:
                print("[Bot]: Flag captured!")
                return True
            
            elif "You're out of chips" in data:
                print("[Bot]: Out of chips!")
                return False
            
            time.sleep(0.5)  # Чтобы не перегружать сервер
    
    def evaluate_hand(self, hand):
        ranks = [card[:-1] for card in hand]
        suits = [card[-1] for card in hand]
        
        if len(set(suits)) == 1:
            return self.combinations['flush']
        if len(set(ranks)) < len(hand):
            return self.combinations['pair']
        return self.combinations['high_card']
    
    def run(self):
        self.connect()
        while True:
            if self.play_round():
                break

if __name__ == "__main__":
    bot = PokerBot()
    bot.run()