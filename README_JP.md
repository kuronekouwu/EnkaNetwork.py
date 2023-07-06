# Enka Network Python

EN | [TH](https://github.com/mrwan200/EnkaNetwork.py/blob/master/README_TH.md) | [JP](https://github.com/mrwan200/EnkaNetwork.py/blob/master/README_JP.md)

https://enka.network/ のAPIラッパーライブラリ

# 🏓 目次

- [💾 インストール](#インストール)
- [✨ 使い方](#使い方)
- [👀 使用例](#使用例)
- [📗 メソッド一覧](#メソッド一覧)
- [📥 レスポンス](#レスポンス)
  - [UID](#uid)
  - [プロフィール](#プロフィール)
- [🚧 データ構造](#データ構造)
  - [プレイヤーオーナー](#プレイヤーオーナー)
  - [Profile patreon](#profile-patreon)
  - [Profile Hoyos](#profile-hoyos)
  - [Build(s) info](#avatar-builds-info)
  - [Profile info](#profile-info)
  - [Player](#プレイヤー)
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
- [🌎 言語のサポート](#言語のサポート)
- [🙋 Support & Question](#support--question)
- [📄 LICENSE](#license)

# インストール

```
pip install enkanetwork.py
```

# 使い方

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
        print(f"Icon: {data.player.avatar.icon.url}")
        print(f"Signature: {data.player.signature}")
        print(f"Achievement: {data.player.achievement}")
        print(f"Abyss floor: {data.player.abyss_floor} - {data.player.abyss_room}")
        print(f"Cache timeout: {data.ttl}")

asyncio.run(main())
```

## 出力

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

## 使用例

[example](./example/) 参照

# メソッド一覧

| メソッド名                                | 詳細                                                                                         |
| ----------------------------------- | --------------------------------------------------------------------------------------------------- |
| fetch_user(uid)                     | ユーザーデータの取得 (UID) **(まもなく廃止されます)**                                                 |
| fetch_user_by_uid(uid)              | ユーザーデータの取得 (UID)                                                                               |
| fetch_user_by_username(profile_id)  | ユーザーデータの取得 (プロフィールID) **(For subscriptions in Enka.Network)**                                |
| fetch_hoyos_by_username(profile_id) | hoyosのユーザーデータの取得 (プロフィールID) **(For subscriptions in Enka.Network)**                        |
| fetch_builds(profile_id, metaname)  | ビルドデータの取得 (プロフィールID) **(For subscriptions in Enka.Network)**                               |
| set_language(lang)                  | 言語の設定 <br> [言語のサポート](#言語のサポート) 参照                      |
| update_assets()                     |  [Enkanetwork.py Data](https://github.com/mrwan200/enkanetwork.py-data/) からアセットを更新します。 |

# レスポンス

## UID

戻り値の型: `EnkaNetworkResponse`
| ラッパー | API | 備考 |
| ---------- | -------------- | ------------------------------------------ |
| player | playerInfo | [プレイヤー](#プレイヤー) を参照 |
| characters | avatarInfoList | [キャラクター](#characters) を参照 |
| profile | - | [プロフィール情報](#プロフィール情報) を参照 |
| owner | owner | [プレイヤーオーナー](#プレイヤーオーナー) を参照 |
| ttl | ttl | |
| uid | uid | |

## プロフィール

戻り値の型: `EnkaNetworkProfileResponse`
| ラッパー | API | 備考 |
| -------- | ---------- | --------------------------------------------------- |
| username | playerInfo | [プレイヤー](#プレイヤー) を参照 |
| profile | profile | [Patreonプロフィール](#profile-patreon) を参照 |
| hoyos | hoyos | [hoyosプロフィール](#hoyosプロフィール) を参照 |

# データ構造

## プレイヤーオーナー

| ラッパー  | API      | 備考                                               |
| -------- | -------- | --------------------------------------------------- |
| hash     | hash     |                                                     |
| username | username | [Tier](#tier) を参照                          |
| profile  | profile  | [Patreonプロフィール](#Patreonプロフィール) を参照 |
| builds   | -        | [ビルド情報](#avatar-builds-info) を参照   |

## Patreonプロフィール

| ラッパー      | API          | 備考                      |
| ------------ | ------------ | -------------------------- |
| bio          | bio          |                            |
| level        | level        | [Tier](#tier) を参照 |
| profile      | worldLevel   |                            |
| signup_state | signup_state |                            |
| image_url    | image_url    |                            |

## Hoyosプロフィール

| ラッパー      | API          | 備考                                            |
| ------------ | ------------ | ------------------------------------------------ |
| uid_public   | uid_public   |                                                  |
| public       | public       |                                                  |
| verified     | verified     |                                                  |
| player_info  | player_info  | [Patreonプロフィール](#Patreonプロフィール) を参照 |
| signup_state | signup_state |                                                  |
| signup_state | signup_state |                                                  |

## アバタービルド情報

| ラッパー     | API         | 備考                                  |
| ----------- | ----------- | -------------------------------------- |
| id          | id          |                                        |
| name        | name        |                                        |
| avatar_id   | avatar_id   |                                        |
| avatar_data | avatar_data | [キャラクター](#キャラクター) を参照 |
| order       | order       |                                        |
| live        | live        |                                        |
| settings    | settings    |                                        |
| public      | public      |                                        |

## プロフィール情報

| ラッパー | API | 備考                          |
| ------- | --- | ------------------------------ |
| uid     | -   | ゲーム内UID                    |
| url     | -   | Enka.NetworkへのURL |
| path    | -   | URLのパス                       |

## プレイヤー

| ラッパー            | API                      | 備考                                                |
| ------------------ | ------------------------ | ---------------------------------------------------- |
| nickname           | nickname                 | [名刺](#名刺) を参照                   |
| signature          | signature                |                                                      |
| world_level        | worldLevel               |                                                      |
| achievement        | finishAchievementNum     |                                                      |
| namecard           | namecardId               |                                                      |
| namecards          | showNameCardIdList -> id | [名刺](#名刺) を参照                   |
| abyss_floor        | towerFloorIndex          |                                                      |
| abyss_room         | towerLevelIndex          |                                                      |
| characters_preview | showAvatarInfoList       | [Character Preview](#character-preview) を参照 |
| avatar             | profilePicture           | [Avatar Icon](#avatar-icon) を参照             |

### Avatar icon

| ラッパー | API      | 備考                                |
| ------- | -------- | ------------------------------------ |
| id      | avatarId |                                      |
| icon    |          | Please refer [Icon Data](#icon-data) |

### 名刺

| ラッパー | API | 備考                                                         |
| ------- | --- | ------------------------------------------------------------- |
| id      | -   | 名刺ID                                                   |
| name    | -   | 名刺の名前                                                 |
| icon    | -   | 名刺アイコン, [Icon Data](#icon-data) を参照           |
| banner  | -   | 名刺のバナー, [Icon Data](#icon-data) を参照         |
| navbar  | -   | Namecard navbar (Alpha), Please refer [Icon Data](#icon-data) |

### キャラクタープレビュー

| ラッパー | API | 備考                                             |
| ------- | --- | ------------------------------------------------- |
| id      | -   | アバターID                                         |
| name    | -   | アバター名                                       |
| level   | -   | アバターのレベル                                      |
| icon    | -   | アバターアイコン, [Icon Data](#icon-data) を参照 |

## Characters

| ラッパー                 | API                    | 備考                                                  |
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

| ラッパー | API | 備考                                                    |
| ------- | --- | -------------------------------------------------------- |
| icon    | -   | Avatar icon, Please refer [Icon Data](#icon-data)        |
| side    | -   | Avatar side icon, Please refer [Icon Data](#icon-data)   |
| banner  | -   | Avatar wish banner, Please refer [Icon Data](#icon-data) |

### Constellation

| ラッパー  | API | 備考                      |
| -------- | --- | -------------------------- |
| id       | -   | Constellation ID           |
| name     | -   | Constellation Name         |
| icon     | -   | Constellation Icon (URL)   |
| unlocked | -   | Constellation has unlocked |

### Skill

| ラッパー    | API | 備考                   |
| ---------- | --- | ----------------------- |
| id         | -   | Skill ID                |
| name       | -   | Skill Name              |
| icon       | -   | Skill Icon (URL)        |
| level      | -   | Skill Level             |
| is_boosted | -   | Skill level has boosted |

## Equipments (Artifact, Weapon)

| ラッパー    | API                                 | 備考                                            |
| ---------- | ----------------------------------- | ------------------------------------------------ |
| id         | itemId                              |                                                  |
| level      | reliquary -> level, weapon -> level |
| type       | -                                   | Type of equipment (Artifact or Weapon)           |
| refinement | weapon -> affixMap                  |                                                  |
| ascension  | weapon -> promoteLevel              |                                                  |
| detail     | flat                                | Please refer [Equipments Info](#equipments-info) |

### Equipments Info

| ラッパー       | API                                 | 備考                                              |
| ------------- | ----------------------------------- | -------------------------------------------------- |
| name          | -                                   | Equipment Name (Artifact name or Weapon name)      |
| icon          | icon                                | Please refer [Icon Data](#icon-data)               |
| artifact_type | -                                   | Please refer [Artifact Type](#artifact-type)       |
| rarity        | rankLevel                           |                                                    |
| mainstats     | reliquaryMainstat, weaponStats -> 0 | Please refer [Equipments Stats](#equipments-stats) |
| substats      | reliquarySubstats, weaponStats -> 1 | Please refer [Equipments Stats](#equipments-stats) |

### Equipments Stats

| ラッパー | API     | 備考                          |
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

## 言語のサポート

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
