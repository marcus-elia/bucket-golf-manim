TITLE = "Backyard Golf - Hole 1"

PREVIOUS_SCORES = {
    "Alex": 0,
    "Jordan": 0,
    "Sam": 0,
}

YARD = {
    "width": 100,
    "height": 70,
}

OBSTACLES = [
    {
        "name": "House",
        "x": 10, "y": 35,
        "width": 35, "height": 25,
        "color": "#858585",
    },
    {
        "name": "Garage",
        "x": 60, "y": 45,
        "width": 20, "height": 15,
        "color": "#B09A83",
    },
    {
        "name": "Garden Bed",
        "x": 55, "y": 10,
        "width": 20, "height": 8,
        "color": "#795548",
    },
]

START = (5, 5)
HOLE = (90, 60)

GOLFERS = {
    "Alex": {
        "color": "#42A5F5",
        "shots": [
            (5, 5),
            (25, 15),
            (45, 20),
            (70, 30),
            (90, 60),
        ],
    },
    "Jordan": {
        "color": "#FFCA28",
        "shots": [
            (5, 5),
            (20, 25),
            (45, 30),
            (75, 35),
            (90, 60),
        ],
    },
    "Sam": {
        "color": "#EF5350",
        "shots": [
            (5, 5),
            (30, 10),
            (50, 25),
            (80, 45),
            (90, 60),
        ],
    },
}
