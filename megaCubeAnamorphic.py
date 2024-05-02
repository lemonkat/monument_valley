from StructuresV3 import Structure, Display
import numpy as np
import random
import copy
import math

st = Structure((30, 30, 30))
st.fill((0, 0, 0), (21, 1, 1,), 1)
st.fill((0, 0, 0), (1, 21, 1,), 1)
st.fill((0, 0, 0), (1, 1, 21,), 1)
st.fill((20, 0, 0), (21, 1, 21), 1)
st.fill((20, 0, 0), (21, 21, 1), 1)
st.fill((0, 20, 0), (1, 21, 21), 1)
st.fill((0, 20, 0), (21, 21, 1), 1)
st.fill((0, 0, 20), (21, 1, 21), 1)
st.fill((0, 0, 20), (1, 21, 21), 1)
st.fill((0, 20, 20), (21, 21, 21), 1)
st.fill((20, 0, 20), (21, 21, 21), 1)
st.fill((20, 20, 0), (21, 21, 21), 1)
st.fill((11, 5, 21), (12, 22, 22), 1)
st.fill((5, 11, 21), (22, 12, 22), 1)
st.fill((10, 1, 20), (11, 4, 21), 1)
st.fill((1, 10, 20), (4, 11, 21), 1)
st.fill((10, 0, 10), (11, 1, 20), 1)
st.fill((0, 10, 10), (1, 11, 20), 1)
st.fill((21, 11, 15), (22, 12, 22), 1)
st.fill((20, 10, 0), (21, 11, 14), 1)
st.fill((21, 2, 11), (22, 22, 12), 1)
st.set((20, 11, 11), 1)
st.fill((10, 0, 10), (20, 1, 11), 1)
st.fill((10, 10, 0), (20, 11, 1), 1)
st.fill((11, 21, 15), (12, 22, 22), 1)
st.fill((10, 20, 0), (11, 21, 14), 1)
st.fill((2, 21, 11), (22, 22, 12), 1)
st.set((11, 20, 11), 1)
st.fill((0, 10, 10), (1, 20, 11), 1)
st.fill((10, 10, 0), (11, 20, 1), 1)


mx = 45
result = [[[0 for i in range(mx)] for j in range(mx)] for k in range(mx)]


grid = st.data
for x in range(grid.shape[0] - 1, -1 , -1):
	for y in range(grid.shape[1] - 1, -1 , -1):
		for z in range(grid.shape[2] - 1, -1 , -1):
			if grid[x][y][z]:
				bound = 0
				check_x = x
				check_y = y
				check_z = z
				while max(check_x, check_y, check_z) < mx - 1:
					if result[check_z][check_y][check_x]:
						break
					if result[check_z + 1][check_y][check_x]:
						break
					if result[check_z][check_y + 1][check_x]:
						break
					if result[check_z][check_y][check_x + 1]:
						break

					check_x += 1
					check_y += 1
					check_z += 1
					bound += 1

				num = 20
				rand = round(random.randint(min(x, y, z) ** num, bound ** num) ** (1.0 / num))
				result[z + rand][y + rand][x + rand] = 1



result_struct = Structure((mx, mx, mx))
result_struct_rotated = Structure((mx, mx, mx))
result_struct.data = np.array(result)
result_struct_rotated.data = np.array(result)


for i in range(1):
	result_struct_rotated.rotate(3, 2)

ds = Display(result_struct, scale = 10, border = 20)
ds2 = Display(result_struct_rotated, scale = 10, border = 20)
ds2.show()
ds.show()
ds2.main.mainloop()