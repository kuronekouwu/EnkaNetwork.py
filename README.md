# Enka Network Python
EN | [TH](https://github.com/mrwan200/EnkaNetwork.py/blob/master/README_TH.md)

Library for API wrapper data from site https://enka.network/

# 🏓 Table of content
- [💾 Installation](#installation)
- [✨ Usage](#usage)
- [👀 Example](#example)
- [📗 Class Methods](#class-methods)
- [🚧 Structure](#structure)
	- [Player](#player) 
		- [Namecard](#namecard)
        - [Avatar Icon](#avatar-icon)
        - [Character preview](#character-preview)
    - [Characters](#characters)
        - [Icon](#icon)
        - [Constellation](#constellation)
        - [Skill](#skill)
    - [Equipments (Artifact, Weapon)](#equipments-artifact-weapon)
        - [Equipments Info](#equipments-info)
        - [Equipments Stats](#equipments-stats)
    - [FIGHT_PROP Data](#fight_prop-data)
- [🔧 Assets](#assets)
	- [Character, constellations, skills, namecards](#assets-character-constellations-skills-namecards)
    - [NameTextMapHash](#assets-nametextmaphash)
- [🌎 Languages Supported](#languages-supported)
- [🙋 Support & Question](#support--question)
- [📄 LICENSE](#license)
	
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
    async with client:
        data = await client.fetch_user(843715177)
        print("=== Player Info ===")
        print(f"Nickname: {data.player.nickname}")
        print(f"Level: {data.player.level}")
        print(f"Icon: {data.player.icon.url}")
        print(f"Signature: {data.player.signature}")
        print(f"Achievement: {data.player.achievement}")
        print(f"Abyss floor: {data.player.abyss_floor} - {data.player.abyss_room}")
        print(f"Cache timeout: {data.ttl}")

asyncio.run(main())
```
## Preview
```sh
=== Player Info ===
Nickname: mrwan2546
Level: 55
Icon: https://enka.network/ui/UI_AvatarIcon_Kazuha.png
Signature: K A Z U H A M U C H <3
Achievement: 396
Abyss floor: 8 - 3
Cache timeout: 300
```

## Example
Please see in [example](./example/) folder.

# Class Methods
| Name       | Description     |
|------------|-----------------|
| fetch_user(uid) | Fetch user data |
| set_language(lang) | Set new language <br> Please see [Languages Supported](#languages-supported) |
| update_assets() | Update new assets from repo [Enkanetwork.py Data](https://github.com/mrwan200/enkanetwork.py-data/) |

# Structure
## Player
| Wrapper         |  API            | Notes             |   
|-----------------|-----------------|-------------------|
| nickname        | nickname        | Please see [Namecard](#namecard) |
| signature       | signature       |                   |
| world_level     | worldLevel      |                   |
| achievement     | finishAchievementNum |              |
| namecard        | namecardId  |                       |
| namecards       | showNameCardIdList -> id | Please see [Namecard](#namecard) | 
| abyss_floor     | towerFloorIndex |                   |
| abyss_room      | towerLevelIndex |                   |
| characters_preview | showAvatarInfoList | Please see [Character Preview](#character-preview) |
| avatar        | profilePicture   | Please see [Avatar Icon](#avatar-icon)          |

### Avatar icon
| Wrapper         |  API            | Notes             |   
|-----------------|-----------------|-------------------|
| id              | avatarId        |                   |
| icon            |                 |  Please see [Icon Data](#icon-data) |

### Namecard
| Wrapper         |  API            | Notes             |
|-----------------|-----------------|-------------------|
| id              | -               | Namecard ID       |
| name            | -               | Namecard name     | 
| icon            | -               | Namecard icon, Please see [Icon Data](#icon-data) |
| banner          | -               | Namecard banner, Please see [Icon Data](#icon-data) |
| navbar          | -               | Namecard navbar (Alpha), Please see [Icon Data](#icon-data) |

### Character preview
| Wrapper         |  API            | Notes             |
|-----------------|-----------------|-------------------|
| id              | -               | Avatar ID         |
| name            | -               | Avatar Name       |
| level           | -               | Avatar Level      |
| icon            | -               | Avatar Icon, Please see [Icon Data](#icon-data) |

## Characters
| Wrapper         |  API            | Notes             |
|-----------------|-----------------|-------------------|
| id              | avatarId        |                   |
| name            | -               | Avatar Name       |
| element         | -               | Please see [Element Type](#element-type) |
| rarity          | -               | Rarity            |
| image           | -               | Please see [Icon](#icon) |
| xp              | propMap -> 1001 |                   |
| ascension       | propMap -> 1002 |                   |
| level           | propMap -> 4001 |                   |
| max_level       | -               | Avatar max level (Like 50/60) |    
| friendship_level| fetterInfo.level|                   |
| equipments      | equipList       | Please see [Equipments](#equipments-artifact-weapon) |
| stats           | fightPropMap    | Please see [FIGHT_PROP Data](#fight_prop-data) |
| constellations  | talentIdList    | Please see [Constellation](#constellation) |
| constellations_unlocked | -       | Constellation unlocked |
| skill_data      | inherentProudSkillList |            |
| skill_id        | skillDepotId    |                   |
| skills          | -               | Please see [Skill](#skill) |

### Icon
| Wrapper         |  API            | Notes             |
|-----------------|-----------------|-------------------|
| icon            | -               | Avatar icon, Please see [Icon Data](#icon-data) |
| side            | -               | Avatar side icon, Please see [Icon Data](#icon-data) |
| banner          | -               | Avatar wish banner, Please see [Icon Data](#icon-data) |

### Constellation
| Wrapper         |  API            | Notes             |
|-----------------|-----------------|-------------------|
| id              | -               | Constellation ID |
| name            | -               | Constellation Name |
| icon            | -               | Constellation Icon (URL) |
| unlocked        | -               | Constellation has unlocked |

### Skill
| Wrapper         |  API            | Notes             |
|-----------------|-----------------|-------------------|
| id              | -               | Skill ID          |
| name            | -               | Skill Name        |
| icon            | -               | Skill Icon (URL)  |
| level           | -               | Skill Level       |
| is_boosted      | -               | Skill level has boosted |

## Equipments (Artifact, Weapon)
| Wrapper         |  API            | Notes             |
|-----------------|-----------------|-------------------|
| id              | itemId          |                   |
| level           | reliquary -> level,  weapon -> level| 
| type            | -               | Type of equipment (Artifact or Weapon) |
| refinement      | weapon -> affixMap |                |
| ascension       | weapon -> promoteLevel |             |
| detail          | flat            | Please see [Equipments Info](#equipments-info) |

### Equipments Info
| Wrapper         |  API            | Notes             |
|-----------------|-----------------|-------------------|
| name            | -               | Equipment Name (Artifact name or Weapon name) |
| icon            | icon            | Please see [Icon Data](#icon-data)                 |
| artifact_type   | -               | Please see [Artifact Type](#artifact-type) |
| rarity          | rankLevel       |                   |
| mainstats       | reliquaryMainstat, weaponStats -> 0 | Please see [Equipments Stats](#equipments-stats) |
| substats        | reliquarySubstats, weaponStats -> 1 | Please see [Equipments Stats](#equipments-stats) |

### Equipments Stats
| Wrapper         |  API            | Notes             |
|-----------------|-----------------|-------------------|
| prop_id         | prop_id         |                   |
| type            | -               | Value type (NUMBER or PERCENT) |
| name            | -               | Name of FIGHT_PROP|
| value           | value           |                   |

## FIGHT_PROP Data

In FIGHT_PROP data. You can get the value from 4 methods.
| Choice           |  Example                  | Output                     |
|------------------|---------------------------|----------------------------|
| Get raw value    | stats.FIGHT_PROP_HP.value | 15552.306640625            |
| Get rounded value| stats.FIGHT_PROP_ATTACK.to_rounded() | 344             |
| Get percentage  | stats.FIGHT_PROP_FIRE_ADD_HURT.to_percentage() | 61.5   |
| Get percentage and symbol | stats.FIGHT_PROP_FIRE_ADD_HURT.to_percentage_symbol() | 61.5% |

# Icon Data
In icon data. You can get the value from 2 methods.
| Choice           |  Example                  | Output                         |
|------------------|---------------------------|--------------------------------|
| Get filename     | icon.filename             | UI_AvatarIcon_Kazuha_Card.png  |
| Get URL          | icon.url                  | https://enka.network/ui/UI_AvatarIcon_Kazuha_Card.png |

## Artifact Type
| Key           | Value         |
|---------------|---------------|
| Flower        | EQUIP_BRACER  |
| Feather       | EQUIP_NECKLACE|
| Sands         | EQUIP_SHOES   |
| Goblet        | EQUIP_RING    |
| Circlet       | EQUIP_DRESS   |

## Element Type
| Key           | Value         |
|---------------|---------------|
| Cryo          | Ice           |
| Hydro         | Water         |
| Anemo         | Wind          |
| Pyro          | Fire          |
| Geo           | Rock          |
| Electro       | Electric      |

# Assets

## Assets character, constellations, skills, namecards
You can use avatarId to get the character, constellations, skills, namecards from assets.
```py
import asyncio

from enkanetwork import Assets

assets = Assets()

async def main():
    # Character
    assets.character(10000046)
    # Constellations
    assets.constellations(2081199193)
    # Skills
    assets.constellations(10462)
    # Namecards
    assets.namecards(210059)
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## Assets NameTextMapHash
The `NameTextMapHash` is a hash map that contains the name text of the assets. You can get `NameTextMapHash` from `hash_id` like this:

```py
import asyncio

from enkanetwork import Assets

assets = Assets(lang="en") # Set languege before get name (Ex. English)

async def main():
    print(assets.get_hash_map(1940919994)) # Hu tao
    # OR you can get FIGHT_PROP name
    print(assets.get_hash_map("FIGHT_PROP_BASE_ATTACK")) # Base ATK
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```


## Languages Supported
| Languege    |  Code   |
|-------------|---------|
|  English    |     en  |
|  русский    |     ru  |
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

If you want full docs for the API, visit [EnkaNetwork API Docs](https://github.com/EnkaNetwork/API-docs)

## Support & Question
If you need support or some question about EnkaNetwokt.py. You can feel free contact to me in [Enka.network discord server](https://discord.gg/G3m7CWkssY) in [𝖯𝖸┃enkanetwork․py](https://discord.com/channels/840335525621268520/1046281445049647104) channel and mention (Ping) to **@M-307** for support and help

# LICENSE
[MIT License](./LICENSE)

![Keqing](https://c.tenor.com/MnkpnVCLcb0AAAAC/keqing-dance.gif)

[Picture by KKOMDASTRO](https://twitter.com/KKOMDASTRO)