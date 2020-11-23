import os
import sys
import unittest
from pathlib import Path
from typing import Dict, Any


from pyproxypattern import Proxy, Optional


def setUpModule() -> None:
    print("[SetUp pyproxypattern common instance test]")


def tearDownModule() -> None:
    print("[TearDown pyproxypattern common instance test]")


class CommonInstanceTest(unittest.TestCase):
    proxy: Optional[Proxy]

    def setUp(self) -> None:
        print("instance setUp")
        self.proxy = Proxy()

    def tearDown(self) -> None:
        print("instance tearDown")
        self.proxy = None

    def test_class_attr(self) -> None:
        class Test_A:
            a = 1
        A = Test_A()
        self.proxy.initialize(A)
        assert self.proxy.a == A.a

    def test_class_attr(self) -> None:
        class Test_A:
            a = 1
        A = Test_A()
        self.proxy.initialize(A)
        assert self.proxy.a == A.a

    def test_class_method(self) -> None:
        class Test_B:
            def get2(self):
                return 2
        B = Test_B()
        self.proxy.initialize(B)
        assert self.proxy.get2() == B.get2()

    def test_class_context(self) -> None:
        class LookingGlass:
            def __init__(self, namespace):
                self.namespace = namespace

            def getkey(key):
                return f"{self.namespace}::{key}"

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_value, traceback):
                return True

        C = LookingGlass("asdfa")
        self.proxy.initialize(C)
        with self.proxy as c:
            assert c.getkey("1234") == "asdfa::1234"
