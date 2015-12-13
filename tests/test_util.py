from bookish import util


def test_flatten():
    text = [
        "aa",
        "bb",
        {"type": "x", "text": [
            "cc",
        ]},
        "dd",
        {"type": "y", "text": [
            "ee",
            {"type": "z", "text": [
                "ff"
            ]},
            "gg"
        ]},
        "hh"
    ]

    # assert util.flatten_text(text) == "aabbccddeeffgghh"


