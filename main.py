import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
import sys
from button import *
from state import *
from aiogram.fsm.context import FSMContext
from get_data import *
from aiogram.utils.keyboard import InlineKeyboardBuilder
TOKEN = "Token"
router = Router()

form_router = Router()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

@form_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    text = """🏡✨ Добро пожаловать в наш умный домашний бот! 🤖

▫️ Если вы клиент и хотите узнать больше о наших услугах, введите "/service"
▫️ Если вы специалист и хотите присоединиться к нашему сообществу, введите "/register"

Выберите один из вариантов, и мы начнем! 🚀"""
    await message.answer(text)
@form_router.message(Command('rules'))
async def command_rules(message: Message):
    text = """
1. Договоренность о стоимости услуги:
1.1. Все условия и стоимость предоставляемых услуг согласовываются между клиентом и специалистом (пользователем) бота.

2. Ответственность администрации:
2.1. Администрация телеграм-бота не несет ответственности за согласование, оформление или изменение условий договора между клиентом и специалистом.

3. Обязательства сторон:
3.1. Клиент и специалист несут ответственность за соблюдение всех условий, оговоренных в договоре между ними.

4. Решение споров:
4.1. Любые споры или недоразумения между клиентом и специалистом решаются исключительно между ними, без участия администрации телеграм-бота.

5. Конфиденциальность:
5.1. Администрация телеграм-бота не имеет доступа к деталям договора между клиентом и специалистом и не разглашает конфиденциальную информацию.
\n
Услуги: /service
    """

    await message.answer(text)

@form_router.message(Command('offers'))
async def command_offer(message: Message, state: FSMContext):
    first_name = message.from_user.first_name
    text = f"""
🚀 Дайте свои Идеи!

Привет, {first_name}!

Спасибо, что хотите внести свой вклад! Если у вас есть предложения, идеи или какие-то интересные предложения, пожалуйста, отправьте их нам. Мы ценим ваш вклад и стремимся сделать наш бот еще лучше!

Просто напишите свои идеи в чат, и мы обязательно рассмотрим их. Вместе мы делаем наш бот лучше для всех!

Спасибо за ваше участие,

Fixify🌟

    """
    await state.set_state(OfferState.text)
    await message.answer(text)

@form_router.message(OfferState.text)
async def get_offer_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.clear()
    send_offer_text(message.text)
    text = f"""
Спасибо за Вашу Идею, {message.from_user.first_name}!

Мы внимательно рассмотрим ваше предложение и постараемся внедрить его, чтобы сделать наше приложение более полезным и удобным для всех.

Благодарим за ваше активное участие,

Fixify🌟
\n
Услуги: /service
"""
    await message.answer(text)
@form_router.message(F.text == '/service')
async def komandi(message: Message, state: FSMContext):

    await bot.send_message(chat_id=message.chat.id, text="<b>Выберите район: </b>", reply_markup=builder.as_markup())
    await state.set_state(ServiceState.region)

@form_router.message(F.text == '/register')
async def registerFunc(message: Message, state: FSMContext):

    await message.answer("<b>Выберите район: </b>", reply_markup=builder.as_markup())
    await state.set_state(RegisterState.region)


