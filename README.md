# Enka Network Python
EN | [TH](./README_TH.md)

Library for fetching JSON data from site https://enka.shinshin.moe/

# 💾 Installation
```
pip install enkanetwork.py
```

# ✨ Usage
```py
import asyncio

from enkanetwork import EnkaNetworkAPI

client = EnkaNetworkAPI()

async def main():
    data = await client.fetch_user(843715177)
    print("=== Player Info ===")
    print(f"Nickname: {data.player.nickname}")
    print(f"Level: {data.player.level}")
    print(f"Icon: {data.player.profile_picture.icon}")
    print(f"Signature: {data.player.signature}")
    print(f"Achievement: {data.player.achievement}")
    print(f"Abyss floor: {data.player.abyss_floor} - {data.player.abyss_room}")
    print(f"Cache timeout: {data.ttl}")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

```sh
=== Player Info ===
Nickname: mrwan2546
Level: 55
Icon: https://enka.shinshin.moe/ui/UI_AvatarIcon_Hutao.png
Signature: ?
Achievement: 395
Abyss floor: 8 - 3
Cache timeout: 300
```

If you want full docs for the API, visit [EnkaNetwork API Docs](https://github.com/EnkaNetwork/API-docs)

## 🌎 Languages Supported
| Languege    |  Code   |
|-------------|---------|
|  English    |     en  |
|  Россия     |     ru  |
|  Tiếng Việt |     vi  |
|  ไทย        |     th  |
|  português  |     pt  |
|  한국어      |     kr  |
|  日本語      |     jp  |
|  中文        |     zh  |
|  Indonesian |     id  |
|  français   |     fr  |
|  español    |     es  |
|  deutsch    |     de  |
|  Taiwan     |    cht  |
|  Chinese    |    chs  |

## 👀 Example
Please see in [example](./example/) folder.

# 📄 LICENSE
[MIT License](./LICENSE)

![Keqing](https://c.tenor.com/MnkpnVCLcb0AAAAC/keqing-dance.gif)

[Picture by KKOMDASTRO](https://twitter.com/KKOMDASTRO)