from aiogram.filters import Filter
from utils.models import User

class IsNewUser(Filter):
    async def __call__(self, message) -> bool:
        user = await User.get_or_none(tg_id=message.from_user.id)
        return user is None