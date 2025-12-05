from aiogram import Router, F
from aiogram.types import Message
from utils.models import User, Tests, UserAnswers
from tortoise.exceptions import DoesNotExist
import re

router = Router()

def check_test_keys_format(test_key: str) -> bool:
    pattern = r'^(?:\d+[a-zA-Z])+$'
    return bool(re.fullmatch(pattern, test_key))

@router.message(F.text.startswith('new '))
async def manage_test(message: Message):
    test_keys = message.text.split()[1]
    user = await User.get(tg_id=message.from_user.id)
    if not check_test_keys_format(test_keys):
        await message.answer("Test kaliti noto'g'ri formatda. Iltimos, to'g'ri formatda kiriting (masalan: 1a2b3c...).")
        return

    test = await Tests.create(user=user, test_keys=test_keys)
    await message.answer(f"Yangi test yaratildi!\n\nTest kodi: `{test.id}`", parse_mode="MARKDOWN")

@router.message(F.text.startswith('stop '))
async def stop_test(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Buyruq noto‘g‘ri. Namuna: /stop_test <test_id>")
        return
    test_code = parts[1].strip()
    try:
        test_id = int(test_code)
    except ValueError:
        await message.answer("Test ID butun son bo‘lishi kerak.")
        return

    try:
        user = await User.get(tg_id=message.from_user.id)
    except DoesNotExist:
        await message.answer("Foydalanuvchi topilmadi.")
        return

    test = await Tests.filter(id=test_id, user=user).first()
    if not test:
        await message.answer("Sizda bunday test mavjud emas.")
        return
    if test.status == 'stopped':
        await message.answer("Bu test allaqachon to'xtatilgan.")
        return
    test.status = 'stopped'
    await test.save()
    top_answers = await (UserAnswers
                         .filter(test=test)
                         .select_related('user')
                         .order_by('-score', 'created_at')
                         .limit(30))

    if not top_answers:
        await message.answer("Bu testda hali natijalar yo‘q.")
        return

    lines = ["Natijalar:\n"]
    for idx, ans in enumerate(top_answers, 1):
        name = ans.user.name or f"ID:{ans.user.id}"
        time_spent = (ans.created_at - test.created_at).total_seconds()
        match idx:
            case 1:
                idx = "🥇"
            case 2:
                idx = "🥈"
            case 3:
                idx = "🥉"

        lines.append(f"{idx}. {name} - {ans.score} ta ({round(time_spent / 60, 1)} min)") 
    msg = "\n".join(lines)
    # jami nechta odam qatnashdi
    msg += f"\n\nJami qatnashganlar soni: {await UserAnswers.filter(test=test).count()}"
    await message.answer(msg[:4000])  

@router.message(F.text.startswith("edit "))
async def edit_test(message: Message):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        await message.answer("To'g'ri format: edit <test_id> <yangi_test_kaliti>\nMasalan: edit 123 1a2b3c10d")
        return

    _, test_code_raw, new_test_keys = parts
    try:
        test_id = int(test_code_raw)
    except ValueError:
        await message.answer("Test ID butun son bo'lishi kerak.")
        return

    try:
        user = await User.get(tg_id=message.from_user.id)
    except DoesNotExist:
        await message.answer("Foydalanuvchi topilmadi.")
        return

    test = await Tests.filter(id=test_id, user=user).first()
    if not test:
        await message.answer("Sizda bunday test mavjud emas.")
        return

    if not check_test_keys_format(new_test_keys):
        await message.answer("Yangi test kaliti noto'g'ri formatda. Iltimos, to'g'ri formatda kiriting (masalan: 1a2b3c...).")
        return

    test.test_keys = new_test_keys
    await test.save()
    await message.answer(f"Test kaliti muvaffaqiyatli yangilandi!")
    