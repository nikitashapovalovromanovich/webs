import random  
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo
import json

bot = Bot('6825098020:AAF44cUD0rKqAApWbFyY-R7tvqmJ8wuMdyc')
dp = Dispatcher(bot)

async def send_data_to_chat(bot, data, chat_id, order_number, total):  
    message_text = f"Номер замовлення: {order_number}\nПІБ: {data['name']}\nEmail: {data['email']}\nТелефон: {data['phone']}\nАдреса: {data['address']}\nКоментар до замовлення: {data['comment']}\n{data['bookname']}\n{data['ordertotal']}\nДякуємо за оформлення вашого замовлення✅"
    await bot.send_message(chat_id, text=message_text)

# Функція для генерації рандомного номера замовлення
def generate_order_number():
    return random.randint(1000, 9999)

@dp.message_handler(commands=['start', 'site'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Відкрити веб-сторінку', web_app=WebAppInfo(url='https://nikitashapovalovromanovich.github.io/webs/index3.html')))
    markup.add(types.KeyboardButton("Зв'язатись з менеджером"))
    await message.answer("Привіт! Ми раді бачити Вас у нашому Веб-додатку! Натисніть на кнопку нижче, щоб відкрити веб-сторінку.", reply_markup=markup)


@dp.message_handler(lambda message: message.text == "Зв'язатись з менеджером")
async def connect_manager(message: types.Message):
    # Отримати інформацію про користувача
    user_info = f"Ім'я: {message.from_user.full_name}\nID: {message.from_user.id}\nUsername: @{message.from_user.username}\n"
    
    # Додати інформацію про користувача до повідомлення для менеджера
    forward_text = f"Користувач бажає зв'язатись з менеджером. Інформація про користувача:\n{user_info}\nПовідомлення: {message.text}"
    
    # Відправити повідомлення в чат менеджера
    manager_chat_id = -1002143349178  
    await bot.forward_message(manager_chat_id, message.chat.id, message.message_id)
    
    # Повідомити користувача про те, що інформація була надіслана
    await message.answer("Ваше повідомлення було надіслано менеджеру. Він зв'яжеться з вами найближчим часом.")


@dp.message_handler(content_types=['web_app_data'])
async def web_app(message: types.Message):
    res = json.loads(message.web_app_data['data'])
    total = res.get('total')  # Отримуємо значення total
    chat_id = -1002143349178  
    order_number = generate_order_number()  # Генеруємо рандомний номер замовлення
    await send_data_to_chat(bot, res, chat_id, order_number, total)  # Передаємо total у функцію
    await message.answer(f"Номер замовлення: {order_number}\nПІБ: {res['name']}\nEmail: {res['email']}\nТелефон: {res['phone']}\nАдреса: {res['address']}\nКоментар до замовлення: {res['comment']}\n{res['bookname']}\n{res['ordertotal']}\nДякуємо за оформлення вашого замовлення✅")


if __name__ == '__main__':
    executor.start_polling(dp)
