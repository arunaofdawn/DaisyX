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


import html

import tldextract
from telethon import events, types
from telethon.tl import functions

import DaisyX.services.sql.urlblacklist_sql as urlsql
from DaisyX.services.events import register
from DaisyX.services.telethon import tbot


async def can_change_info(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.change_info
    )


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerUser):
        return True


@register(pattern="^/addurl")
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if event.is_group:
        if await can_change_info(message=event):
            pass
        else:
            return
    chat = event.chat
    urls = event.text.split(None, 1)
    if len(urls) > 1:
        urls = urls[1]
        to_blacklist = list({uri.strip() for uri in urls.split("\n") if uri.strip()})
        blacklisted = []

        for uri in to_blacklist:
            extract_url = tldextract.extract(uri)
            if extract_url.domain and extract_url.suffix:
                blacklisted.append(extract_url.domain + "." + extract_url.suffix)
                urlsql.blacklist_url(
                    chat.id, extract_url.domain + "." + extract_url.suffix
                )

        if len(to_blacklist) == 1:
            extract_url = tldextract.extract(to_blacklist[0])
            if extract_url.domain and extract_url.suffix:
                await event.reply(
                    "Menambahkan <code>{}</code> domain ke blacklist!".format(
                        html.escape(extract_url.domain + "." + extract_url.suffix)
                    ),
                    parse_mode="html",
                )
            else:
                await event.reply("Anda mencoba memasukkan url yang tidak valid ke daftar hitam")
        else:
            await event.reply(
                "Menambahkan <code>{}</code> domain ke blacklist.".format(
                    len(blacklisted)
                ),
                parse_mode="html",
            )
    else:
        await event.reply("Beri tahu saya url mana yang ingin Anda tambahkan ke blacklist.")


@register(pattern="^/delurl")
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if event.is_group:
        if await can_change_info(message=event):
            pass
        else:
            return
    chat = event.chat
    urls = event.text.split(None, 1)

    if len(urls) > 1:
        urls = urls[1]
        to_unblacklist = list({uri.strip() for uri in urls.split("\n") if uri.strip()})
        unblacklisted = 0
        for uri in to_unblacklist:
            extract_url = tldextract.extract(uri)
            success = urlsql.rm_url_from_blacklist(
                chat.id, extract_url.domain + "." + extract_url.suffix
            )
            if success:
                unblacklisted += 1

        if len(to_unblacklist) == 1:
            if unblacklisted:
                await event.reply(
                    "Removed <code>{}</code> from the blacklist!".format(
                        html.escape(to_unblacklist[0])
                    ),
                    parse_mode="html",
                )
            else:
                await event.reply("This isn't a blacklisted domain...!")
        elif unblacklisted == len(to_unblacklist):
            await event.reply(
                "Menghapus <code>{}</code> domain dari blacklist.".format(
                    unblacklisted
                ),
                parse_mode="html",
            )
        elif not unblacklisted:
            await event.reply("Tak satu pun dari domain ini ada, jadi mereka tidak dihapus.")
        else:
            await event.reply(
                "Menghapus <code>{}</code> domains dari blacklist. {} tidak ada, jadi tidak dihapus.".format(
                    unblacklisted, len(to_unblacklist) - unblacklisted
                ),
                parse_mode="html",
            )
    else:
        await event.reply(
            "Beri tahu saya domain mana yang ingin Anda hapus dari daftar hitam."
        )


@tbot.on(events.NewMessage(incoming=True))
async def on_url_message(event):
    if event.is_private:
        return
    chat = event.chat
    extracted_domains = []
    for (ent, txt) in event.get_entities_text():
        if ent.offset != 0:
            break
        if isinstance(ent, types.MessageEntityUrl):
            url = txt
            extract_url = tldextract.extract(url)
            extracted_domains.append(extract_url.domain + "." + extract_url.suffix)
    for url in urlsql.get_blacklisted_urls(chat.id):
        if url in extracted_domains:
            try:
                await event.delete()
            except:
                return


@register(pattern="^/geturl$")
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if event.is_group:
        if await can_change_info(message=event):
            pass
        else:
            return
    chat = event.chat
    base_string = "Current <b>blacklisted</b> domains:\n"
    blacklisted = urlsql.get_blacklisted_urls(chat.id)
    if not blacklisted:
        await event.reply("Tidak ada domain yang masuk blacklist di sini!")
        return
    for domain in blacklisted:
        base_string += "- <code>{}</code>\n".format(domain)
    await event.reply(base_string, parse_mode="html")


__help__ = """
<b> Blacklist/daftar hitam</b>
 - /addfilter [kata pemicu] Pilih kata pemicunya
 - /delfilter [kata pemicu] : berhenti/menghapus kata pemicu pada blacklist
 - /filters: daftar semua filter dalam blacklist
 
<b> Url Blacklist </B>
 - /geturl: Lihat url daftar hitam saat ini
 - /addurl [url/link]: Tambahkan domain ke daftar hitam. Bot akan secara otomatis mem-parsing url.
 - /delurl [url/link]: Hapus url dari daftar hitam.
<b> Contoh:</b>
 - /addblacklist admin jelek: Ini akan menghapus kata "admin jelek" setiap kali anggota grup(kecuali admin) mengetiknya
 - /addurl bit.ly: Ini akan menghapus pesan apa pun yang berisi url "bit.ly"
"""
__mod_name__ = "📓Blacklist"
