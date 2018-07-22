from threading import RLock


class LWW:

    def __init__(self):
        self.lww_add_rlock = RLock()
        self.lww_remove_rlock = RLock()
        self.lww_add = {}
        self.lww_remove = {}

    # helper function to add/remove elements from the sets
    @staticmethod
    def add_to_set(lww_set, element, timestamp):

        """
        If the element already exists in the lww_set, check its current timestamp.
        If it is smaller than the one provided -> replace it.
        If it is bigger -> leave it.
        """
        if element in lww_set:
            element_current_timestamp = lww_set[element]
            if element_current_timestamp < timestamp:
                lww_set[element] = timestamp

        # If the element does not exist in the add_set, add it.
        else:
            lww_set[element] = timestamp

    def add(self, element, timestamp):

        with self.lww_add_rlock:
            self.add_to_set(self.lww_add, element, timestamp)

        return True

    def remove(self, element, timestamp):

        with self.lww_remove_rlock:
            self.add_to_set(self.lww_remove, element, timestamp)

        return True
