import os
import datetime

LOGS_FOLDER = os.path.join(os.path.dirname(__file__), 'logs')


class Logger:
    _names = {}
    def __new__(cls, *args, **kwargs):
        name = args[0]
        if not cls._names.get(args[0]):
            new_logger = super().__new__(cls)
            new_logger.name = name
            new_logger.log_file = os.path.join(LOGS_FOLDER, f'{name}.log')
            cls._names[name] = new_logger
        return cls._names[name]

    def write(self, event: str):
        record = f'[{datetime.datetime.now()}] [{self.name}] [{event}]\n'
        with open(self.log_file, 'a') as f:
            f.write(record)
