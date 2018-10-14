from unittest import (
    mock,
    TestCase
)

from RedisProxy.cache import (
    Cache,
    CacheStorage,
    LocalValueNode
)


class LocalValueNodeTest(TestCase):

    def setUp(self):
        self.lvn = LocalValueNode(1)
        self.lvn.timestamp = 10.0

    @mock('time.time', spec_set=True)
    def test_expired(self, mock_time):
        mock_time.return_value = 20.0
        self.assertEqual(False, self.lvn.expired(10))
