import unittest
import redis

from lww_redis import LWWRedis
from tests.lww_threads.add_thread import AddThread
from tests.lww_threads.remove_thread import RemoveThread

# setting up redis connection on localhost, making sure we decode the returned byte string
redis_connection = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)


class TestRedis(unittest.TestCase):

    def setUp(self):
        self.lww = LWWRedis(redis_connection)

    def tearDown(self):
        # remove all elements between the lowest (0) and highest (-1) scores
        redis_connection.zremrangebyrank('lww_add', 0, -1)
        redis_connection.zremrangebyrank('lww_remove', 0, -1)

    def test_lww_redis_1(self):
        self.lww.add("a", 1)
        self.assertTrue(self.lww.exists("a"))
        self.lww.add("b", 1)
        self.assertTrue(self.lww.exists("b"))

    def test_lww_redis_2(self):
        self.lww.add("a", 1)
        self.assertTrue(self.lww.exists("a"))
        self.lww.remove("a", 2)
        self.assertFalse(self.lww.exists("a"))

    def test_lww_redis_3(self):
        self.lww.add("a", 1)
        self.lww.add("b", 1)
        self.lww.add("c", 1)
        self.assertEqual(sorted(self.lww.get()), ['a', 'b', 'c'])

    def test_lww_redis_4(self):
        self.lww.add("a", 1)
        self.lww.add("b", 1)
        self.lww.add("c", 1)
        self.lww.remove("a", 2)
        self.assertEqual(sorted(self.lww.get()), ['b', 'c'])

    def test_lww_redis_5(self):
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
