#!/usr/bin/python
"""telegram bot to send a words from dictionary"""

import sys
import json

import telegram
from telegram.ext import Updater, CommandHandler
import psycopg2
import psycopg2.extras

with open('config.json', 'r') as f:
    config = json.load(f)

pg = config['db']['pg_conn']
tg_bot = config['telegram_bot']

if not all(k in pg for k in ('host', 'port', 'dbname', 'user', 'pass')):
    print('err: all pg connect options must be specified')
    sys.exit(1)

# connect to postgres
conn = psycopg2.connect(
    "host=%s port=%s dbname=%s user=%s password=%s"
    % (pg['host'], pg['port'], pg['dbname'], pg['user'], pg['pass']),
    cursor_factory=psycopg2.extras.DictCursor)


if 'token' not in tg_bot:
    print('err: telegram TOKEN must be specified')
    sys.exit(1)


def start(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat_id,
        text="Hi, %s!" % update.message.from_user.first_name
    )


def word(bot, update):
    try:
        cur = conn.cursor()
        cur.execute("""
            select vocab word, def || def_w_exam definition
            from v_dictionary
            offset random() * (select count(*) from v_dictionary)
            limit 1
                    """)
        word_row = cur.fetchone()

        bot.sendMessage(
            chat_id=update.message.chat_id,
            text='*%s* - %s' % (word_row['word'], word_row['definition']),
            parse_mode=telegram.ParseMode.MARKDOWN
        )
        cur.close()
    except:
        print('error: ', sys.exc_info()[0])
        sys.exit(1)


updater = Updater(token=tg_bot['token'])
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.addHandler(start_handler)

word_handler = CommandHandler('word', word)
dispatcher.addHandler(word_handler)

updater.start_polling()
