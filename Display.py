from utils import sum_lists, ndrange
from Structures import Block, Coord
from Game import Grid
import functools
import tkinter


class Display:

	def __init__(self, grd:Grid, scale:float = 10.0, border:int = 3):
		self.scale = scale
		self.border = border
		self.slope_scale = (3.0 ** 0.5)/2.0
		self.grd = grd
		self.main = tkinter.Tk()
		self.width, self.height = self.scale * self.slope_scale * self.grd.size * 2.0, self.scale * self.grd.size * 2.0
		self.cnv = tkinter.Canvas(self.main, width = self.width + 2 * self.border, height = self.height + 2 * self.border)

	@classmethod
	def get_display_coords(cls, crd:Coord) -> tuple[float, float]:
		return (
			crd.y - crd.x,
			2 * crd.z - (crd.x + crd.y)
		)

	def get_pixel_coords(self, xy:tuple[float, float]):
		return (
			self.border + 0.5 * self.width + self.scale * self.slope_scale * xy[0],
			self.border + 0.5 * self.height - self.scale * xy[1] * 0.5
		)


	def paint_block_side(self, block:Block, side:int, color:str) -> None:
		corners = []
		if side == 0:
			#top
			corners = [
				block.corner(True, True, True),
				block.corner(True, False, True),
				block.corner(False, False, True),
				block.corner(False, True, True),
			]
		elif side == 1:
			#left
			corners = [
				block.corner(True, True, True),
				block.corner(True, False, True),
				block.corner(True, False, False),
				block.corner(True, True, False),
			]
		elif side == 2:
			#right
			corners = [
				block.corner(True, True, True),
				block.corner(False, True, True),
				block.corner(False, True, False),
				block.corner(True, True, False),
			]
		corner_coords = [self.get_pixel_coords(self.get_display_coords(crd)) for crd in corners]
		self.cnv.create_polygon(
			corner_coords[0][0],
			corner_coords[0][1],
			corner_coords[1][0],
			corner_coords[1][1],
			corner_coords[2][0],
			corner_coords[2][1],
			corner_coords[3][0],
			corner_coords[3][1],
			fill = color
		)
		


	def place_tri(self, crd:Coord, side:bool, color:str):
		#false = left, true = right
		ref_x, ref_y = self.scale * self.slope_scale * (crd.y - crd.x), self.scale * (crd.z - (crd.x + crd.y)/2.0)
		ref_x += 300
		ref_y -= 300
		self.cnv.create_polygon([
			ref_x,
			self.height - ref_y, 
			ref_x,
			self.height - ref_y + self.scale,
			ref_x + self.scale * self.slope_scale * (1 if side else -1),
			self.height - ref_y + 0.5 * self.scale
			], fill = color)

	def place_side(self, crd:Coord, side:int):
		#0 = top, 1 = left, 2 = right
		if side == 0:
			self.place_tri(crd, False, "red")
			self.place_tri(crd, True, "red")
		elif side == 1:
			self.place_tri(crd.shift(Coord(1, 1, 0)), False, "blue")
			self.place_tri(crd.shift(Coord(1, 0, 0)), True, "blue")
		elif side == 2:
			self.place_tri(crd.shift(Coord(0, 1, 0)), False, "yellow")
			self.place_tri(crd.shift(Coord(1, 1, 0)), True, "yellow")

	def place_block(self, crd:Coord):
		ref_x, ref_y = self.scale * self.slope_scale * (crd.y - crd.x), self.height - self.scale * (crd.z - (crd.x + crd.y)/2.0)
		ref_x += 300
		ref_y += 300
		radius = 0.01 * self.scale
		
		self.place_side(crd, 0)
		self.place_side(crd, 1)
		self.place_side(crd, 2)

	def display(self):
		data = self.grd.as_lst()
		for z in range(self.grd.size):
			for x in range(self.grd.size):
				for y in range(self.grd.size):
					if data[z][y][x] > 0:
						self.place_block(Coord(x, y, z))
						
		self.cnv.pack(fill = 'both', expand = 1)

	def display_v2(self):
		self.cnv.delete("all")
		for block in self.grd.blocks:
			
			self.paint_block_side(block, 1, "yellow")

			self.paint_block_side(block, 2, "blue")
			self.paint_block_side(block, 0, "red")
			pass
		for block in self.grd.blocks:
			#self.paint_block_side(block, 0, "red")
			#self.paint_block_side(block, 1, "yellow")
			#self.paint_block_side(block, 2, "blue")
			pass
		for block in self.grd.blocks:
			#self.paint_block_side(block, 0, "red")
			#self.paint_block_side(block, 1, "yellow")
			#self.paint_block_side(block, 2, "blue")
			pass
		self.cnv.pack()

if __name__ == "__main__":
	g = Grid(50)
	#g.add(Coord(1, 0, 0), Coord(10, 1, 1), 1)
	#g.add(Coord(9, 0, 1), Coord(10, 1, 8), 1)
	#g.add(Coord(9, 0, 7), Coord(10, 9, 8), 1)
	#g.add(Coord(0, 0, 0), Coord(1, 1, 1), 1)
	
	g.add(Coord(0, 0, 0), Coord(10, 1, 1), 1)
	g.add(Coord(0, 0, 1), Coord(1, 1, 10), 1)
	g.add(Coord(9, 0, 1), Coord(10, 1, 20), 1)
	g.add(Coord(9, 0, 19), Coord(10, 10, 20), 1)
	
	# g.add(Coord(0, -1, -1), Coord(9, 0, 0), 1)

	# g.add(Coord(9, 0, 0), Coord(10, 1, 50), 1)

	# g.add(Coord(9, 1, 0), Coord(10, 9, 1), 1)
	# g.add(Coord(9, 1, 10), Coord(10, 9, 11), 1)
	# g.add(Coord(9, 1, 20), Coord(10, 9, 21), 1)
	# g.add(Coord(9, 1, 30), Coord(10, 9, 31), 1)



	# g.add(Coord(9, 9, 0), Coord(10, 10, 50), 1)

	


	


	
	#g.print()
	d = Display(g, scale = 10, border = 3)
	d.display_v2()
	d.main.mainloop()








