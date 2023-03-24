import random
import telebot
import os
import time
import string

if not os.path.exists(f"Users"):
    os.mkdir(f"Users")

bot = telebot.TeleBot('5867697688:AAG6vDyPz7Qb6bAU0Cf0i5DYXPm4uYHX4Bg', parse_mode='HTML')

answers = {
    0: "<b>Точно нет</b>",
    1: "Думаю, <b>нет</b>",
    2: "Скорее всего <b>нет</b>",
    3: "<b>Не уверен</b>",
    4: "<b>Возможно</b>",
    5: "Скорее всего <b>да</b>",
    6: "Считаю, <b>да</b>",
    7: "<b>Точно да</b>",
}

symbs = (*string.ascii_lowercase, *string.digits, *"""ёйцукенгшщзхъфывапролджэячсмитьбю""",
         *"""ёйцукенгшщзхъфывапролджэячсмитьбю""".upper())

letters = dict((let, random.randint(1, 15)) for let in symbs)


def logs(usr: str, message: str, ans=False):
    if not os.path.exists(f"Users/{usr.chat.id}"):
        os.mkdir(f"Users/{usr.chat.id}")

    with open(f"Users/{usr.chat.id}/Logs.txt", "a+", encoding="UTF-8") as w:
        if ans:
            anss = "Ответ: "
        else:
            anss = ""

        message = f"{time.asctime()} - ({usr.from_user.username}) - {anss}{message}\n"
        w.write(message)


@bot.message_handler(commands=["start"])
def start(message):
    if not os.path.exists(f"Users/{message.chat.id}"):
        os.mkdir(f"Users/{message.chat.id}")

    logs(message, message.text)

    bot.send_message(message.chat.id, """
BestGuessing - Предсказатель
Просто задай вопрос и ответит да или нет.""")


@bot.message_handler(content_types=['text'])
def message_reply(message):
    logs(message, message.text)
    if message.text.endswith("?"):
        x = 0
        for let in message.text.lower():
            try:
                x += letters[let]
            except KeyError:
                ...

        if x == 0:
            chs = random.choice(["Что-то не так с вопросом", "Хммм... сложно", "Чё?", "И что это значит?"])

            logs(message, chs, ans=True)
            bot.send_message(message.chat.id, chs)
        else:
            ans = answers[x % len(answers)]

            logs(message, ans, ans=True)
            bot.send_message(message.chat.id, ans)
    else:
        chs_f = random.choice(["Это точно вопрос?", "Я не могу ответить на это, возможно это не вопрос",
                               "Это утверждение?", "И?"])

        logs(message, chs_f, ans=True)
        bot.send_message(message.chat.id, chs_f)


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
