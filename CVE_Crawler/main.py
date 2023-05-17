from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from texts import *
from finder import finder
from recent import find_recent_cve
from find_recent_in import find_recent_in
from last_activity import find_last_activity
from token import *
bot = Bot(token=Token_)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class CveForm(StatesGroup):
    cve = State()


class DaysForm(StatesGroup):
    day = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(start_text)


@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply(cancel)


@dp.message_handler(commands=['find'])
async def find_cve_start(message: types.Message):
    await message.answer(find_cve_text)
    await CveForm.cve.set()


@dp.message_handler(state=CveForm.cve)
async def find_cve_end(message: types.Message, state: FSMContext):
    text = message.text
    # noinspection PyBroadException
    try:
        cve_year, cve_id = text.split()
        cve_year = str(cve_year)
        cve_id = str(cve_id)
        await message.answer(finder(cve_year, cve_id))
        await state.finish()
    except Exception:
        await message.answer(cve_input_error)
        await state.finish()


@dp.message_handler(commands=['recent'])
async def recent_cve(message: types.Message):
    await message.answer(find_recent_cve())


@dp.message_handler(commands=['last_activity'])
async def last_activity(message: types.Message):
    await message.answer(find_last_activity())


@dp.message_handler(commands=['recent_in'])
async def find_recent_in_start(message: types.Message):
    await message.answer(find_recent_cve_in_text)
    await DaysForm.day.set()


@dp.message_handler(state=DaysForm.day)
async def find_recent_in_end(message: types.Message, state: FSMContext):
    text = message.text
    # noinspection PyBroadException
    try:
        days = int(text)
        r = find_recent_in(days)

        if len(r) > 4095:
            for char in range(0, len(r), 4095):
                await message.answer(r[char:char + 4095])
        else:
            await message.answer(r)

        await state.finish()
    except Exception as ex:
        print(ex)
        await message.answer(cve_input_error)
        await state.finish()


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(help_text)


@dp.message_handler()
async def not_understand(message: types.Message):
    await message.answer(not_understand_error)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
