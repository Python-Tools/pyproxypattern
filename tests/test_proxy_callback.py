import unittest
from pyproxy import Proxy
from aiounittest import async_test


def setUpModule() -> None:
    print("[SetUp pyproxypattern proxy callback test]")


def tearDownModule() -> None:
    print("[TearDown pyproxypattern proxy callback test]")


class ProxyCallbackTest(unittest.TestCase):
    proxy: Proxy

    def setUp(self) -> None:
        print("Proxy setUp")
        self.proxy = Proxy()

    def tearDown(self) -> None:
        print("Proxy tearDown")

    def test_regist_callback(self) -> None:
        class Test_B:
            def get2(self) -> int:
                return 2
        B = Test_B()
        self.proxy.attach_callback(lambda x: self.assertEqual(x.get2(), 2))
        self.proxy.initialize(B)
        assert self.proxy.get2() == B.get2()

    def test_regist_typecheck(self) -> None:
        class Test_B:
            def get2(self) -> int:
                return 2
        B = Test_B()
        self.proxy.attach_instance_check(lambda x: isinstance(x, Test_B))
        self.proxy.initialize(B)
        assert self.proxy.get2() == B.get2()

    def test_regist_typecheck_notpass(self) -> None:
        class Test_B:
            def get2(self) -> int:
                return 2
        B = Test_B()
        self.proxy.attach_instance_check(lambda x: isinstance(x, str))
        with self.assertRaisesRegex(AttributeError, '实例校验失败'):
            self.proxy.initialize(B)

    def test_regist_when_init(self) -> None:
        class Test_B:
            def get2(self) -> int:
                return 2
        B = Test_B()
        self.proxy = Proxy(B)
        assert self.proxy.get2() == B.get2()

    def test_set_attr_in_proxy(self) -> None:
        class Test_B:
            def get2(self) -> int:
                return 2
        B = Test_B()
        self.proxy.initialize(B)
        with self.assertRaisesRegex(AttributeError, 'Cannot set attribute on proxy.'):
            self.proxy.a = 12

    @async_test
    async def test_uninitialize(self) -> None:

        with self.assertRaisesRegex(AttributeError, 'Cannot use uninitialized Proxy.'):
            self.proxy.get2()

        with self.assertRaisesRegex(AttributeError, 'Cannot use uninitialized Proxy.'):
            for i in self.proxy:
                print(i)

        with self.assertRaisesRegex(AttributeError, 'Cannot use uninitialized Proxy.'):
            async with self.proxy:
                print(1)
