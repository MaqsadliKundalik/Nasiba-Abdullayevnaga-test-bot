from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from utils.models import User
from aiogram.fsm.context import FSMContext  
from filters import IsNewUser
from states import RegistrationStates
from config import CMD_MSG

router = Router()

@router.message(RegistrationStates.WAITING_FOR_NAME)    
async def process_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if len(name.split()) < 2:
        await message.answer("Iltimos, ism-familyangizni yuboring.")
        return

    await User.create(tg_id=message.from_user.id, name=name)
    await message.answer(f"Ro'yxatdan o'tganingiz uchun rahmat, {name}!")
    await message.answer(CMD_MSG, parse_mode="MARKDOWN")
    await state.clear()

@router.message(IsNewUser())
async def register_user(message: Message, state: FSMContext):
    await message.answer("Xush kelibsiz! Iltimos, ism-familyangizni kiriting.\n\nMaslan: Ali Valiyev")
    await state.set_state(RegistrationStates.WAITING_FOR_NAME)

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Nima qilamiz?")
