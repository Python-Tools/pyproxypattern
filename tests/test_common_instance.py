import unittest
from typing import Any
from pyproxypattern import Proxy


def setUpModule() -> None:
    print("[SetUp pyproxypattern common instance test]")


def tearDownModule() -> None:
    print("[TearDown pyproxypattern common instance test]")


class CommonInstanceTest(unittest.TestCase):
    proxy: Proxy

    def setUp(self) -> None:
        print("Proxy setUp")
        self.proxy = Proxy()

    def tearDown(self) -> None:
        print("Proxy tearDown")

    def test_class_attr(self) -> None:
        class Test_A:
            a = 1
        A = Test_A()
        self.proxy.initialize(A)
        assert self.proxy.a == A.a

    def test_class_method(self) -> None:
        class Test_B:
            def get2(self) -> int:
                return 2
        B = Test_B()
        self.proxy.initialize(B)
        assert self.proxy.get2() == B.get2()

    def test_class_context(self) -> None:
        class LookingGlass:
            def __init__(self, namespace: str) -> None:
                self.namespace = namespace

            def getkey(self, key: str) -> str:
                return f"{self.namespace}::{key}"

            def __enter__(self) -> "LookingGlass":
                return self

            def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> bool:
                return True

        C = LookingGlass("asdfa")
        self.proxy.initialize(C)
        with self.proxy as c:
            assert c.getkey("1234") == "asdfa::1234"

    def test_class_gen(self) -> None:
        class ExGen:
            def __init__(self, max_num: int) -> None:
                self.max_num = max_num
                self.i = 0

            def __iter__(self) -> "ExGen":
                return self

            def __next__(self) -> int:
                if self.i >= self.max_num:
                    raise StopIteration
                self.i += 1
                return self.i

        C = ExGen(10)
        cc = ExGen(10)
        self.proxy.initialize(C)
        for ii, jj in zip((i for i in C), (j for j in cc)):
            assert ii == jj
