import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from pizza_store.handlers.user_private import user_private_router
from pizza_store.handlers.user_group import user_group_router
from pizza_store.handlers.admin_private import admin_router
from pizza_store.common.bot_cmds_list import private

ALLOWED_UPDATES = ['message', 'edited_message']

bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
bot.my_admins_list = []
dp = Dispatcher()

dp.include_routers(user_private_router, user_group_router, admin_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())
