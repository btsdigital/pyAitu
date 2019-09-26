from typing import Union, Optional


class BaseStorage:
    async def get_state(self, *,
                        chat: Union[str, int, None] = None,
                        user: Union[str, int, None] = None,
                        default: Optional[str] = None) -> Optional[str]:
        raise NotImplementedError


class DisabledStorage(BaseStorage):
    async def get_state(self, *,
                        chat: Union[str, int, None] = None,
                        user: Union[str, int, None] = None,
                        default: Optional[str] = None) -> Optional[str]:
        return None