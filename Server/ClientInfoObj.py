__author__ = 'David'
class ClientInfoObj:
    def __init__(self, user_id, host_name):
        self.user_id = user_id
        self.host_name = host_name

    def print_out(self):
        return "ClientInfoObj - user_id: {0} - host_name: {1}".format(self.user_id, self.host_name)
