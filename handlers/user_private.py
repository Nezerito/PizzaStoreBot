from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command
from aiogram.utils.formatting import as_list, as_marked_section, Bold

from filters.chat_types import ChatTypeFilter
from kbs import reply
from kbs.reply import get_keyboard

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        "Привет, я виртуальный помощник",
        reply_markup=get_keyboard(
            "Меню",
            "О магазине",
            "Варианты оплаты",
            "Варианты доставки",
            placeholder="Что вас интересует?",
            sizes=(2, 2)
        ),
    )


@user_private_router.message(F.text.lower() == "меню")
@user_private_router.message(Command("menu"))
async def menu_cmd(message: types.Message):
    await message.answer("Вот меню:", reply_markup=reply.del_kb)


@user_private_router.message(F.text.lower() == "о нас")
@user_private_router.message(Command("about"))
async def about_cmd(message: types.Message):
    await message.answer("О нас:")


@user_private_router.message(F.text.lower() == "варианты оплаты")
@user_private_router.message(Command("payment"))
async def payment_cmd(message: types.Message):
    text = as_marked_section(
        Bold('Варианты оплаты:'),
        "Картой в боте",
        "При получении",
        "В заведении",
        marker='✅'
    )
    await message.answer(text.as_html())


@user_private_router.message((F.text.lower().contains('доставк')) | (F.text.lower() == 'варианты доставки'))
@user_private_router.message(Command("shipping"))
async def shipping_cmd(message: types.Message):
    text = as_list(as_marked_section(
        Bold('Варианты доставки:'),
        "Курьер",
        "Самовынос",
        "Поем в заведении",
        marker='✅'),
        as_marked_section(
            Bold('Запрещается:'),
            "Почта",
            "Голуби",
            marker='❌'
        ), sep='\n--------------------------------------------------\n')
    await message.answer(text.as_html())


@user_private_router.message(F.contact)
async def number_cmd(message: types.Message):
    await message.answer("Номер получен")
    await message.answer(str(message.contact))


@user_private_router.message(F.location)
async def location_cmd(message: types.Message):
    await message.answer("Локация получена")
    await message.answer(str(message.location))
