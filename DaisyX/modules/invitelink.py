# Copyright (C) 2021 TeamDaisyX


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

from pyrogram import filters

from DaisyX.function.pluginhelpers import admins_only
from DaisyX.services.pyrogram import pbot

__HELP__ = """
Filter klasik sama seperti sistem filter marie. Jika Anda masih menyukai sistem filter semacam itu lakukan ini:
**Khusus Admin**
 - /cfilter <kata> <pesan>: Setiap kali seseorang mengatakan "kata", bot akan membalas dengan "pesan"
Anda juga dapat memasukkan button(tombol) dalam filter, misalnya kirim `/savefilter google` sebagai balasannya `Click Here To Open Google | [Button.url('Google', 'google.com')]`
 - /stopcfilter <filter>: Menghentikan filter tersebut.
 - /stopallcfilters: Menghapus semua filter dalam obrolan saat ini.
**Admin+Non-Admin**
 - /cfilters: Daftar semua filter aktif dalam obrolan
 
 **Harap dicatat filter klasik bisa tidak stabil. Kami menyarankan Anda untuk menggunakan /addfilter**
"""


@pbot.on_message(
    filters.command("invitelink") & ~filters.edited & ~filters.bot & ~filters.private
)
@admins_only
async def invitelink(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "Add me as admin of yor group first",
        )
        return
    await message.reply_text(f"Invite link generated successfully \n\n {invitelink}")


@pbot.on_message(filters.command("cfilterhelp") & ~filters.private & ~filters.edited)
@admins_only
async def filtersghelp(client, message):
    await client.send_message(message.chat.id, text=__HELP__)
