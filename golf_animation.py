
from manim import *
from shapely.geometry import Polygon as ShapelyPolygon, box
from golf_data import (
    YARD, OBSTACLES, START, HOLE, GOLFERS,
    TITLE, PREVIOUS_SCORES,
)


FLIGHT_TIME = 1.2
PAUSE_AFTER_SHOT = 0.25
MIN_ARC_HEIGHT = 0.12
MAX_ARC_HEIGHT = 0.65
ARC_HEIGHT_FACTOR = 0.18
BALL_RADIUS = 0.065
LANDING_RADIUS = 0.035


class BackyardGolf(Scene):
    def xy(self, point):
        x, y = point
        return np.array([
            (x - YARD["width"] / 2) * self.scale,
            (y - YARD["height"] / 2) * self.scale - 0.1,
            0,
        ])

    def make_lawn_stripes(self):
        stripes = VGroup()
        stripe_width = 8  # feet
        colors = ["#A8D58D", "#70B85A"]

        width = YARD["width"]
        height = YARD["height"]
        yard_shape = box(0, 0, width, height)

        x = -height
        index = 0

        while x < width:
            band = ShapelyPolygon([
                (x, 0),
                (x + stripe_width, 0),
                (x + stripe_width + height, height),
                (x + height, height),
            ])

            clipped = band.intersection(yard_shape)

            if not clipped.is_empty:
                polygons = [clipped] if clipped.geom_type == "Polygon" else list(clipped.geoms)

                for poly in polygons:
                    if poly.geom_type == "Polygon":
                        points = [self.xy((px, py)) for px, py in list(poly.exterior.coords)[:-1]]
                        stripes.add(Polygon(*points, stroke_width=0, fill_color=colors[index % 2], fill_opacity=1))

            x += stripe_width
            index += 1

        return stripes

    def construct(self):
        self.camera.background_color = "#19251D"

        self.scale = min(
            10.0 / YARD["width"],
            5.3 / YARD["height"],
        )

        # ----------------------------
        # Draw the yard
        # ----------------------------

        yard = Rectangle(
            width=YARD["width"] * self.scale,
            height=YARD["height"] * self.scale,
            stroke_color=WHITE,
            stroke_width=1.5,
            fill_color="#315C38",
            fill_opacity=1,
        ).move_to(
            self.xy((YARD["width"] / 2, YARD["height"] / 2))
        )

        self.add(yard)

        self.add(self.make_lawn_stripes())

        for obstacle in OBSTACLES:
            center = (
                obstacle["x"] + obstacle["width"] / 2,
                obstacle["y"] + obstacle["height"] / 2,
            )

            rect = Rectangle(
                width=obstacle["width"] * self.scale,
                height=obstacle["height"] * self.scale,
                stroke_color="#E5E5E5",
                stroke_width=1,
                fill_color=obstacle["color"],
                fill_opacity=1,
            ).move_to(self.xy(center))

            label = Text(
                obstacle["name"],
                font_size=14,
                color=WHITE,
            ).move_to(self.xy(center))

            self.add(rect, label)

        # Tee marker.
        self.add(
            Dot(self.xy(START), radius=0.07, color=WHITE),
            Text("START", font_size=13).next_to(
                self.xy(START), DOWN, buff=0.08
            ),
        )

        # Hole: cup, flagpole, and red triangular flag.
        self.add(
            Circle(
                radius=0.10,
                color=WHITE,
                stroke_width=2,
            ).move_to(self.xy(HOLE)),
            Dot(self.xy(HOLE), radius=0.035, color=BLACK),
        )

        flagpole = Line(
            self.xy(HOLE),
            self.xy(HOLE) + UP * 0.42,
            color=WHITE,
            stroke_width=2,
        )

        flag = Triangle(
            color=RED,
            fill_color=RED,
            fill_opacity=1,
            stroke_width=0,
        ).scale(0.16)

        flag.rotate(-PI / 2)
        flag.move_to(self.xy(HOLE) + UP * 0.32 + RIGHT * 0.13)

        self.add(flagpole, flag)

        # Configurable title.
        title = Text(TITLE, font_size=25)
        title.to_edge(UP, buff=0.2)
        self.add(title)

        # ----------------------------
        # Scoreboard
        # ----------------------------

        strokes = {name: 0 for name in GOLFERS}

        def make_scoreboard():
            rows = [
                Text("SCORES", font_size=19, color=WHITE),
                Text("Hole | Total", font_size=13, color=WHITE),
            ]

            for name, data in GOLFERS.items():
                hole_score = strokes[name]
                total_score = (
                    PREVIOUS_SCORES.get(name, 0) + hole_score
                )

                rows.append(
                    Text(
                        f"{name}: {hole_score} | {total_score}",
                        font_size=15,
                        color=data["color"],
                    )
                )

            panel = VGroup(*rows).arrange(
                DOWN, aligned_edge=LEFT, buff=0.14
            )
            return panel

        scoreboard = make_scoreboard()
        scoreboard.to_edge(RIGHT, buff=0.2)
        scoreboard.shift(UP * 0.2)
        self.add(scoreboard)

        # The old bottom shot label is intentionally disabled.
        # status = Text("Ready to play", font_size=21)
        # status.to_edge(DOWN, buff=0.2)
        # self.add(status)

        # ----------------------------
        # Curved shot path
        # ----------------------------

        def make_shot_path(start, end, curve_side=1):
            p0 = self.xy(start)
            p2 = self.xy(end)

            direction = p2 - p0
            distance = np.linalg.norm(direction[:2])

            if distance < 1e-8:
                return Line(p0, p2)

            perpendicular = np.array([
                -direction[1] / distance,
                direction[0] / distance,
                0,
            ])

            height = np.clip(
                distance * ARC_HEIGHT_FACTOR,
                MIN_ARC_HEIGHT,
                MAX_ARC_HEIGHT,
            )

            p1 = (
                (p0 + p2) / 2
                + perpendicular * height * curve_side
            )

            def bezier(t):
                return (
                    (1 - t) ** 2 * p0
                    + 2 * (1 - t) * t * p1
                    + t ** 2 * p2
                )

            return ParametricFunction(
                bezier,
                t_range=[0, 1],
                color=WHITE,
                stroke_width=2.5,
            )

        # ----------------------------
        # Animate shots in turn order
        # ----------------------------

        while any(
            strokes[name] < len(data["shots"]) - 1
            for name, data in GOLFERS.items()
        ):
            for name, data in GOLFERS.items():
                shot_index = strokes[name]

                if shot_index >= len(data["shots"]) - 1:
                    continue

                start = data["shots"][shot_index]
                end = data["shots"][shot_index + 1]
                color = data["color"]

                ball = Dot(
                    self.xy(start),
                    radius=BALL_RADIUS,
                    color=color,
                    stroke_color=WHITE,
                    stroke_width=0.8,
                )
                self.add(ball)

                # Player name follows the moving ball.
                player_label = Text(
                    name,
                    font_size=15,
                    color=color,
                )
                player_label.add_updater(
                    lambda m, b=ball: m.next_to(
                        b, RIGHT, buff=0.09
                    )
                )
                self.add(player_label)

                curve_side = 1 if shot_index % 2 == 0 else -1
                path = make_shot_path(
                    start, end, curve_side
                )
                path.set_color(color)

                self.play(
                    MoveAlongPath(ball, path),
                    Create(path),
                    run_time=FLIGHT_TIME,
                    rate_func=smooth,
                )

                player_label.clear_updaters()
                self.remove(player_label, ball)

                # Permanent marker at the landing point.
                self.add(
                    Dot(
                        self.xy(end),
                        radius=BALL_RADIUS,
                        color=color,
                    )
                )

                strokes[name] += 1

                # Refresh the cumulative and current-hole scores.
                new_scoreboard = make_scoreboard()
                new_scoreboard.to_edge(RIGHT, buff=0.2)
                new_scoreboard.shift(UP * 0.2)

                self.remove(scoreboard)
                scoreboard = new_scoreboard
                self.add(scoreboard)

                self.wait(PAUSE_AFTER_SHOT)

        # ----------------------------
        # Final scores
        # ----------------------------

        final_rows = [
            Text("SCORES", font_size=25, color=WHITE)
        ]

        for name, data in GOLFERS.items():
            hole_score = strokes[name]
            total_score = (
                PREVIOUS_SCORES.get(name, 0) + hole_score
            )

            final_rows.append(
                Text(
                    f"{name}: {total_score} total "
                    f"(+{hole_score} this hole)",
                    font_size=18,
                    color=data["color"],
                )
            )

        final_panel = VGroup(*final_rows).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18
        )
        final_panel.to_edge(RIGHT, buff=0.2)

        self.play(Transform(scoreboard, final_panel))
        self.wait(3)
