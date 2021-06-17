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

from countryinfo import CountryInfo

from DaisyX.services.events import register
from DaisyX.services.telethon import tbot as borg


@register(pattern="^/country (.*)")
async def msg(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    lol = input_str
    country = CountryInfo(lol)
    try:
        a = country.info()
    except:
        await event.reply("Negara Tidak Tersedia Saat Ini")
    name = a.get("nama")
    bb = a.get("alt Ejaan")
    hu = ""
    for p in bb:
        hu += p + ",  "

    area = a.get("area")
    borders = ""
    hell = a.get("perbatasan")
    for fk in hell:
        borders += fk + ",  "

    call = ""
    WhAt = a.get("kode panggilan")
    for what in WhAt:
        call += what + "  "

    capital = a.get("modal")
    currencies = ""
    fker = a.get("mata uang")
    for FKer in fker:
        currencies += FKer + ",  "

    HmM = a.get("demonym")
    geo = a.get("geoJSON")
    pablo = geo.get("fitur")
    Pablo = pablo[0]
    PAblo = Pablo.get("geometry")
    EsCoBaR = PAblo.get("tipe")
    iso = ""
    iSo = a.get("ISO")
    for hitler in iSo:
        po = iSo.get(hitler)
        iso += po + ",  "
    fla = iSo.get("alpha2")
    fla.upper()

    languages = a.get("bahasa")
    lMAO = ""
    for lmao in languages:
        lMAO += lmao + ",  "

    nonive = a.get("nama asli")
    waste = a.get("populasi")
    reg = a.get("wilayah")
    sub = a.get("sub kawasan")
    tik = a.get("zona waktu")
    tom = ""
    for jerry in tik:
        tom += jerry + ",   "

    GOT = a.get("tld")
    lanester = ""
    for targaryen in GOT:
        lanester += targaryen + ",   "

    wiki = a.get("wiki")

    caption = f"""<b><u>Informasi Berhasil Dikumpulkan</b></u>
<b>
Nama negara:- {name}
Ejaan Alternatif:- {hu}
Wilayah Negara:- {area} km persegi
Borders:- {borders}
Kode Panggilan:- {call}
Ibukota Negara:- {capital}
Mata uang negara:- {currencies}
Demonym:- {HmM}
Tipe Negara:- {EsCoBaR}
Nama ISO:- {iso}
Bahasa:- {lMAO}
Nama Asli:- {nonive}
populasi:- {waste}
Wilayah:- {reg}
Sub Wilayah:- {sub}
Zona waktu:- {tom}
Domain Tingkat Atas:- {lanester}
wikipedia:- {wiki}</b>
Dikumpulkan oleh Roso.</b>
"""

    await borg.send_message(
        event.chat_id,
        caption,
        parse_mode="HTML",
    )
