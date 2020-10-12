from twilio.rest import Client


class CallQueue:
    def __init__(self, name):
        self.name = name
        self.client = Client()
        self.sid = self._create()

    def __repr__(self):
        return f"{self.name} ({self.sid})"

    def _create(self):
        current_queues = self.client.queues.list()
        for queue in current_queues:
            if self.name == queue.friendly_name:
                return queue.sid
        else:
            new_queue = self.client.queues.create(friendly_name=self.name)
            return new_queue.sid

    def size(self):
        queue = self.client.queues(self.sid).fetch()
        return queue.current_size
