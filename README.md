# Enka Network Python
Library for fetching JSON data from site https://enka.shinshin.moe/

# Installation
```
pip install enkanetwork.py
```

# Usage
```py
import asyncio

from enkanetwork import EnkaNetworkAPI

client = EnkaNetworkAPI()

async def main():
    data = await client.fetch_user(843715177)
    print(f"Nickname: {data.player.nickname}")
    print(f"Level: {data.player.level}")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

```sh
Nickname: mrwan2546
Level: 55
Cache timeout: 236
```

If you want full docs for the API, visit [EnkaNetwork API](https://github.com/EnkaNetwork/API-docs)

# LICENSE
[MIT License](./LICENSE)

![Keqing](https://c.tenor.com/MnkpnVCLcb0AAAAC/keqing-dance.gif)

[Picture by KKOMDASTRO](https://twitter.com/KKOMDASTRO)