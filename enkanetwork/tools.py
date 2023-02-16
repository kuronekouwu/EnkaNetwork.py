from typing import List, Any, Dict

async def merge_raw_data(
    new_data: Dict[str, Any], 
    cache_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
        Merge cached data into newly fetched data.

        Parameters
        ----------
            new_data: The newly fetched data as a dictionary.
            cache_data: The cached data as a dictionary.

        Returns
        -------
            A dictionary containing the merged data.
    """

    async def combine_lists(
        new_list: List[Dict[str, Any]], cache_list: List[Dict[str, Any]]
    ):
        new_ids = {item["avatarId"] for item in new_list}
        unique_cache_items = [
            item for item in cache_list if item["avatarId"] not in new_ids
        ]
        new_list.extend(unique_cache_items)

    if "showAvatarInfoList" in cache_data["playerInfo"]:
        new_data.setdefault("playerInfo", {}).setdefault(
            "showAvatarInfoList", [])
        await combine_lists(
            new_data["playerInfo"]["showAvatarInfoList"],
            cache_data["playerInfo"]["showAvatarInfoList"],
        )

    if "avatarInfoList" in cache_data:
        new_data.setdefault("avatarInfoList", [])
        await combine_lists(
            new_data["avatarInfoList"], cache_data["avatarInfoList"]
        )

    return new_data