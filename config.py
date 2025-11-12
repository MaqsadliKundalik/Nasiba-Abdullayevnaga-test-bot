from dotenv import load_dotenv
import os
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN = int(os.getenv("ADMIN"))

CMD_MSG = """
*BOT BILAN ISHLASH:*

Test yechish uchun:
`test <test_kodi> 1a2b3c...`
`test <test_kodi> abcdef...`
`test <test_kodi> 1a,2b,...`
`test <test_kodi> a,b,c,...`

Test yaratish uchun:
`new 1a2b3c...`

Testni to'xtatib, natijani olish uchun:
`stop <test_kodi>`
"""