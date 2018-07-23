from threading import Thread


class AddThread(Thread):

    def __init__(self, lww_set, element, timestamp):

        Thread.__init__(self)

        self.lww_set = lww_set
        self.element = element
        self.timestamp = timestamp

    def run(self):
        self.lww_set.add(self.element, self.timestamp)
