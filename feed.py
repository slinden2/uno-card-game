import datetime


class Feed:
    """Class to display what happens in the game
    in feed format.

    :param msg_qty: The number of messages saved.
    """

    def __init__(self, msg_qty):
        self.messages = []
        self.max_msg = msg_qty

    def add_msg(self, msg):
        self.messages.append((self.get_time_now(), msg))
        self._check_qty()

    def _check_qty(self):
        if len(self.messages) > self.max_msg:
            qty_to_remove = len(self.messages) - self.max_msg
            self.messages = self.messages[qty_to_remove:]

    def reset(self):
        self.messages = self.messages[:]

    @staticmethod
    def get_time_now():
        dt = datetime.datetime.now()
        return dt.strftime("%H:%M:%S")
