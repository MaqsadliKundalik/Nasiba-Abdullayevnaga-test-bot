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

Test yechish uchun:
`test <test_kodi> 1a2b3c...`
`test <test_kodi> abcdef...`
`test <test_kodi> 1a,2b,...`
`test <test_kodi> a,b,c,...`

Test yaratish uchun:
`new <test_kodi>  1a2b3c...`

Testni yakunlash:
`stop <test_kodi>`
"""