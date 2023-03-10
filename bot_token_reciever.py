import prompt

bot_token = prompt.string("Введите токен бота: ")

with open("telegram_pass_bot/bot_token.py", "w") as file:
    file.write(f"TOKEN = '{bot_token}'")
