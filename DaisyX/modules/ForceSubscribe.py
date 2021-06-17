#    Copyright (C) 2020-2021 by @InukaAsith
#    This programme is a part of Daisy TG bot project
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


import logging
import time

from pyrogram import filters
from pyrogram.errors import RPCError
from pyrogram.errors.exceptions.bad_request_400 import (
    ChannelPrivate,
    ChatAdminRequired,
    PeerIdInvalid,
    UsernameNotOccupied,
    UserNotParticipant,
)
from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup

from DaisyX import BOT_ID

# from DaisyX import OWNER_ID as SUDO_USERS
from DaisyX.services.pyrogram import pbot
from DaisyX.services.sql import forceSubscribe_sql as sql

logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(
    lambda _, __, query: query.data == "onUnMuteRequest"
)


@pbot.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, cb):
    try:
        user_id = cb.from_user.id
        chat_id = cb.message.chat.id
    except:
        return
    chat_db = sql.fs_settings(chat_id)
    if chat_db:
        channel = chat_db.channel
        try:
            chat_member = client.get_chat_member(chat_id, user_id)
        except:
            return
        if chat_member.restricted_by:
            if chat_member.restricted_by.id == BOT_ID:
                try:
                    client.get_chat_member(channel, user_id)
                    client.unban_chat_member(chat_id, user_id)
                    cb.message.delete()
                    # if cb.message.reply_to_message.from_user.id == user_id:
                    # cb.message.delete()
                except UserNotParticipant:
                    client.answer_callback_query(
                        cb.id,
                        text=f"❗ Bergabunglah dengan kami di chanel @{channel} dan tekan tombol 'UnMute Me'.",
                        show_alert=True,
                    )
                except ChannelPrivate:
                    client.unban_chat_member(chat_id, user_id)
                    cb.message.delete()

            else:
                client.answer_callback_query(
                    cb.id,
                    text="❗ Anda telah dibisukan oleh admin karena beberapa alasan lain.",
                    show_alert=True,
                )
        else:
            if not client.get_chat_member(chat_id, BOT_ID).status == "administrator":
                client.send_message(
                    chat_id,
                    f"❗ **{cb.from_user.mention} sedang mencoba untuk unmute sendiri tetapi saya tidak dapat mengaktifkannya karena saya bukan admin dalam obrolan ini, tambahkan saya sebagai admin lagi.**\n__#Leaving this chat...__",
                )

            else:
                client.answer_callback_query(
                    cb.id,
                    text="❗ Peringatan! Jangan tekan tombol ini saat Anda tidak di mute.",
                    show_alert=True,
                )


@pbot.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
    chat_id = message.chat.id
    chat_db = sql.fs_settings(chat_id)
    if chat_db:
        try:
            user_id = message.from_user.id
        except:
            return
        try:
            if (
                not client.get_chat_member(chat_id, user_id).status
                in ("administrator", "creator")
                and not user_id == 1141839926
            ):
                channel = chat_db.channel
                try:
                    client.get_chat_member(channel, user_id)
                except UserNotParticipant:
                    try:
                        sent_message = message.reply_text(
                            "Welcome {} 🙏 \n **Anda belum bergabung dengan kami di chanel @{} sekarang**❕ \n \nTolong ikuti kami di [channel](https://t.me/{}) dan tekan tombol **UNMUTE ME**. \n \n ".format(
                                message.from_user.mention, channel, channel
                            ),
                            disable_web_page_preview=True,
                            reply_markup=InlineKeyboardMarkup(
                                [
                                    [
                                        InlineKeyboardButton(
                                            "Join Channel",
                                            url="https://t.me/{}".format(channel),
                                        )
                                    ],
                                    [
                                        InlineKeyboardButton(
                                            "UnMute Me", callback_data="onUnMuteRequest"
                                        )
                                    ],
                                ]
                            ),
                        )
                        client.restrict_chat_member(
                            chat_id, user_id, ChatPermissions(can_send_messages=False)
                        )
                    except ChatAdminRequired:
                        sent_message.edit(
                            "❗ **Saya bukan admin disini..**\n__Beri saya izin ban dan coba lagi.. \n#Ending FSub...__"
                        )
                    except RPCError:
                        return

                except ChatAdminRequired:
                    client.send_message(
                        chat_id,
                        text=f"❗ **Saya bukan admin di chanel @{channel}.**\n__Beri saya admin chanel itu dan coba lagi.\n#Ending FSub...__",
                    )
                except ChannelPrivate:
                    return
        except:
            return


