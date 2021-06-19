# Written by Inukaasith for the Daisy project
# This file is part of DaisyXBot (Telegram Bot)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.


import json
import math

import requests

from DaisyX.decorator import register

from .utils.disable import disableable_dec
from .utils.message import get_args_str


@register(cmds=["math", "simplify"])
@disableable_dec("math")
async def _(message):
    args = get_args_str(message)
    response = requests.get(f"https://newton.now.sh/api/v2/simplify/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await message.reply(j)


@register(cmds=["factor", "factorize"])
@disableable_dec("factor")
async def _(message):
    args = get_args_str(message)
    response = requests.get(f"https://newton.now.sh/api/v2/factor/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await message.reply(j)


@register(cmds="derive")
@disableable_dec("derive")
async def _(message):
    args = get_args_str(message)
    response = requests.get(f"https://newton.now.sh/api/v2/derive/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await message.reply(j)


@register(cmds="integrate")
@disableable_dec("integrate")
async def _(message):
    args = get_args_str(message)
    response = requests.get(f"https://newton.now.sh/api/v2/integrate/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await message.reply(j)


@register(cmds="zeroes")
@disableable_dec("zeroes")
async def _(message):
    args = get_args_str(message)
    response = requests.get(f"https://newton.now.sh/api/v2/zeroes/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await message.reply(j)


@register(cmds="tangent")
@disableable_dec("tangent")
async def _(message):
    args = get_args_str(message)
    response = requests.get(f"https://newton.now.sh/api/v2/tangent/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await message.reply(j)


@register(cmds="area")
@disableable_dec("area")
async def _(message):
    args = get_args_str(message)
    response = requests.get(f"https://newton.now.sh/api/v2/area/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await message.reply(j)


@register(cmds="cos")
@disableable_dec("cos")
async def _(message):
    args = get_args_str(message)
    await message.reply(str(math.cos(int(args))))


@register(cmds="sin")
@disableable_dec("sin")
async def _(message):
    args = get_args_str(message)
    await message.reply(str(math.sin(int(args))))


@register(cmds="tan")
@disableable_dec("tan")
async def _(message):
    args = get_args_str(message)
    await message.reply(str(math.tan(int(args))))


@register(cmds="arccos")
@disableable_dec("arccos")
async def _(message):
    args = get_args_str(message)
    await message.reply(str(math.acos(int(args))))


@register(cmds="arcsin")
@disableable_dec("arcsin")
async def _(message):
    args = get_args_str(message)
    await message.reply(str(math.asin(int(args))))


@register(cmds="arctan")
@disableable_dec("arctan")
async def _(message):
    args = get_args_str(message)
    await message.reply(str(math.atan(int(args))))


@register(cmds="abs")
@disableable_dec("abs")
async def _(message):
    args = get_args_str(message)
    await message.reply(str(math.fabs(int(args))))


@register(cmds="log")
@disableable_dec("log")
async def _(message):
    args = get_args_str(message)
    await message.reply(str(math.log(int(args))))


__help__ = """
Memecahkan masalah matematika yang kompleks menggunakan https://newton.now.sh dan modul matematika python
 - /simplify- Math /math 2^2+2(2)
 - /factor - Factor /factor x^2 + 2x
 - /derive - Derive /derive x^2+2x
 - /integrate - Mengintegrasikan /integrate x^2+2x
 - /zeroes - Temukan 0's /zeroes x^2+2x
 - /tangent - Temukan Tangent /tangent 2lx^
 - /area - Area di Bawah Kurva /area 2:4lx^3`
 - /cos - Cosinus /cos pi
 - /sin - Sinus /sin 0
 - /tan - Tangent /tan 0
 - /arccos - Inverse Cosinus /arccos 1
 - /arcsin - Inverse Sinus /arcsin 0
 - /arctan - Inverse Tangent /arctan 0
 - /abs - Nilai mutlak /abs -1
 - /log* - Logaritma /log 2l8
 
Perlu diingat, Untuk menemukan garis singgung suatu fungsi pada nilai x tertentu, kirim permintaan sebagai c|f(x) di mana c adalah nilai x yang diberikan dan f(x) adalah ekspresi fungsi, pemisahnya adalah vertikal batang '|'. Lihat tabel di atas untuk contoh permintaan.
Untuk menemukan area di bawah suatu fungsi, kirim permintaan sebagai c:d|f(x) di mana c adalah nilai x awal, d adalah nilai x akhir, dan f(x) adalah fungsi di mana Anda ingin kurva antara dua nilai x.
Untuk menghitung pecahan, masukkan ekspresi sebagai pembilang (lebih) penyebut. Misalnya, untuk memproses 2/4 Anda harus mengirimkan ekspresi Anda sebagai 2(over)4. Ekspresi hasil akan dalam notasi matematika standar (1/2, 3/4).
"""

__mod_name__ = "Matematika🧮"
