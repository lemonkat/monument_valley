from dataclasses import dataclass, field
import functools
from utils import sum_lists, ndrange

from Structures import Coord, Block, Ladder, Button, Door

@dataclass
class Grid:
	size:int
	blocks:list[Block] = field(default_factory = list)
	doors:list[Door] = field(default_factory = list)
	ladders:list[Ladder] = field(default_factory = list)

	def as_lst(self):
		return functools.reduce(
			sum_lists, 
			(
				block.as_lst() 
				for block in self.blocks
			), 
			[
				[
					[
						0 
						for x in range(self.size)
					] 
					for j in range(self.size)
				] 
				for k in range(self.size)
			]
		)

	def print(self):
		lst = self.as_lst()
		for layer in range(self.size):
			print("Layer " + str(layer) + ": ")
			print("\n".join("".join((str(item) for item in row)) for row in lst[layer]))

	def add(self, lower, upper, weight):
		self.blocks.append(Block(lower, upper, self, weight))


	def get(self, crd: Coord) -> int:
		return sum([block.contains(crd) for block in self.blocks])

# @dataclass
# class Player:
# 	crd:Coord
# 	facing:int
# 	lv:"Level"

# 	def display(self) -> None:
# 		#display the character on the coordinate board.
# 		pass

# 	def can_move(self, direction:Coord) -> bool:
# 		#check if this player can move to this position
# 		if not coord.is_unit():
# 			return False
# 		target = self.crd.shift(direction)
# 		if direction.z == 0:
# 			if lv.grd.get(target) != 0:
# 				return gm.is_door_at(target, (direction + 2) % 4)
# 				#must be empty space there, possibly a door
# 			if lv.grd.get(target.shift(Coord(0, 0, -1))) == 0:
# 				return False #must be floor
# 			return True
# 		else:
# 			pass
# 			#check if ladder is there

# class Level:

# 	def __init__(self, size:int):
# 		self.players = []
# 		self.grd = Grid(size)

# 	def add_player(self, crd:Coord, facing:int) -> None:
# 		self.players.append(Player(crd, facing, self))

# 	def is_door_at(self, crd:Coord, facing:int) -> bool:
# 		for door in self.grd.doors:
# 			if door.crd == crd:
# 				pass

		


