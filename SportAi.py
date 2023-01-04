from aiogram import Bot, Dispatcher, executor, types
import emoji
from aiogram.types import InlineKeyboardButton,  InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from loader import Start
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

#from aiogram.dispatcher.filters import Text


bot = Bot("5875286195:AAGs6qAQwmDTpBtyY6SPlxS9_bytHr8NEhM")
dp = Dispatcher(bot, storage=MemoryStorage())


#******Клавиатура 1********
kb = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
b1 = KeyboardButton("/help")
b2 = KeyboardButton("О спорт зале")
b3 = KeyboardButton("Записаться")
kb.add(b1,b2,b3)


@dp.message_handler(commands = ["start"])
async def start_command(message: types.Message):
    photo = open('F:/SportZalAiBot/data/SportZalphoto.jpg', 'rb')
    await bot.send_photo(chat_id=message.chat.id, photo = photo)
    await bot.send_message(chat_id = message.from_user.id,
                            text = emoji.emojize(":alien:")+ f"Приветствую, {message.from_user.first_name}. Добро пожаловать в спорт зал SportZalAi",
                            reply_markup=kb)
     
@dp.message_handler(commands = ["help"])
async def help_command(message: types.Message):
    mess = '''/start - начало работы с ботом
           /trainers - тренеры
           /help - помощь
           /record - записаться на тренировку'''
    await bot.send_message(chat_id = message.from_user.id,
                           text = mess)

@dp.message_handler(lambda message: message.text == "О спорт зале")
async def about_sport(message: types.Message):
     await message.reply("спортзал SportZalAi находится по адресу такому - то. Там есть такие -то тренажеры и разнве направления",
                         reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands = ["trainers"])
async def help_command(message: types.Message):
    mess = ""
    with open("F:/SportZalAiBot/data/AdminFile.txt", "r",encoding='utf-8') as file:
        mess = file.read()
    await bot.send_message(chat_id = message.from_user.id,
                           text = mess)
     

#******Машина состояний1***********
@dp.message_handler(commands = ['record'])
async def record_command (message: types.Message):
    await bot.send_message(chat_id = message.from_user.id,
                           text = "Мы рады, что вы захотели к нам записаться. Напишите свое имя")
    
    await Start.start_name.set()

@dp.message_handler(state=Start.start_name)
async def name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name1"] = message.text
        name = data["name1"]
        await bot.send_message(message.from_user.id,
                               text=f'Спасибо за ответ\nВас зовут: {name}, напишите свой номер телефона')
        
        await Start.start_number.set()

@dp.message_handler(state=Start.start_number)
async def number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number1'] = message.text
        number = data['number1']
        ikb = InlineKeyboardMarkup(row_width = 1)
        ib1 = InlineKeyboardButton(text='Стоп', callback_data ='stop')
        ikb.add(ib1)
        await bot.send_message(message.from_user.id,
                               text=f'Спасибо за ответ\nтвой номер: {number}, если все верно напишите любое слово, если нет просьба нажать на кнопку стоп, для того, чтобы начать вводить свои данные заново',
                               reply_markup=ikb)
        await Start.start_timetable.set()

        
@dp.callback_query_handler(text = 'stop', state=Start.start_timetable)
async def stop_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Нажмите /record, чтобы начать заново')
    await state.finish()


@dp.message_handler(state=Start.start_timetable)
async def timetable(message: types.Message, state: FSMContext):
     async with state.proxy() as data:
         mess = "Выберете подходящее рассписание"
         ikb = InlineKeyboardMarkup(row_width = 2)
         ib1 = InlineKeyboardButton(text='Групповые тренировки Вт/Чт 18.00', callback_data ='VT')
         ib2 = InlineKeyboardButton(text='Групповые тренровки Пн/Сб 8.00', callback_data ='PN')
         ikb.add(ib1,ib2)
         await bot.send_message(chat_id = message.from_user.id,
                               text = mess,
                               reply_markup=ikb)
             
         await Start.start_timetable_1.set()

@dp.callback_query_handler(text = 'VT', state=Start.start_timetable_1)
async def vt_callback(callback: types.CallbackQuery, state: FSMContext):
         async with state.proxy() as data:
             await callback.message.answer('Вы успешно записаны')
             await callback.answer('Вы успешно записаны')
             filePath = "F:/SportZalAiBot/data/RecordFile.txt"
             file = open(filePath,'a')
             file.write("************\n Имя:"+data['name1']+'\n')
             file.write('Номер:'+data['number1']+'\n')
             file.write('Расписание вт/чт\n')
             file.close()
             await state.finish()

            
@dp.callback_query_handler(text = 'PN', state=Start.start_timetable_1)
async def pn_callback(callback: types.CallbackQuery, state: FSMContext):
         async with state.proxy() as data:
             await callback.message.answer('Вы успешно записаны')
             await callback.answer('Вы успешно записаны')
             filePath = "F:/SportZalAiBot/data/RecordFile.txt"
             file = open(filePath,'a')
             file.write("************\n Имя:"+data['name1']+'\n')
             file.write('Номер:'+data['number1']+'\n')
             file.write('Расписание пн/сб\n')
             file.close()
             await state.finish()
    

if __name__ == "__main__":
    executor.start_polling(dispatcher = dp)
        
