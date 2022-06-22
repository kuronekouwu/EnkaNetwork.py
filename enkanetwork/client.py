import aiohttp
import sys

from .model import EnkaNetworkResponse
from .exception import VaildateUIDError, UIDNotFounded

class EnkaNetworkAPI:
    URL = "https://enka.shinshin.moe/u/{uid}/__data.json"
    USER_AGENT = "EnkaNetwork.py / {version} (Python {major}.{minor}.{micro})"

    def __init__(self) -> None:
        pass
    
    async def __get_headers(self):
        # Get python version
        python_version = sys.version_info

        return {
            "User-Agent": self.USER_AGENT.format(
                version='1.0.0',
                major=python_version.major,
                minor=python_version.minor,
                micro=python_version.micro
            ),
        }

    async def fetch_user(self, uid: int) -> EnkaNetworkResponse:
        if not isinstance(uid, int) or \
            len(str(uid)) != 9 or \
            (uid < 100000000 and uid > 999999999):
            raise VaildateUIDError("Validate UID failed. Please check your UID.")
            
        session = aiohttp.ClientSession(headers=await self.__get_headers())
        resp = await session.request(method="GET", url=self.URL.format(uid=uid))
        if resp.status != 200:
            raise UIDNotFounded(f"UID {uid} not found.")

        data = await resp.json()
                    
        if not data:
            raise UIDNotFounded(f"UID {uid} not found.")

        await session.close()

        return EnkaNetworkResponse.parse_obj(data)