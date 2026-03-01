from dotenv import load_dotenv
import os
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
CHANNEL_URL = os.getenv("CHANNEL_URL")
ADMINS = os.getenv("ADMINS")
ADMINS = [int(admin.strip()) for admin in ADMINS.split(",")]

CMD_MSG = """
*BOT BILAN ISHLASH:*

<b>Test yechish uchun:</b>
<code>::test_kodi::javoblar</code> ko'rinishida yuboring.

<b>Namuna:</b> <code>::1001::abcd...</code> yoki <code>::1001::1a2b3c...</code>

<b>Test yaratish uchun:</b>
<code>//javoblar</code> ko'rinishida yuboring.

<b>Namuna:</b> <code>//1a2b3c4d5e</code>

<b>Testni yakunlash:</b>
<code>stop test_kodi</code>
"""