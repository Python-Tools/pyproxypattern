import asyncio
import unittest
from typing import Any
from aiounittest import async_test
from pyproxy import Proxy


def setUpModule() -> None:
    print("[SetUp pyproxypattern aio instance test]")


def tearDownModule() -> None:
    print("[TearDown pyproxypattern aio instance test]")


class CommonInstanceTest(unittest.TestCase):
    proxy: Proxy

    def setUp(self) -> None:
        print("Proxy setUp")
        self.proxy = Proxy()
        self.loop = asyncio.get_event_loop()

    def tearDown(self) -> None:
        print("Proxy tearDown")

    @async_test
    async def test_class_aio_method(self) -> None:
        class Test_B:
            async def get2(self) -> int:
                return 2
        B = Test_B()
        self.proxy.initialize(B)
        assert (await self.proxy.get2()) == (await B.get2())

    @async_test
    async def test_class_aio_context(self) -> None:
        class LookingGlass:
            def __init__(self, namespace: str) -> None:
                self.namespace = namespace

            def getkey(self, key: str) -> str:
                return f"{self.namespace}::{key}"

            async def __aenter__(self) -> "LookingGlass":
                return self

            async def __aexit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> bool:
                return True

        C = LookingGlass("asdfa")
        self.proxy.initialize(C)
        async with self.proxy as c:
            assert c.getkey("1234") == "asdfa::1234"

    @async_test
    async def test_class_aiogen(self) -> None:
        class ExGen:
            def __init__(self, max_num: int) -> None:
                self.max_num = max_num
                self.i = 0

            def __aiter__(self) -> "ExGen":
                return self

            async def __anext__(self) -> int:
                if self.i >= self.max_num:
                    raise StopAsyncIteration
                self.i += 1
                return self.i

        C = ExGen(10)
        cc = ExGen(10)
        self.proxy.initialize(C)
        for ii, jj in zip([i async for i in C], [j async for j in cc]):
            assert ii == jj
