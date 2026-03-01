from aiogram import BaseMiddleware
from aiogram.types import Message, Update
from aiogram.enums import ChatMemberStatus
from aiogram.fsm.context import FSMContext
from utils.models import User
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import CHANNEL_ID, CHANNEL_URL


class CheckSub(BaseMiddleware):
    async def __call__(self, handler, event: Update, state: FSMContext):
        if event.message:
            message = event.message
            user = await User.get_or_none(tg_id=message.from_user.id)
            if not user:
                return
            channel_user = await message.bot.get_chat_member(CHANNEL_ID, message.from_user.id)
            if channel_user.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return await handler(event, state)
            else:
                inline_kb = InlineKeyboardBuilder()
                inline_kb.button(text="Kanalga o'tish", url=CHANNEL_URL)
                inline_kb.button(text="✅ Tekshirish", callback_data="check_sub")
                inline_kb.adjust(1)
                await message.answer("Botdan foydalanish uchun kanalimizga obuna bo'ling.", reply_markup=inline_kb.as_markup())
                return
        
        return await handler(event, state)