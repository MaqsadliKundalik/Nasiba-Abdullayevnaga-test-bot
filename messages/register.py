from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message, KeyboardButton
from utils.models import User
from aiogram.fsm.context import FSMContext  
from filters import IsNewUser
from states import RegistrationStates
from config import CMD_MSG, CHANNEL_URL, CHANNEL_ID
from aiogram.enums import ChatMemberStatus
from aiogram.types import CallbackQuery

router = Router()


main_btn = ReplyKeyboardBuilder()
main_btn.button(text="✅ Javobni tekshirish")
main_btn.button(text="➕ Test yaratish")
main_btn.adjust(1)

@router.message(RegistrationStates.WAITING_FOR_NAME)    
async def process_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if len(name.split()) < 2:
        await message.answer("Iltimos, ism-familyangizni yuboring.")
        return

    await User.create(tg_id=message.from_user.id, name=name)
    await message.answer(f"Ro'yxatdan o'tganingiz uchun rahmat, {name}!", reply_markup=main_btn.as_markup(resize_keyboard=True))
    await state.clear()

@router.message(IsNewUser())
async def register_user(message: Message, state: FSMContext):
    await message.answer("Xush kelibsiz! Iltimos, ism-familyangizni kiriting.\n\nMaslan: Ali Valiyev")
    await state.set_state(RegistrationStates.WAITING_FOR_NAME)

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Nima qilamiz?", parse_mode="HTML", reply_markup=main_btn.as_markup(resize_keyboard=True))

@router.message(F.text == "➕ Test yaratish")
async def cmd_create_test(message: Message):
    await message.answer("""
<b>Test yaratish uchun:</b>
<code>//javoblar</code> ko'rinishida yuboring.

<b>Namuna:</b> <code>//1a2b3c4d5e</code>
""", parse_mode="HTML")

@router.message(F.text == "✅ Javobni tekshirish")
async def cmd_check_answer(message: Message):
    await message.answer("""
<b>Testni tekshirish uchun:</b>
<code>::test_kodi::javoblar</code> ko'rinishida yuboring.

<b>Namuna:</b> <code>::1001::abcd...</code> yoki <code>::1001::1a2b3c...</code>
""", parse_mode="HTML")

@router.callback_query(F.data == "check_sub")
async def check_sub(callback: CallbackQuery):
    channel_user = await callback.bot.get_chat_member(CHANNEL_ID, callback.from_user.id)
    if channel_user.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        await callback.message.edit_text("Obuna bo'lganingiz uchun raxmat", reply_markup=main_btn.as_markup(resize_keyboard=True))
    else:
        await callback.answer("Botdan foydalanish uchun kanalimizga obuna bo'ling.", show_alert=True)
