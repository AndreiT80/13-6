# Домашнее задание по теме "Клавиатура кнопок". module_13_6.py

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio



api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text="Расчитать")
button2 = KeyboardButton(text="Информация")
kb.add(button)
kb.insert(button2)

kb1 = InlineKeyboardMarkup()
button3 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button4 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb1.add(button3)
kb1.insert(button4)

@dp.message_handler(commands=['start'])
async def start_message(message):
     await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text=["Расчитать"])
async def set_age(message):
    await message.answer("Выберите опцию:", reply_markup=kb1)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 x вес (кг) + 6,25 х рост (см) - 5 х возраст (г) - 5')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def get_age(call):
    await call.message.answer('Введите свой возраст')
    await UserState.age.set()
    await call.answer()

@dp.message_handler(state=UserState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_growth(message, state):
    await state.update_data(growth=message.text)
    data = await state.get_data()
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'Ваши калории {calories}')
    await state.finish()

@dp.message_handler(text=["Информация"])
async def inform(message):
    await message.answer("Информация о Боте")


@dp.message_handler()
async def all_message(message):
        await message.answer('Введите команду /start, чтобы начать общение.')




if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)











