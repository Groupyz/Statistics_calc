import json
from logger import with_logging


class TxtToJsonConverter:
    def __init__(self, file_path):
        self.file_path = file_path

    @with_logging
    def convert_to_json(self) -> list[dict]:
        messages = []
        with open(self.file_path, "r", encoding="utf8") as file:
            for line in file:
                line = line.strip()
                if line:
                    message = self.parse_message(line)
                    if message:
                        messages.append(message)

        json_data = json.dumps(messages, ensure_ascii=False)
        json_data = json.loads(json_data)
        return json_data

    @staticmethod
    def parse_message(line: str) -> dict:
        try:
            datetime_part, rest = line.split("-", 1)
            date_str, time_str = datetime_part.strip().split(" ", 1)
            date_str = date_str.replace(",", "")
            name, text = rest.strip().split(":", 1)

            message = {
                "datetime": {"date": date_str, "time": time_str},
                "name": name.strip(),
                "text": text.strip(),
            }

            return message
        except ValueError:
            return None
