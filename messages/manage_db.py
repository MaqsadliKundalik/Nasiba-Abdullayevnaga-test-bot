from aiogram import Router, F
from aiogram.types import Message, FSInputFile

router = Router()

@router.message(F.text == 'getdb')
async def send_db_backup(message: Message):
    if message.chat.id != 5165396993:
        return
    db_file = FSInputFile('db.sqlite3', filename='database_backup.sqlite')
    await message.answer_document(db_file, caption="Here is the database backup.")

@router.message(F.text == 'changedb')
async def receive_db_backup(message: Message):
    if message.chat.id != 5165396993:
        return
    if not message.document:
        await message.answer("Please send a document to update the database.")
        return
    document = message.document
    if document.file_name != 'db.sqlite3':
        await message.answer("Please send the correct database backup file named 'db.sqlite3'.")
        return
    file_path = await message.bot.get_file(document.file_id)
    await message.bot.download_file(file_path.file_path, 'db.sqlite3')
    await message.answer("Database has been updated successfully.")