import random
import string
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo
import json

bot = Bot('6825098020:AAF44cUD0rKqAApWbFyY-R7tvqmJ8wuMdyc')
dp = Dispatcher(bot)

async def send_data_to_chat(bot, data, chat_id):
    # Генеруємо рандомний номер замовлення
    order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    # Створюємо повідомлення з отриманими даними
    message_text = f"Номер замовлення: {order_number}\nПІБ: {data['name']}\nEmail: {data['email']}\nТелефон: {data['phone']}\nАдреса: {data['address']}\nКоментар до замовлення: {data['comment']}\nЗагальна сума до оплати: {data['total']} грн\nКниги: {', '.join(data['books'])}\nДякуємо за оформлення вашого замовлення✅"
    # Відправляємо повідомлення у вказаний чат
    await bot.send_message(chat_id, text=message_text)

@dp.message_handler(commands=['start', 'site'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Відкрити веб-сторінку', web_app=WebAppInfo(url='https://nikitashapovalovromanovich.github.io/webs/index3.html')))
    await message.answer("Привіт! Ми раді бачити Вас у нашому Веб-додатку! Натисніть на кнопку нижче, щоб відкрити веб-сторінку.", reply_markup=markup)

@dp.message_handler(content_types=['web_app_data'])
async def web_app(message: types.Message):
    res = json.loads(message.web_app_data['data'])
    # Відправляємо дані у чат (використовуйте додатній ідентифікатор чату)
    chat_id = -4118418632  
    await send_data_to_chat(bot, res, chat_id)
    await message.answer(f"ПІБ: {res['name']}\nEmail: {res['email']}\nТелефон: {res['phone']}\nАдреса: {res['address']}\nКоментар до замовлення: {res['comment']}\nЗагальна сума до оплати: {res['total']} грн\nКниги: {', '.join(res['books'])}\nДякуємо за оформлення вашого замовлення✅")

if __name__ == '__main__':
    executor.start_polling(dp)


