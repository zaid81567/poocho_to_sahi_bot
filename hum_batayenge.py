import wikipedia
import telebot
import decouple

TOKEN_KEY = decouple.config('TOKEN_KEY')
bot = telebot.TeleBot(TOKEN_KEY)


@bot.message_handler(commands=['start','help'])
def start(message):
    bot.send_message(message.chat.id,'''
POOCHO TO SAHI

commands
➡ /start
➡ /creator
➡ /help

Search 
➡ Topic ex - 'India' then enter
    ''')


@bot.message_handler(func= lambda message: True)
def search(message):
    user_query = message.text

    # print(user_query)
    try:
        pages = wikipedia.search(user_query)
        # print(pages)
        try:
            first_page_obj = wikipedia.page(pages[0])
        except IndexError:
            bot.send_message(message.chat.id,'Check your spelling!')
            return
        # print(first_page_obj.title)
        search_summary = wikipedia.summary(first_page_obj.title,3)
        bot.send_message(message.chat.id,first_page_obj.images[0])
        bot.send_message(message.chat.id,f'{first_page_obj.title}\n\n{search_summary}')
        bot.clear_step_handler_by_chat_id(message)
        return
    except wikipedia.exceptions.PageError:
        bot.send_message(message.chat.id,'Error: Page not found.')
        return
    except wikipedia.exceptions.DisambiguationError:
        pages_list = list(filter(lambda page_title:page_title != message.text.title(),pages))
        # print(pages_list)
        suggestion_message = 'Add more keywords - Choose from below⬇\n'

        for x in range(0,len(pages_list)):
            suggestion_message +='\n' + pages_list[x]
        bot.send_message(message.chat.id,suggestion_message)
        return

try:
    bot.infinity_polling(timeout=10,long_polling_timeout=5)
except Exception as e:
    print(e)


