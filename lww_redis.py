from threading import RLock


class LWWRedis:

    def __init__(self, redis):
        self.lww_add_rlock = RLock()
        self.lww_remove_rlock = RLock()
        self.lww_redis = redis

    # helper function to add/remove elements from the sets
    def add_to_set(self, lww_set, element, timestamp):

        """
        If the element already exists in lww_set, check its current timestamp.
        If it is smaller than the one provided -> replace it.
        If it is bigger -> leave it.
        """
        element_current_timestamp = self.lww_redis.zscore(lww_set, element)
        if element_current_timestamp:
            if element_current_timestamp < timestamp:
                self.lww_redis.zadd(lww_set, timestamp, element)

        # if the element does not exist in lww_set, add it
        else:
            self.lww_redis.zadd(lww_set, timestamp, element)

    def add(self, element, timestamp):

        with self.lww_add_rlock:
            self.add_to_set("lww_add", element, timestamp)

        return True

    def remove(self, element, timestamp):

        with self.lww_remove_rlock:
            self.add_to_set("lww_remove", element, timestamp)

        return True

    def exists(self, element):

        add_timestamp = self.lww_redis.zscore("lww_add", element)
        remove_timestamp = self.lww_redis.zscore("lww_remove", element)

        # if no timestamp in "lww_add", element is not there
        if not add_timestamp:
            return False
        # elif not in "lww_remove" but in "lww_add", element is there
        elif not remove_timestamp:
            return True
        # elif both there, compare timestamps
        elif add_timestamp and remove_timestamp and (add_timestamp >= remove_timestamp):
            return True
        else:
            return False

    def get(self):

        lww_result = []

        # for each element in lww_add, make sure it exists
        for element in self.lww_redis.zrange("lww_add", 0, -1):
            if self.exists(element):
                lww_result.append(element)

        return lww_result
