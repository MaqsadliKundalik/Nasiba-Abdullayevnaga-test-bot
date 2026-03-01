from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.enums import ChatMemberStatus
from aiogram.fsm.context import FSMContext
from utils.models import User
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import CHANNEL_ID, CHANNEL_URL


class CheckSub(BaseMiddleware):
    async def __call__(self, handler, event: Message, state: FSMContext):
        user = await User.get_or_none(tg_id=event.from_user.id)
        if not user:
            return
        channel_user = await event.bot.get_chat_member(CHANNEL_ID, event.from_user.id)
        if channel_user.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            await handler(event, state)
        else:
            inline_kb = InlineKeyboardBuilder()
            inline_kb.button(text="Kanalga o'tish", url=CHANNEL_URL)
            inline_kb.button(text="✅ Tekshirish", callback_data="check_sub")
            inline_kb.adjust(1)
            await event.answer("Botdan foydalanish uchun kanalimizga obuna bo'ling.", reply_markup=inline_kb.as_markup())
