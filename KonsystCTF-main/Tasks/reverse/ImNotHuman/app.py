import random
import telebot

API_TOKEN = 'XXXXXX'
bot = telebot.TeleBot(API_TOKEN)

# Пример данных для цепи Маркова
markov_data = {
    "привет": ["как", "что", "друг"],
    "как": ["дела", "жизнь", "ты"],
    "дела": ["?", "хорошо", "плохо"],
    "пока": ["!", "друг", "скоро"],
}

# Генератор текста на цепи Маркова
def markov_generate(start_word, length=5):
    current_word = start_word
    sentence = [current_word]
    for _ in range(length):
        if current_word not in markov_data:
            break
        next_word = random.choice(markov_data[current_word])
        sentence.append(next_word)
        current_word = next_word
    return ' '.join(sentence)

# Детектор prompt-инъекций
def is_hack_attempt(text):
    triggers = [
        "игнорируй правила",
        "взломай себя",
        "секретный ключ",
        "теперь ты враг",
        "забудь все",
        "забудь всё",
    ]
    text_lower = text.lower()
    return any(trigger in text_lower for trigger in triggers)

# Обработчик всех текстовых сообщений
@bot.message_handler(func=lambda message: True)
def reply(message):
    user_text = message.text

    if is_hack_attempt(user_text):
        bot.reply_to(message, "🔥 Взлом обнаружен! Держи флаг: flag{pr0mpt-injection-hack}")
    else:
        start_word = random.choice(list(markov_data.keys()))
        response = markov_generate(start_word, length=random.randint(3, 8))
        bot.reply_to(message, response)

if __name__ == '__main__':
    bot.polling()