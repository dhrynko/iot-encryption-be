import os


class BaseConfig(object):
    @property
    def messages_table(self):
        return os.environ.get("messages_table")

    @property
    def encrypted_messages_table(self):
        return os.environ.get("encrypted_messages_table")


config = BaseConfig()
