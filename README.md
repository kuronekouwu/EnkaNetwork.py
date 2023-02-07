# Enka Network Python

EN | [TH](https://github.com/mrwan200/EnkaNetwork.py/blob/master/README_TH.md)

Library for API wrapper data from site https://enka.network/

# 🏓 Table of content

- [💾 Installation](#installation)
- [✨ Usage](#usage)
- [👀 Example](#example)
- [📗 Class Methods](#class-methods)
- [📥 Response data](#return-data)
  - [UID](#uid)
  - [Profile](#profile)
- [🚧 Structure](#structure)
  - [Player owner](#player-owner)
  - [Profile patreon](#profile-patreon)
  - [Profile Hoyos](#profile-hoyos)
  - [Build(s) info](#avatar-builds-info)
  - [Profile info](#profile-info)
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
    - [Build(s)](#build)
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

Please refer in [example](./example/) folder.

# Class Methods

| Name                                | Description                                                                                         |
| ----------------------------------- | --------------------------------------------------------------------------------------------------- |
| fetch_user(uid)                     | Fetch user data (UID) **(Will be depercated soon)**                                                 |
| fetch_user_by_uid(uid)              | Fetch user data (UID)                                                                               |
| fetch_user_by_username(profile_id)  | Fetch user data (Profile ID) **(For subscriptions in Enka.Network)**                                |
| fetch_hoyos_by_username(profile_id) | Fetch user hoyo(s) data (Profile ID) **(For subscriptions in Enka.Network)**                        |
| fetch_builds(profile_id, metaname)  | Fetch build data (Profile ID) **(For subscriptions in Enka.Network)**                               |
| set_language(lang)                  | Set new language <br> Please refer [Languages Supported](#languages-supported)                      |
| update_assets()                     | Update new assets from repo [Enkanetwork.py Data](https://github.com/mrwan200/enkanetwork.py-data/) |

# Return data

## UID

Return type: `EnkaNetworkResponse`
| Wrapper | API | Notes |
| ---------- | -------------- | ------------------------------------------ |
| player | playerInfo | Please refer [Player](#player) |
| characters | avatarInfoList | Please refer [Characters](#characters) |
| profile | - | Please refer [Profile Info](#profile-info) |
| owner | owner | Please refer [Player Owner](#player-owner) |
| ttl | ttl | |
| uid | uid | |

## Profile

Return type: `EnkaNetworkProfileResponse`
| Wrapper | API | Notes |
| -------- | ---------- | --------------------------------------------------- |
| username | playerInfo | Please refer [Player](#player) |
| profile | profile | Please refer in [Profile patreon](#profile-patreon) |
| hoyos | hoyos | Please refer [Profile hoyos](#profile-hoyos) |

# Structure

## Player owner

| Wrapper  | API      | Notes                                               |
| -------- | -------- | --------------------------------------------------- |
| hash     | hash     |                                                     |
| username | username | Please refer [Tier](#tier)                          |
| profile  | profile  | Please refer in [Profile patreon](#profile-patreon) |
| builds   | -        | Please refer [Build(s) info](#avatar-builds-info)   |

## Profile Patreon

| Wrapper      | API          | Notes                      |
| ------------ | ------------ | -------------------------- |
| bio          | bio          |                            |
| level        | level        | Please refer [Tier](#tier) |
| profile      | worldLevel   |                            |
| signup_state | signup_state |                            |
| image_url    | image_url    |                            |

## Profile Hoyos

| Wrapper      | API          | Notes                                            |
| ------------ | ------------ | ------------------------------------------------ |
| uid_public   | uid_public   |                                                  |
| public       | public       |                                                  |
| verified     | verified     |                                                  |
| player_info  | player_info  | Please refer [Profile Patreon](#profile-patreon) |
| signup_state | signup_state |                                                  |
| signup_state | signup_state |                                                  |

## Avatar build(s) info

| Wrapper     | API         | Notes                                  |
| ----------- | ----------- | -------------------------------------- |
| id          | id          |                                        |
| name        | name        |                                        |
| avatar_id   | avatar_id   |                                        |
| avatar_data | avatar_data | Please refer [Characters](#characters) |
| order       | order       |                                        |
| live        | live        |                                        |
| settings    | settings    |                                        |
| public      | public      |                                        |

## Profile Info

| Wrapper | API | Notes                          |
| ------- | --- | ------------------------------ |
| uid     | -   | UID in-game                    |
| url     | -   | URL to enter Enka.Network site |
| path    | -   | Path URL                       |

## Player

| Wrapper            | API                      | Notes                                                |
| ------------------ | ------------------------ | ---------------------------------------------------- |
| nickname           | nickname                 | Please refer [Namecard](#namecard)                   |
| signature          | signature                |                                                      |
| world_level        | worldLevel               |                                                      |
| achievement        | finishAchievementNum     |                                                      |
| namecard           | namecardId               |                                                      |
| namecards          | showNameCardIdList -> id | Please refer [Namecard](#namecard)                   |
| abyss_floor        | towerFloorIndex          |                                                      |
| abyss_room         | towerLevelIndex          |                                                      |
| characters_preview | showAvatarInfoList       | Please refer [Character Preview](#character-preview) |
| avatar             | profilePicture           | Please refer [Avatar Icon](#avatar-icon)             |

### Avatar icon

| Wrapper | API      | Notes                                |
| ------- | -------- | ------------------------------------ |
| id      | avatarId |                                      |
| icon    |          | Please refer [Icon Data](#icon-data) |

### Namecard

| Wrapper | API | Notes                                                         |
| ------- | --- | ------------------------------------------------------------- |
| id      | -   | Namecard ID                                                   |
| name    | -   | Namecard name                                                 |
| icon    | -   | Namecard icon, Please refer [Icon Data](#icon-data)           |
| banner  | -   | Namecard banner, Please refer [Icon Data](#icon-data)         |
| navbar  | -   | Namecard navbar (Alpha), Please refer [Icon Data](#icon-data) |

### Character preview

| Wrapper | API | Notes                                             |
| ------- | --- | ------------------------------------------------- |
| id      | -   | Avatar ID                                         |
| name    | -   | Avatar Name                                       |
| level   | -   | Avatar Level                                      |
| icon    | -   | Avatar Icon, Please refer [Icon Data](#icon-data) |

## Characters

| Wrapper                 | API                    | Notes                                                  |
| ----------------------- | ---------------------- | ------------------------------------------------------ |
| id                      | avatarId               |                                                        |
| name                    | -                      | Avatar Name                                            |
| element                 | -                      | Please refer [Element Type](#element-type)             |
| rarity                  | -                      | Rarity                                                 |
| image                   | -                      | Please refer [Icon](#icon)                             |
| xp                      | propMap -> 1001        |                                                        |
| ascension               | propMap -> 1002        |                                                        |
| level                   | propMap -> 4001        |                                                        |
| max_level               | -                      | Avatar max level (Like 50/60)                          |
| friendship_level        | fetterInfo.level       |                                                        |
| equipments              | equipList              | Please refer [Equipments](#equipments-artifact-weapon) |
| stats                   | fightPropMap           | Please refer [FIGHT_PROP Data](#fight_prop-data)       |
| constellations          | talentIdList           | Please refer [Constellation](#constellation)           |
| constellations_unlocked | -                      | Constellation unlocked                                 |
| skill_data              | inherentProudSkillList |                                                        |
| skill_id                | skillDepotId           |                                                        |
| skills                  | -                      | Please refer [Skill](#skill)                           |

### Icon

| Wrapper | API | Notes                                                    |
| ------- | --- | -------------------------------------------------------- |
| icon    | -   | Avatar icon, Please refer [Icon Data](#icon-data)        |
| side    | -   | Avatar side icon, Please refer [Icon Data](#icon-data)   |
| banner  | -   | Avatar wish banner, Please refer [Icon Data](#icon-data) |

### Constellation

| Wrapper  | API | Notes                      |
| -------- | --- | -------------------------- |
| id       | -   | Constellation ID           |
| name     | -   | Constellation Name         |
| icon     | -   | Constellation Icon (URL)   |
| unlocked | -   | Constellation has unlocked |

### Skill

| Wrapper    | API | Notes                   |
| ---------- | --- | ----------------------- |
| id         | -   | Skill ID                |
| name       | -   | Skill Name              |
| icon       | -   | Skill Icon (URL)        |
| level      | -   | Skill Level             |
| is_boosted | -   | Skill level has boosted |

## Equipments (Artifact, Weapon)

| Wrapper    | API                                 | Notes                                            |
| ---------- | ----------------------------------- | ------------------------------------------------ |
| id         | itemId                              |                                                  |
| level      | reliquary -> level, weapon -> level |
| type       | -                                   | Type of equipment (Artifact or Weapon)           |
| refinement | weapon -> affixMap                  |                                                  |
| ascension  | weapon -> promoteLevel              |                                                  |
| detail     | flat                                | Please refer [Equipments Info](#equipments-info) |

### Equipments Info

| Wrapper       | API                                 | Notes                                              |
| ------------- | ----------------------------------- | -------------------------------------------------- |
| name          | -                                   | Equipment Name (Artifact name or Weapon name)      |
| icon          | icon                                | Please refer [Icon Data](#icon-data)               |
| artifact_type | -                                   | Please refer [Artifact Type](#artifact-type)       |
| rarity        | rankLevel                           |                                                    |
| mainstats     | reliquaryMainstat, weaponStats -> 0 | Please refer [Equipments Stats](#equipments-stats) |
| substats      | reliquarySubstats, weaponStats -> 1 | Please refer [Equipments Stats](#equipments-stats) |

### Equipments Stats

| Wrapper | API     | Notes                          |
| ------- | ------- | ------------------------------ |
| prop_id | prop_id |                                |
| type    | -       | Value type (NUMBER or PERCENT) |
| name    | -       | Name of FIGHT_PROP             |
| value   | value   |                                |

## FIGHT_PROP Data

In FIGHT_PROP data. You can get the value from 4 methods.
| Choice | Example | Output |
|------------------|---------------------------|----------------------------|
| Get raw value | stats.FIGHT_PROP_HP.value | 15552.306640625 |
| Get rounded value| stats.FIGHT_PROP_ATTACK.to_rounded() | 344 |
| Get percentage | stats.FIGHT_PROP_FIRE_ADD_HURT.to_percentage() | 61.5 |
| Get percentage and symbol | stats.FIGHT_PROP_FIRE_ADD_HURT.to_percentage_symbol() | 61.5% |

## Build

In this `Builds` It's not pretty data. You can use this method to get data. Or if you want get full, You can use `raw` argument
| Choice | Example | Output |
|------------------|---------------------------|----------------------------|
| Get avatar ID list | builds.get_avatar_list() | [10000021,10000037,10000025, ...] |
| Get character build | builds.get_character(10000021) | List of [Build info](#avatar-builds-info) |
| Get build info by avatar id | builds.get_character(10000021, 11111111) | [Build info](#avatar-builds-info) |

# Icon Data

In icon data. You can get the value from 2 methods.
| Choice | Example | Output |
|------------------|---------------------------|--------------------------------|
| Get filename | icon.filename | UI_AvatarIcon_Kazuha_Card.png |
| Get URL | icon.url | https://enka.network/ui/UI_AvatarIcon_Kazuha_Card.png |

## Artifact Type

| Key     | Value          |
| ------- | -------------- |
| Flower  | EQUIP_BRACER   |
| Feather | EQUIP_NECKLACE |
| Sands   | EQUIP_SHOES    |
| Goblet  | EQUIP_RING     |
| Circlet | EQUIP_DRESS    |

## Element Type

| Key     | Value    |
| ------- | -------- |
| Cryo    | Ice      |
| Hydro   | Water    |
| Anemo   | Wind     |
| Pyro    | Fire     |
| Geo     | Rock     |
| Electro | Electric |

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

| Languege   | Code |
| ---------- | ---- |
| English    | en   |
| русский    | ru   |
| Tiếng Việt | vi   |
| ไทย        | th   |
| português  | pt   |
| 한국어     | kr   |
| 日本語     | jp   |
| 中文       | zh   |
| Indonesian | id   |
| français   | fr   |
| español    | es   |
| deutsch    | de   |
| Taiwan     | cht  |
| Chinese    | chs  |

If you want full docs for the API, visit [EnkaNetwork API Docs](https://github.com/EnkaNetwork/API-docs)

## Support & Question

If you need support or some question about EnkaNetwokt.py. You can feel free contact to me in [Enka.network discord server](https://discord.gg/G3m7CWkssY) in [𝖯𝖸┃enkanetwork․py](https://discord.com/channels/840335525621268520/1046281445049647104) channel and mention (Ping) to **@M-307** for support and help

# LICENSE

[MIT License](./LICENSE)

![Keqing](https://c.tenor.com/MnkpnVCLcb0AAAAC/keqing-dance.gif)

[Picture by KKOMDASTRO](https://twitter.com/KKOMDASTRO)
