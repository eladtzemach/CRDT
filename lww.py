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
        If the element already exists in lww_set, check its current timestamp.
        If it is smaller than the one provided -> replace it.
        If it is bigger -> leave it.
        """
        if element in lww_set:
            element_current_timestamp = lww_set[element]
            if element_current_timestamp < timestamp:
                lww_set[element] = timestamp

        # if the element does not exist in lww_add, add it
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

    def exists(self, element):

        # if element is not in lww_add
        if element not in self.lww_add:
            return False

        # elif the element has a larger timestamp in lww_add
        elif element in self.lww_add and element in self.lww_remove \
                and self.lww_add[element] >= self.lww_remove[element]:
            return True

        # elif element is not in lww_remove (but it is in lww_add)
        elif element not in self.lww_remove:
            return True

        else:
            return False

    def get(self):

        lww_result = []

        # for each element in lww_add, make sure it exists
        for element in self.lww_add:
            if self.exists(element):
                lww_result.append(element)

        return lww_result
