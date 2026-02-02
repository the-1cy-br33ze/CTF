import socket
import random
from threading import Thread
from collections import defaultdict

PORT = 10001
STARTING_CHIPS = 1000
TARGET_WINS = 10
FLAG = "flag{P0ker_StrAnge_Rule$}"  # Фиксированный флаг

class PokerServer:
    def __init__(self):
        self.suits = ['♥', '♦', '♣', '♠']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.client_stats = defaultdict(lambda: {'wins': 0, 'chips': STARTING_CHIPS})

    def shuffle_deck(self):
        return [f"{rank}{suit}" for suit in self.suits for rank in self.ranks]

    def deal_cards(self, deck, n):
        return [deck.pop(random.randint(0, len(deck)-1)) for _ in range(n)]

    def evaluate_hand(self, hand):
        """Определяем силу комбинации"""
        ranks = [card[:-1] for card in hand]
        suits = [card[-1] for card in hand]
        
        if len(set(suits)) == 1:
            return 2  # Флеш
        if len(set(ranks)) < len(hand):
            return 1  # Пара
        return 0  # Старшая карта

    def handle_client(self, conn, addr):
        try:
            client_id = f"{addr[0]}:{addr[1]}"
            stats = self.client_stats[client_id]
            
            conn.sendall(
                f"Добро пожаловать в покер! Победите в {TARGET_WINS} раундах, чтобы получить флаг.\n"
                f"Стартовый баланс: {STARTING_CHIPS} фишек. Удачи!\n".encode()
            )

            while stats['wins'] < TARGET_WINS:
                deck = self.shuffle_deck()
                
                # Ставка
                conn.sendall(b"Ваша ставка (10-100): ")
                bet = int(conn.recv(1024).decode().strip())
                bet = max(10, min(100, bet))
                
                if bet > stats['chips']:
                    conn.sendall(b"Недостаточно фишек!\n")
                    continue

                # Раздача
                player_hand = self.deal_cards(deck, 2)
                bot_hand = self.deal_cards(deck, 2)
                
                conn.sendall(f"Ваши карты: {', '.join(player_hand)}\n".encode())
                conn.sendall(b"Действие (fold/call/raise): ")
                action = conn.recv(1024).decode().strip().lower()

                if action == "fold":
                    stats['chips'] -= bet
                    conn.sendall(
                        f"Вы сбросили карты. Бот побеждает. "
                        f"Побед: {stats['wins']}/{TARGET_WINS}. Баланс: {stats['chips']}\n".encode()
                    )
                    continue

                # Определяем победителя
                player_score = self.evaluate_hand(player_hand)
                bot_score = self.evaluate_hand(bot_hand)
                
                if player_score > bot_score:
                    stats['chips'] += bet
                    stats['wins'] += 1
                    conn.sendall(
                        f"Вы выиграли! Побед: {stats['wins']}/{TARGET_WINS}. "
                        f"Баланс: {stats['chips']}\n".encode()
                    )
                else:
                    stats['chips'] -= bet
                    conn.sendall(
                        f"Бот выиграл. Побед: {stats['wins']}/{TARGET_WINS}. "
                        f"Баланс: {stats['chips']}\n".encode()
                    )

                if stats['chips'] <= 0:
                    conn.sendall(b"Фишки закончились! Игра окончена.\n")
                    break

            if stats['wins'] >= TARGET_WINS:
                conn.sendall(f"Поздравляем! Ваш флаг: {FLAG}\n".encode())

        except Exception as e:
            print(f"Ошибка с {addr}: {e}")
        finally:
            conn.close()

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', PORT))
            s.listen()
            print(f"Сервер покера запущен на порту {PORT}...")
            
            while True:
                conn, addr = s.accept()
                print(f"Новое подключение: {addr}")
                Thread(target=self.handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    server = PokerServer()
    server.start()