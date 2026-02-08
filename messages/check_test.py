import re
from aiogram import Router, F
from aiogram.types import Message
from tortoise.exceptions import DoesNotExist
from utils.models import User, Tests, UserAnswers

router = Router()

PAIR_RE = re.compile(r'\d+[a-zA-Z]')
LETTER_RE = re.compile(r'[a-zA-Z]')

def extract_key_letters(s: str) -> list[str]:
    s = s.replace(' ', '')
    pairs = PAIR_RE.findall(s)
    return [p[-1].lower() for p in pairs]

def extract_user_letters(s: str) -> list[str]:
    raw = s.replace(' ', '').replace(',', '')
    pairs = PAIR_RE.findall(raw)
    if pairs:
        return [p[-1].lower() for p in pairs]
    return [ch.lower() for ch in LETTER_RE.findall(raw)]

@router.message(F.text.startswith('test '))
async def check_test(message: Message):
    text = (message.text or '').strip()
    parts = text.split(maxsplit=2)
    if len(parts) < 3:
        await message.answer("To'g'ri format: test <test_kodi> <javoblar>\nMasalan: test 123 1a2b3c10d yoki test 123 abcd")
        return

    _, test_code_raw, user_answer_raw = parts
    try:
        test_id = int(test_code_raw)
    except ValueError:
        await message.answer("Test kodi butun son bo'lishi kerak.")
        return

    try:
        user = await User.get(tg_id=message.from_user.id)
    except DoesNotExist:
        await message.answer("Foydalanuvchi topilmadi.")
        return

    test = await Tests.filter(test_code=test_code_raw).first()
    if not test:
        await message.answer("Sizda bunday test mavjud emas.")
        return

    if await UserAnswers.filter(user=user, test=test).exists():
        await message.answer("Siz allaqachon bu testga javob bergansiz.")
        return

    key_letters = extract_key_letters(test.test_keys or '')
    user_letters = extract_user_letters(user_answer_raw or '')

    if not key_letters:
        await message.answer("Test kaliti noto'g'ri yoki bo'sh.")
        return
    if not user_letters:
        await message.answer("Javoblar topilmadi. Harflar yoki juftliklar ko'rinishida kiriting (masalan: abcd yoki 1a2b3c).")
        return

    total = len(key_letters)
    correct = 0
    results = []

    for idx in range(total):
        u = user_letters[idx] if idx < len(user_letters) else None
        k = key_letters[idx]
        ok = (u is not None) and (u == k)
        if ok:
            correct += 1
        label = f"{idx+1:02d} {(u or '-').upper()}"
        mark = "✅" if ok else "❌"
        results.append(f"{label} {mark}")

    cols = 3
    lines = ['   '.join(results[i:i+cols]) for i in range(0, len(results), cols)]
    result_table = '\n'.join(lines)

    await UserAnswers.create(user=user, test=test, score=correct)

    header = f"Sizning natijangiz: {correct}/{total}"
    body = f"{header}\n\n{result_table}"
    await message.answer(body[:4000])