@pbot.on_message(filters.command(["forcesubscribe", "forcesub"]) & ~filters.private)
def config(client, message):
    user = client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status is "creator" or user.user.id == 1141839926:
        chat_id = message.chat.id
        if len(message.command) > 1:
            input_str = message.command[1]
            input_str = input_str.replace("@", "")
            if input_str.lower() in ("off", "no", "disable"):
                sql.disapprove(chat_id)
                message.reply_text("❌ **Force subscribe Berhasil Dinonaktifkan.**")
            elif input_str.lower() in ("clear"):
                sent_message = message.reply_text(
                    "**Unmuting all members who are muted by me...**"
                )
                try:
                    for chat_member in client.get_chat_members(
                        message.chat.id, filter="restricted"
                    ):
                        if chat_member.restricted_by.id == BOT_ID:
                            client.unban_chat_member(chat_id, chat_member.user.id)
                            time.sleep(1)
                    sent_message.edit("✅ **Membunyikan semua anggota yang dibisukan oleh saya.**")
                except ChatAdminRequired:
                    sent_message.edit(
                        "❗ **Saya bukan admin di Grup ini.**\n__Saya tidak dapat unmute anggota karena saya bukan admin dalam obrolan ini, jadikan saya admin dengan izin ban pengguna.__"
                    )
            else:
                try:
                    client.get_chat_member(input_str, "me")
                    sql.add_channel(chat_id, input_str)
                    message.reply_text(
                        f"✅ **Force Subscribe Diaktifkan**\n__Force Subscribe diaktifkan, semua anggota grup harus berlangganan [channel](https://t.me/{input_str}) untuk mengirim pesan di grup ini.__",
                        disable_web_page_preview=True,
                    )
                except UserNotParticipant:
                    message.reply_text(
                        f"❗ **Bukan Admin di Chanel**\n__Saya bukan admin di [channel](https://t.me/{input_str}). Tambahkan saya sebagai admin untuk mengaktifkan ForceSubscribe.__",
                        disable_web_page_preview=True,
                    )
                except (UsernameNotOccupied, PeerIdInvalid):
                    message.reply_text(f"❗ **Username chanel tidak valid.**")
                except Exception as err:
                    message.reply_text(f"❗ **ERROR:** ```{err}```")
        else:
            if sql.fs_settings(chat_id):
                message.reply_text(
                    f"✅ **Force Subscribe is enabled in this chat.**\n__For this [Channel](https://t.me/{sql.fs_settings(chat_id).channel})__",
                    disable_web_page_preview=True,
                )
            else:
                message.reply_text("❌ **Force Subscribe dinonaktifkan dalam obrolan ini.**")
    else:
        message.reply_text(
            "❗ **Diperlukan Pembuat Grup**\n__Anda harus menjadi pembuat grup untuk melakukan itu.__"
        )


__help__ = """
<b>ForceSubscribe:</b>
- Bot akan membisukan anggota yang tidak berlangganan chanel Anda sampai mereka berlangganan
- Saat diaktifkan, saya akan membisukan anggota yang tidak berlangganan dan menunjukkan kepada mereka tombol suarakan(unmute). Ketika mereka menekan tombol, baru saya akan membunyikan mereka
<b>Setup</b>
1) Pertama-tama tambahkan saya di grup sebagai admin dengan izin larangan pengguna dan di chanel sebagai admin.
Catatan: Hanya pembuat grup yang dapat mengatur saya dan saya tidak akan mengizinkan paksa berlangganan lagi jika tidak melakukannya.
 
<b>Commmands</b>
 - /forcesubscribe - Untuk mendapatkan pengaturan saat ini.
 - /forcesubscribe no/off/disable - Untuk mematikan ForceSubscribe.
 - /forcesubscribe {channel username} - Untuk mengaktifkan dan mengatur chanel.
 - /forcesubscribe clear - Untuk membunyikan semua anggota yang dibisukan oleh saya.
Catatan: /forcesub adalah alias dari /forcesubscribe
 
"""
__mod_name__ = "Force Subs🔔 "
