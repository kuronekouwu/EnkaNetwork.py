#!/bin/bash
# -*- Mode: python -*-
import enkanetwork
import json

from enkanetwork.enum import ElementType, Language, EquipmentsType
from enkanetwork.model.equipments import Equipments

# Init enkanetwork client
client = enkanetwork.client.EnkaNetworkAPI(lang=enkanetwork.Language.TH)

with open("test.json", "r") as f:
    _j = json.load(f)

def test_get_asset_data() -> None:
    """
        Test case 1:
            Get asset data
    """
    for lang in list(Language):
        client.lang = lang.value
        for ids in client.assets.CHARACTERS_IDS:
            data = client.assets.character(ids)

            # Check character data
            assert data is not None  # Check data is None
            if not data.id in [10000005, 10000007]:
                assert data.id == int(ids)  # Check id is correct
            else:
                if data.skill_id > 0:
                    assert f"{data.id}-{data.skill_id}" == ids # Check id is correct (Tarveler)

            assert str(data.id)[:2] != "11"  # Check id is not 11xx (Test character)
            assert data.element in list(ElementType)  # Check element is correct

            # Check icon filename
            assert "_AvatarIcon_" in data.images.icon.filename and \
                "_AvatarIcon_Side_" in data.images.side.filename and \
                "_Gacha_AvatarImg_" in data.images.banner.filename and \
                "_Card" in data.images.card.filename
            
            assert data.images.icon.url.startswith("https://") and \
                data.images.side.url.startswith("https://") and \
                data.images.banner.url.startswith("https://") and \
                data.images.card.url.startswith("https://")

            # Get name hash map
            name = client.assets.get_hash_map(data.hash_id)
            assert name is not None

            # Get constellations
            for constellations in data.constellations:
                _constellations = client.assets.constellations(constellations)
                assert _constellations is not None
                assert "UI_Talent_" in _constellations.icon.filename
                assert _constellations.icon.url.startswith("https://")

                # Get name hash map
                name = client.assets.get_hash_map(_constellations.hash_id)
                assert name is not None

            # Get skills
            for skill in data.skills:
                _skill = client.assets.skills(skill)
                assert _skill is not None
                assert "Skill_" in _skill.icon.filename
                assert _skill.icon.url.startswith("https://")

                # Get name hash map
                name = client.assets.get_hash_map(_skill.hash_id)
                assert name is not None

def test_artifacts() -> None:
    """
        Test case 2:
            Test equipments star
    """

    for star in _j["artifacts"]:
        raw = _j["artifacts"][star]
        data = Equipments.model_validate(raw)
        assert data.id == raw["itemId"]
        assert data.type in list(EquipmentsType)
        assert data.detail.name is not None
        assert data.detail.icon is not None
        assert data.detail.icon.url.startswith("https://")
        assert data.detail.rarity != 0
        assert data.level == raw["reliquary"]["level"] - 1

        # Stats
        assert data.detail.mainstats is not None
        assert data.detail.mainstats.prop_id != ""
        assert data.detail.mainstats.name is not None

        if len(data.detail.substats) > 0:
            for sub in data.detail.substats:
                assert sub.prop_id != ""
                assert sub.name is not None
        

def test_weapons():
    """
        Test case 3:
            Test weapons star
    """

    for star in _j["weapons"]:
        raw = _j["weapons"][star]
        data = Equipments.model_validate(raw)
        assert data.id == raw["itemId"]
        assert data.type in list(EquipmentsType)
        assert data.detail.name is not None
        assert data.detail.icon is not None
        assert data.detail.icon.url.startswith("https://")
        assert data.detail.rarity != 0
        assert data.level == raw["weapon"]["level"]

        # Stats
        assert data.detail.mainstats is not None
        assert data.detail.mainstats.prop_id != ""
        assert data.detail.mainstats.name is not None

        if len(data.detail.substats) > 0:
            for sub in data.detail.substats:
                assert sub.prop_id != ""
                assert sub.name is not None
        
        assert data.level == raw["weapon"]["level"]
        if "affixMap" in raw["weapon"]:
            assert data.refinement == raw["weapon"]["affixMap"][list(raw["weapon"]["affixMap"].keys())[0]] + 1

def test_costumes() -> None:
    """
        Test case 4:
            Test characters costumes
    """

    for costume in client.assets.COSTUMES_IDS:
        _costume = client.assets.character_costume(costume)
        assert _costume is not None
        assert _costume.id == int(costume)
        # Check icon filename
        assert "_AvatarIcon_" in _costume.images.icon.filename and \
                "_AvatarIcon_Side_" in _costume.images.side.filename and \
                "_Costume_" in _costume.images.banner.filename and \
                "_Card" in _costume.images.card.filename

        assert _costume.images.icon.url.startswith("https://") and \
                _costume.images.side.url.startswith("https://") and \
                _costume.images.banner.url.startswith("https://") and \
                _costume.images.card.url.startswith("https://")

def test_namecards() -> None:
    """
        Test case 5:
            Test namecards
    """

    for costume in client.assets.NAMECARD_IDS:
        _namecard = client.assets.namecards(costume)
        assert _namecard is not None
        assert _namecard.id == int(costume)
        # Check icon filename
        assert  _namecard.icon.url.startswith("https://") and \
                _namecard.banner.url.startswith("https://") and \
                _namecard.navbar.url.startswith("https://")

        # Get name hash map
        name = client.assets.get_hash_map(_namecard.hash_id)
        assert name is not None