@form_router.callback_query(RegisterState.region)
async def get_regionReg(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(region=callback.data)
    await bot.send_message(callback.from_user.id, text="<b>Выберите услугу: </b>", reply_markup=servicebutton.as_markup())
    await state.set_state(RegisterState.service)


@form_router.callback_query(RegisterState.service)
async def get_serviceReg(callback: types.CallbackQuery, state: FSMContext):
    data = await state.update_data(service=callback.data)
   
    await bot.send_message(callback.from_user.id, text="Введите имя: ")
    await state.set_state(RegisterState.first_name)

@form_router.message(RegisterState.first_name)
async def get_fname(message: Message,state: FSMContext):

    await state.update_data(first_name=message.text)
    await message.answer("Введите фамилия: ")
    await state.set_state(RegisterState.last_name)


@form_router.message(RegisterState.last_name)
async def get_lname(message: Message,state: FSMContext):

    await state.update_data(last_name=message.text)
    await message.answer("Сколько лет опыта у вас в данной области? ")
    await state.set_state(RegisterState.year_experence)


@form_router.message(RegisterState.year_experence)
async def get_year_experence(message: Message,state: FSMContext):

    await state.update_data(year_experence=message.text)
    await message.answer("Какие конкретные навыки у вас есть?")
    await state.set_state(RegisterState.skills)

@form_router.message(RegisterState.skills)
async def get_skills(message: Message,state: FSMContext):

    await state.update_data(skills=message.text)
    await message.answer("Каков ваш график работы и доступность?")
    await state.set_state(RegisterState.schedule)

@form_router.message(RegisterState.schedule)
async def get_schedule(message: Message,state: FSMContext):

    await state.update_data(schedule=message.text)
    await message.answer("Укажите ваши стандартные ставки или как определяются цены на ваши услуги.")
    await state.set_state(RegisterState.price)


@form_router.message(RegisterState.price)
async def get_price(message: Message,state: FSMContext):

    await state.update_data(price=message.text)
    await message.answer("Введите тел.номер: ")
    await state.set_state(RegisterState.phone_number)

@form_router.message(RegisterState.phone_number)
async def get_phone_number(message: Message,state: FSMContext):

    data = await state.update_data(phone_number=message.text)
    data['chat_id'] = message.from_user.id
    createapplicant(data)
    await state.clear()
    text = """📬 Спасибо за заполнение нашего опроса! Мы ценим ваш интерес к нашему сообществу.

🔄 Ваша заявка получена, и мы обязуемся рассмотреть ее в течение 24 часов. Наши эксперты свяжутся с вами по указанным контактным данным для дальнейшего обсуждения.

🤝 Благодарим за выбор нас, и мы с нетерпением ожидаем сотрудничества!"""
    await bot.send_message(message.from_user.id, text=text)    



@form_router.callback_query(ServiceState.region)
async def get_region(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(region=callback.data)
    await bot.send_message(callback.from_user.id, text="<b>Выберите услугу: </b>", reply_markup=servicebutton.as_markup())
    await state.set_state(ServiceState.sname)


@form_router.callback_query(ServiceState.sname)
async def get_service(callback: types.CallbackQuery, state:FSMContext):
    
    if callback.data == "addition":
        text_a = """
🔧 Приветствуем, специалист!

Не нашли свою область в списке? Расскажите нам, чем занимаетесь. Мы готовы рассмотреть новые возможности!

💬 Опишите свою деятельность, и мы постараемся внедрить её в наше сообщество.

Благодарим за ваш интерес! 🚀

        """
        await bot.send_message(callback.from_user.id, text=text_a)
        await state.set_state(AddService.text)

    else:
        data = await state.update_data(sname=callback.data)
        applicant_button = InlineKeyboardBuilder()

        if getApplicant(data):
            for i in getApplicant(data):
                answer = i['fedback']/i['quentity']
                if answer:
                    if 1 <= answer < 1.5:
                        applicant_button.add(types.InlineKeyboardButton(text=i['first_name']+" "+"⭐️", callback_data=str(i['id'])))
                    elif 1.5 <= answer < 2.5:
                        applicant_button.add(types.InlineKeyboardButton(text=i['first_name']+" "+"⭐️⭐️", callback_data=str(i['id'])))

                    elif 2.5 <= answer <=3:
                        applicant_button.add(types.InlineKeyboardButton(text=i['first_name']+" "+"⭐️⭐️⭐️", callback_data=str(i['id'])))
                    else:
                        applicant_button.add(types.InlineKeyboardButton(text=i['first_name']+" "+i['last_name'], callback_data=str(i['id'])))
                

                else:
                    applicant_button.add(types.InlineKeyboardButton(text=i['first_name']+" "+i['last_name'], callback_data=str(i['id'])))

            applicant_button.adjust(1)
            await bot.send_message(callback.from_user.id, text="Выберите специалист: ", reply_markup=applicant_button.as_markup())
            await state.set_state(ServiceState.applicant)

        else:
            await state.clear()
            await bot.send_message(callback.from_user.id, "Ничего не найдено!\n/service")

@form_router.message(AddService.text)
async def get_text_add_service(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.clear()
    addServicerequest(message.text)
    await message.answer("Спасибо для вашего ответа!\n/service")
@form_router.callback_query(ServiceState.applicant)
async def get_applicant(callback: types.CallbackQuery, state:FSMContext):
    text = getApplicantDetail(callback.data)
    data = await state.update_data(applicant=callback.data)

    await state.set_state(ServiceState.fedback)
    await bot.send_message(callback.from_user.id, text=text)
    await bot.send_message(callback.from_user.id, text="Оцените специалиста", reply_markup=fedbackBtn.as_markup())
@form_router.callback_query(ServiceState.fedback)
async def get_fedbackFunc(callback: types.CallbackQuery, state: FSMContext):
    data = await state.update_data(fedback=callback.data)
    fedbackView(data)
    await state.clear()
    await bot.send_message(callback.from_user.id, "Спасибо за выбор!\n/service")

async def main() -> None:
    
    dp = Dispatcher()
    dp.include_router(form_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())