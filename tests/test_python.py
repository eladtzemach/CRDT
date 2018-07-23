import unittest

from lww import LWW
from tests.lww_threads.add_thread import AddThread
from tests.lww_threads.remove_thread import RemoveThread


class TestPython(unittest.TestCase):

    def setUp(self):
        self.lww = LWW()

    def tearDown(self):
        pass

    def test_lww_1(self):
        self.lww.add("a", 1)
        self.assertTrue(self.lww.exists("a"))
        self.lww.add("b", 1)
        self.assertTrue(self.lww.exists("b"))

    def test_lww_2(self):
        self.lww.add("a", 1)
        self.assertTrue(self.lww.exists("a"))
        self.lww.remove("a", 2)
        self.assertFalse(self.lww.exists("a"))

    def test_lww_3(self):
        self.lww.add("a", 1)
        self.lww.add("b", 1)
        self.lww.add("c", 1)
        self.assertEqual(sorted(self.lww.get()), ['a', 'b', 'c'])

    def test_lww_4(self):
        self.lww.add("a", 1)
        self.lww.add("b", 1)
        self.lww.add("c", 1)
        self.lww.remove("a", 2)
        self.assertEqual(sorted(self.lww.get()), ['b', 'c'])

    def test_lww_5(self):
        self.lww.add("a", 1)
        self.lww.remove("d", 1)
        self.lww.add("b", 1)
        self.lww.remove("e", 1)
        self.lww.add("c", 1)
        self.lww.add("e", 2)
        self.lww.add("d", 2)
        self.assertEqual(sorted(self.lww.get()), ['a', 'b', 'c', 'd', 'e'])

    def test_multiple_threads_1(self):
        element = 'a'
        threads = []

        remove_thread1 = RemoveThread(self.lww, element, 2)
        threads.append(remove_thread1)
        add_thread1 = AddThread(self.lww, element, 3)
        threads.append(add_thread1)
        remove_thread2 = RemoveThread(self.lww, element, 4)
        threads.append(remove_thread2)

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertFalse(self.lww.exists(element))

    def test_multiple_threads_2(self):
        element = 'b'
        threads = []

        remove_thread1 = RemoveThread(self.lww, element, 4)
        threads.append(remove_thread1)
        add_thread1 = AddThread(self.lww, element, 5)
        threads.append(add_thread1)
        remove_thread2 = RemoveThread(self.lww, element, 6)
        threads.append(remove_thread2)

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertFalse(self.lww.exists(element))

    def test_multiple_threads_3(self):
        element = 'c'
        threads = []

        remove_thread1 = RemoveThread(self.lww, element, 7)
        threads.append(remove_thread1)
        add_thread1 = AddThread(self.lww, element, 8)
        threads.append(add_thread1)
        remove_thread2 = RemoveThread(self.lww, element, 9)
        threads.append(remove_thread2)

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertFalse(self.lww.exists(element))

if __name__ == '__main__':
    unittest.main()
