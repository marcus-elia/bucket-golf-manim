TITLE = "Bucket Golf - Hole 1"

PREVIOUS_SCORES = {
    "Beard": 0,
    "Pants": 0,
    "Shades": 0,
    "Golf Man": 0,
}

YARD = {
    "width": 180,
    "height": 140,
}

OBSTACLES = [
    {
        "name": "House",
        "x": 55, "y": 65,
        "width": 50, "height": 30,
        "color": "#858585",
    },
    {
        "name": "Garage",
        "x": 30, "y": 80,
        "width": 25, "height": 24,
        "color": "#B09A83",
    },
    {
        "name": "Garden",
        "x": 150, "y": 65,
        "width": 8, "height": 16,
        "color": "#795548",
    },
    {
        "name": "Driveway",
        "x": 31, "y": 0,
        "width": 23, "height": 80,
        "color": "#050505",
    },
]

START = (8, 45)
HOLE = (55, 120)

GOLFERS = {
    "Beard": {
        "color": "#ffffff",
        "shots": [
            (8, 45),
            (8, 110),
            (13, 100),
            (59, 124),
            (51, 116),
            (55, 120)
        ],
    },
    "Pants": {
        "color": "#c78006",
        "shots": [
            (8, 45),
            (35, 120),
            (70, 118),
            (65, 119),
            (55, 120),
        ],
    },
    "Shades": {
        "color": "#3492eb",
        "shots": [
            (8, 45),
            (40, 110),
            (55, 121),
            (55, 120),
        ],
    },
    "Golf Man": {
            "color": "#4f4f4f",
            "shots": [
                (8, 45),
                (40, 125),
                (58, 124),
                (55, 120),
            ],
        }
}
