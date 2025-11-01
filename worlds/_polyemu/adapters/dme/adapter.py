from ... import core as polyemu

__all__ = [
    "DMEAdapter",
]

class DMEAdapter(polyemu.Adapter):
    name = "DME Adapter"

    def __init__(self):
        super().__init__()

    def is_connected(self):
        pass

    async def connect(self):
        pass

    async def disconnect(self):
        pass

    async def send_message(self, message) -> bytes:
        pass