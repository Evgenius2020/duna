import csv
import uuid
from datetime import datetime


class CSVLogger:
    def __init__(self):
        self.filename = f"logs/{uuid.uuid4()}.csv"

    def log(self, values: list[str]):
        timestamp = datetime.now().isoformat()
        with open(
            self.filename, mode='a', newline='', encoding='utf-8'
        ) as log_file:
            csv.writer(log_file).writerow([timestamp] + values)
