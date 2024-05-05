from dataclasses import dataclass


@dataclass
class Coord:
    x: int
    y: int
    z: int

    @classmethod
    def is_between(cls, lower: "Coord", test: "Coord", upper: "Coord") -> bool:
        return cls.is_above(upper, test, False) and cls.is_above(test, lower, True)

    @classmethod
    def is_above(cls, upper: "Coord", test: "Coord", allow_same: bool) -> bool:
        if allow_same:
            return upper.x >= test.x and upper.y >= test.y and upper.z >= test.z
        return upper.x > test.x and upper.y > test.y and upper.z > test.z

    def shift(self, delta: "Coord") -> "Coord":
        return Coord(self.x + delta.x, self.y + delta.y, self.z + delta.z)

    def rotate(self, pitch, yaw, roll, size):
        x, y, z = self.x, self.y, self.z
        for i in range(pitch):
            x, z = size - z, x
        for i in range(yaw):
            x, y = size - y, x
        for i in range(roll):
            y, z = size - z, y
        return Coord(x, y, z)

    def is_unit(self) -> bool:
        return (
            (self.x == 1 and self.y == 0 and self.z == 0)
            or (self.x == -1 and self.y == 0 and self.z == 0)
            or (self.x == 0 and self.y == 1 and self.z == 0)
            or (self.x == 0 and self.y == -1 and self.z == 0)
            or (self.x == 0 and self.y == 0 and self.z == 1)
            or (self.x == 0 and self.y == 0 and self.z == -1)
        )

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z


@dataclass
class Block:
    lower: Coord
    upper: Coord
    grd: "Grid"
    weight: int = 1

    def as_lst(self) -> list[list[list[int]]]:
        return [
            [
                [
                    self.weight
                    if (Coord.is_between(self.lower, Coord(x, y, z), self.upper))
                    else 0
                    for x in range(self.grd.size)
                ]
                for y in range(self.grd.size)
            ]
            for z in range(self.grd.size)
        ]

    def rotated(self, pitch: int, yaw: int, roll: int) -> "Block":
        c0 = self.lower.rotate(pitch, yaw, roll)
        c1 = self.upper.rotate(pitch, yaw, roll)
        return Block(
            Coord(min(c0.x, c1.x), min(c0.y, c1.y), min(c0.z, c1.z)),
            Coord(max(c0.x, c1.x), max(c0.y, c1.y), max(c0.z, c1.z)),
            self.grd,
            self.weight,
        )

    def corner(self, x: bool, y: bool, z: bool) -> Coord:
        # note: upper is toward viewer, lower is away.
        return Coord(
            self.upper.x if x else self.lower.x,
            self.upper.y if y else self.lower.y,
            self.upper.z if z else self.lower.z,
        )

    def contains(self, crd: Coord) -> int:
        return self.weight if Coord.is_between(self.lower, crd, self.upper) else 0


class Ladder:
    pass


class Button:
    pass


@dataclass
class Door:
    crd: Coord
    facing: int
    link: "Door"
    gm: "Game"

    @classmethod
    def pair(
        a_crd: Coord, a_facing: int, b_crd: Coord, b_facing: int, gm: "Game"
    ) -> tuple["Door"]:
        door_a, door_b = (
            Door(a_crd, a_facing, None, gm),
            Door(b_crd, b_facing, None, gm),
        )
        door_a.link, door_b.link = door_b, door_a
        return door_a, door_b
