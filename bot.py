import telebot 
from telebot import types
from config import TOKEN
from parsing import get_articles , get_article_info , scrape_page, URL
from parsing_akipress import osnova , news , get_info 

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])

def welcome(message):
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton("24KG 📺")
    menu.add(b1)
    bot.send_message(message.chat.id, f"<b>Добро пожаловать {message.from_user.username}! Нажмите на сайт для просмотра новостей 👇 </b>" , parse_mode="html" ,reply_markup=menu)

@bot.message_handler(content_types=['text'])

def category(message):
    if message.chat.type == "private":
        if message.text == "24KG 📺":
            menu24 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            b1 = types.KeyboardButton("СПОРТ 🏋️‍♂️")
            b2 = types.KeyboardButton("ВЛАСТЬ 🕴")
            b3 = types.KeyboardButton("ЭКОНОМИКА  💰")
            menu24.add(b1,b2,b3)
            bot.send_message(message.chat.id , "<b>Теперь выберите категорию 👇</b>" , parse_mode="html" , reply_markup= menu24)
        elif message.text == "СПОРТ 🏋️‍♂️":
            page_url = URL + '/sport/'
            articles = scrape_page(page_url)
            articles_generator = get_articles(articles)
            message_generator = bot.send_message(message.chat.id, "<b>Загружаемся...</b>" , parse_mode='html')

            try:
                article = next(articles_generator)
                bot.delete_message(message.chat.id, message_generator.message_id) 
                send_article(message, article, articles_generator)
            except StopIteration:
                bot.delete_message(message.chat.id, message_generator.message_id)  
                bot.send_message(message.chat.id, '<b>Увы, на сегодня новостей больше нет</b>' , parse_mode='html')
        elif message.text == "ВЛАСТЬ 🕴":
            page_url = URL + '/vlast/'
            articles = scrape_page(page_url)
            articles_generator = get_articles(articles)
            message_generator = bot.send_message(message.chat.id, "<b>Загружаемся...</b>" , parse_mode='html')

            try:
                article = next(articles_generator)
                bot.delete_message(message.chat.id, message_generator.message_id) 
                send_article(message, article, articles_generator)
            except StopIteration:
                bot.delete_message(message.chat.id, message_generator.message_id)  
                bot.send_message(message.chat.id, '<b>Увы, на сегодня новостей больше нет</b>' , parse_mode='html')
        elif message.text == "ЭКОНОМИКА  💰":
            page_url = URL + '/ekonomika/'
            articles = scrape_page(page_url)
            articles_generator = get_articles(articles)
            message_generator = bot.send_message(message.chat.id, "<b>Загружаемся...</b>" , parse_mode='html')

            try:
                article = next(articles_generator)
                bot.delete_message(message.chat.id, message_generator.message_id) 
                send_article(message, article, articles_generator)
            except StopIteration:
                bot.delete_message(message.chat.id, message_generator.message_id)  
                bot.send_message(message.chat.id, '<b>Увы, на сегодня новостей больше нет</b>' , parse_mode='html')

def send_article(message, article, articles_generator):
    message_parts = []
    message_parts.append(f'Ссылка: {article["link"]}')
    text_parts = article["text"].split('\n')
    for part in text_parts:
        if len(part) <= 4096:
            message_parts.append(part)
        else:
            message_parts.extend(split_message(part))
    
    bot.send_message(message.chat.id, message_parts[0])
    
    for part in message_parts[1:]:
        bot.send_message(message.chat.id, part)
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_next = types.KeyboardButton('Далее')
    item_back = types.KeyboardButton('Назад к выбору раздела')
    markup.add(item_next, item_back)
    bot.send_message(message.chat.id, "<b>Дальше смотрим? Или устал?</b>",parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, handle_next_step, articles_generator)



def split_message(text, max_length=4096):
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

def handle_next_step(message, articles_generator):
    if message.text == 'Далее':
        try:
            article = next(articles_generator)
            send_article(message, article, articles_generator)
        except StopIteration:
            bot.send_message(message.chat.id, '<b>Увы, на сегодня новостей больше нет</b>' , parse_mode='html')
    elif message.text == 'Назад к выбору раздела':
        menu24 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = types.KeyboardButton("СПОРТ 🏋️‍♂️")
        b2 = types.KeyboardButton("ВЛАСТЬ 🕴")
        b3 = types.KeyboardButton("ЭКОНОМИКА  💰")
        menu24.add(b1,b2,b3)
        bot.send_message(message.chat.id , "<b>Как скажешь, идем выбирать раздел</b>" , parse_mode='html' , reply_markup=menu24)   
   

bot.polling(non_stop=True)



    


            
    



   

