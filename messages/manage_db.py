from aiogram import Router, F
from aiogram.types import Message, FSInputFile
import os

router = Router()

@router.message(F.text == 'getdb')
async def send_db_backup(message: Message):
    if message.from_user.id != 5165396993:
        await message.answer("❌ Sizda bu buyruqni bajarish huquqi yo'q!")
        return
    try:
        # Database faylining to'liq yo'li
        db_path = os.path.join(os.getcwd(), 'db.sqlite3')
        
        # Debugging uchun
        if not os.path.exists(db_path):
            await message.answer(f"❌ Database fayli topilmadi!\n📁 Izlangan yo'l: {db_path}\n📂 Joriy papka: {os.getcwd()}\n📋 Fayllar: {', '.join(os.listdir(os.getcwd())[:10])}")
            return
        
        db_file = FSInputFile(db_path, filename='db.sqlite3')
        await message.answer_document(db_file, caption="✅ Mana database backup fayli.")
    except FileNotFoundError:
        await message.answer("❌ Database fayli topilmadi. Iltimos, bot to'g'ri ishlayotganini tekshiring.")
    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {str(e)}")

@router.message(F.text == 'changedb')
async def receive_db_backup(message: Message):
    if message.from_user.id != 5165396993:
        await message.answer("❌ Sizda bu buyruqni bajarish huquqi yo'q!")
        return
    if not message.document:
        await message.answer("📎 Iltimos, database faylini hujjat sifatida yuboring.")
        return
    document = message.document
    if document.file_name != 'db.sqlite3':
        await message.answer("❌ Iltimos, to'g'ri 'db.sqlite3' nomli faylni yuboring.")
        return
    try:
        file_path = await message.bot.get_file(document.file_id)
        await message.bot.download_file(file_path.file_path, 'db.sqlite3')
        await message.answer("✅ Database muvaffaqiyatli yangilandi!")
    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {str(e)}")