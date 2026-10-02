from __future__ import annotations
import asyncio
from aiogram import Bot,Dispatcher,F
from aiogram.filters import Command
from aiogram.types import Message
from ..configuration import load_config

def main(): asyncio.run(run())
async def run():
    cfg=load_config()
    if not cfg or not cfg.configured: raise RuntimeError('JARVIS is not configured. Run jarvis setup locally first.')
    if not cfg.telegram_bot_token: raise RuntimeError('Telegram bot token is missing. Run jarvis setup locally.')
    from ..agent.runtime import Runtime
    runtime=Runtime(cfg); bot=Bot(cfg.telegram_bot_token); dp=Dispatcher()
    def authorized(message): return bool(message.from_user and message.from_user.id in set(cfg.allowed_user_ids or []))
    @dp.message(Command('start'))
    async def start(message:Message):
        if not authorized(message): return await message.answer('⛔ Unauthorized. Ask the owner to add your Telegram user ID.')
        await message.answer('🤖 JARVIS online. Telegram is connected to the configured terminal agent.')
    @dp.message(F.contact)
    async def contact(message:Message):
        if not authorized(message): return await message.answer('⛔ Unauthorized.')
        c=message.contact; runtime.contacts.add(message.from_user.id,c.first_name,c.phone_number); await message.answer(f'Contact stored: {c.first_name}')
    @dp.message(F.text)
    async def text_message(message:Message):
        if not authorized(message): return await message.answer('⛔ Unauthorized.')
        try: await message.answer(await runtime.handle(message.from_user.id,message.text))
        except Exception as exc: await message.answer(f'⚠️ {type(exc).__name__}: {exc}')
    try: await dp.start_polling(bot)
    finally: await bot.session.close()
