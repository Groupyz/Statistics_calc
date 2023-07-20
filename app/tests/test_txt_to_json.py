import os
import json
import pytest
from transformers.txt_to_json import TxtToJsonConverter
from logger import with_logging


@pytest.fixture
def sample_txt_file(tmp_path):
    with open("messages.txt", "w", encoding="utf-8") as txt_file:
        lines = [
            "11/21/22, 22:16 - Omer LeiBo: לא הוא עוד לא ענה, שלחתי לו אתמול עוד תזכורת במייל אבל מחר אני כבר אשלח לו הודעה",
            "11/21/22, 22:21 - Ns: חיה, תודה👌🏿",
        ]
        for line in lines:
            txt_file.write(line + "\n")

    return str(txt_file)


@with_logging
def test_convert_to_json(sample_txt_file):
    expected_json = json.dumps(
        [
            {
                "datetime": {"date": "11/21/22", "time": "22:16"},
                "name": "Omer LeiBo",
                "text": "לא הוא עוד לא ענה, שלחתי לו אתמול עוד תזכורת במייל אבל מחר אני כבר אשלח לו הודעה",
            },
            {
                "datetime": {"date": "11/21/22", "time": "22:21"},
                "name": "Ns",
                "text": "חיה, תודה👌🏿",
            },
        ],
        ensure_ascii=False,
    )
    expected_json = json.loads(expected_json)

    converter = TxtToJsonConverter("messages.txt")
    actual_json = converter.convert_to_json()
    assert actual_json == expected_json
    if os.path.exists("messages.txt"):
        os.remove("messages.txt")
