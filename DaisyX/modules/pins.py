# This file is part of Daisy (Telegram Bot)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from aiogram.utils.exceptions import BadRequest

from DaisyX import bot
from DaisyX.decorator import register

from .utils.connections import chat_connection
from .utils.language import get_strings_dec
from .utils.message import get_arg


@register(cmds="unpin", user_can_pin_messages=True, bot_can_pin_messages=True)
@chat_connection(admin=True)
@get_strings_dec("pins")
async def unpin_message(message, chat, strings):
    # support unpinning all
    if get_arg(message) in {"all"}:
        return await bot.unpin_all_chat_messages(chat["chat_id"])

    try:
        await bot.unpin_chat_message(chat["chat_id"])
    except BadRequest:
        await message.reply(strings["chat_not_modified_unpin"])
        return


@register(cmds="pin", user_can_pin_messages=True, bot_can_pin_messages=True)
@get_strings_dec("pins")
async def pin_message(message, strings):
    if "reply_to_message" not in message:
        await message.reply(strings["no_reply_msg"])
        return
    msg = message.reply_to_message.message_id
    arg = get_arg(message).lower()

    dnd = True
    loud = ["loud", "notify"]
    if arg in loud:
        dnd = False

    try:
        await bot.pin_chat_message(message.chat.id, msg, disable_notification=dnd)
    except BadRequest:
        await message.reply(strings["chat_not_modified_pin"])


__mod_name__ = "📌Pinning"

__help__ = """
Semua perintah terkait pin dapat ditemukan di sini; tetap perbarui obrolan Anda tentang berita terbaru dengan pesan yang disematkan secara sederhana!

<b> Basic Pins </b>
- /pin: secara diam-diam menyematkan pesan yang dibalas - tambahkan 'loud' atau 'notify' untuk memberikan pemberitahuan kepada pengguna.
- /unpin: melepas pin pesan yang saat ini disematkan - tambahkan 'all' untuk melepas pin semua pesan yang disematkan.

<b> Lainnya </b>
- /permapin [reply]: Sematkan pesan khusus melalui bot. Pesan ini dapat berisi markdown, button, dan semua fitur keren lainnya.
- /unpinall: Lepas pin semua pesan yang disematkan.
- /antichannelpin [yes/no/on/off]: Jangan biarkan telegram menyematkan chanel tertaut secara otomatis. Jika tidak ada argumen yang diberikan akan menunjukkan pengaturan saat ini.
- /cleanlinked [yes/no/on/off]: Hapus pesan yang dikirim oleh chanel tertaut.

Catatan: Saat menggunakan antichannelpin, pastikan untuk menggunakan perintah /unpin, daripada melakukannya secara manual. Jika tidak, pesan lama akan disematkan ulang saat chanel mengirim pesan apa pun.
"""
