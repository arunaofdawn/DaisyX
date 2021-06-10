"""
MIT License
Copyright (c) 2021 TheHamkerCat
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import os

from pyrogram import filters

from DaisyX.function.pluginhelpers import member_permissions
from DaisyX.services.pyrogram import pbot as app


@app.on_message(filters.command("setgrouptitle") & ~filters.private)
async def set_chat_title(_, message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        permissions = await member_permissions(chat_id, user_id)
        if "can_change_info" not in permissions:
            await message.reply_text("You Don't Have Enough Permissions.")
            return
        if len(message.command) < 2:
            await message.reply_text("**Usage:**\n/set_chat_title NEW NAME")
            return
        old_title = message.chat.title
        new_title = message.text.split(None, 1)[1]
        await message.chat.set_title(new_title)
        await message.reply_text(
            f"Successfully Changed Group Title From {old_title} To {new_title}"
        )
    except Exception as e:
        print(e)
        await message.reply_text(e)


@app.on_message(filters.command("settitle") & ~filters.private)
async def set_user_title(_, message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        from_user = message.reply_to_message.from_user
        permissions = await member_permissions(chat_id, user_id)
        if "can_change_info" not in permissions:
            await message.reply_text("You Don't Have Enough Permissions.")
            return
        if len(message.command) < 2:
            await message.reply_text(
                "**Usage:**\n/set_user_title NEW ADMINISTRATOR TITLE"
            )
            return
        title = message.text.split(None, 1)[1]
        await app.set_administrator_title(chat_id, from_user.id, title)
        await message.reply_text(
            f"Successfully Changed {from_user.mention}'s Admin Title To {title}"
        )
    except Exception as e:
        print(e)
        await message.reply_text(e)


@app.on_message(filters.command("setgrouppic") & ~filters.private)
async def set_chat_photo(_, message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id

        permissions = await member_permissions(chat_id, user_id)
        if "can_change_info" not in permissions:
            await message.reply_text("You Don't Have Enough Permissions.")
            return
        if not message.reply_to_message:
            await message.reply_text("Reply to a photo to set it as chat_photo")
            return
        if not message.reply_to_message.photo and not message.reply_to_message.document:
            await message.reply_text("Reply to a photo to set it as chat_photo")
            return
        photo = await message.reply_to_message.download()
        await message.chat.set_photo(photo)
        await message.reply_text("Successfully Changed Group Photo")
        os.remove(photo)
    except Exception as e:
        print(e)
        await message.reply_text(e)


__mod_name__ = "Admin"

__help__ = """
Make it easy to admins for manage users and groups with the admin module!

<b>Available commands:</b>

<b> Admin List </b>
- /adminlist: Menampilkan semua admin obrolan.*
- /admincache: Perbarui cache admin, untuk memperhitungkan izin admins/admin baru.*

<b> Mutes </b>
- /mute: bisukan pengguna
- /unmute: bunyikan pengguna
- /tmute [waktu] : membisukan sementara pengguna untuk interval waktu
- /unmuteall: Bunyikan semua anggota yang dibisukan

<b> Bans & Kicks </b>
- /ban: ban/larang pengguna
- /tban [waktu] : ban sementara pengguna untuk interval waktu.
- /unban: membatalkan pemblokiran pengguna
- /unbanall: Buka blokir semua anggota yang diblokir
- /banme: Melarang Anda dari grup
- /kick: menendang pengguna dari grup
- /kickme: Mengeluarkanmu dari grup

<b> Promotes & Demotes</b>
- /promote (user) (title admin): Mempromosikan pengguna menjadi admin.*
- /demote (user): Menurunkan jabatan pengguna dari admin.*
- /lowpromote: Promosikan anggota dengan hak rendah*
- /midpromote: Promosikan anggota dengan hak menengah*
- /highpromote: Promosikan anggota dengan hak maksimal*
- /lowdemote: Turunkan admin ke izin rendah*
- /middemote: Turunkan admin ke izin pertengahan*

<b> Cleaner/Purges </b>
- /purge: menghapus semua pesan dari pesan yang Anda balas
- /del: menghapus pesan yang dibalas
- /zombies: menghitung jumlah akun yang dihapus di grup Anda
- /kickthefools: Keluarkan anggota yang tidak aktif dari grup(selama satu minggu)

<b> User Info </b>
- /info: Dapatkan info pengguna
- /users: Dapatkan daftar pengguna grup
- /spwinfo : Periksa info spam pengguna dari layanan perlindungan Spam intellivoid
- /whois : Memberikan info pengguna seperti pyrogram

<b> Other </b>
- /invitelink: Dapatkan tautan undangan obrolan grup
- /settitle [entity] [title]: menetapkan judul khusus untuk admin. Jika tidak ada [judul] yang diberikan, maka secara default ke "Admin"
- /setgrouptitle [teks] tentukan judul grup group
- /setgrouppic: balas/reply gambar untuk ditetapkan sebagai foto grup
- /setdescription: Menetapkan deskripsi grup
- /setsticker: Setel stiker grup

*catatan:
Terkadang, Anda mempromosikan atau menurunkan seorang admin secara manual, dan Bot tidak segera menyadarinya. Ini karena untuk menghindari spamming server telegram, status admin di-cache secara lokal.
Ini berarti Anda terkadang harus menunggu beberapa menit untuk memperbarui hak admin. Jika Anda ingin segera memperbaruinya, Anda dapat menggunakan perintah `/admincache`; itu akan memaksa Bot untuk memeriksa siapa admin lagi.
"""
