from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
import requests
builder = InlineKeyboardBuilder()
get_region = requests.get('http://crudsystem0124.pythonanywhere.com/')
get_service = requests.get('http://crudsystem0124.pythonanywhere.com/getService')


for i in get_region.json():
    builder.add(types.InlineKeyboardButton(
        text=i['name'],
        callback_data=str(i['id'])
    ))

builder.adjust(3)

servicebutton = InlineKeyboardBuilder()

for i in get_service.json():

    servicebutton.add(types.InlineKeyboardButton(text=i['name'], callback_data=str(i['id'])))
servicebutton.add(types.InlineKeyboardButton(text="Дополнительные Услуги", callback_data="addition"))
servicebutton.adjust(2)
applicant_button = InlineKeyboardBuilder()

fedbackBtn = InlineKeyboardBuilder()

a1 = types.InlineKeyboardButton(text="⭐️⭐️⭐️", callback_data="3")
a2 = types.InlineKeyboardButton(text="⭐️⭐️", callback_data="2")
a3 = types.InlineKeyboardButton(text="⭐️", callback_data="1")

fedbackBtn.add(a1, a2, a3)
fedbackBtn.adjust(1)


