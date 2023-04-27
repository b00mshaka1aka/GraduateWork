import math


class Voxel:
    def __init__(self, points):
        self.points = points
        self.count = 0
        self.min = 0
        self.max = 0

    def get_mean_point(self):
        mean_point = [0] * 3

        for i in range(self.min, self.max + 1):
            point = self.points[i]

            mean_point[0] += point[0]
            mean_point[1] += point[1]
            mean_point[2] += point[2]

        mean_point[0] /= self.count
        mean_point[1] /= self.count
        mean_point[2] /= self.count

        return mean_point

    def get_points(self):
        return self.points[self.min:self.max + 1]


class Cell:
    def __init__(self):
        self.voxels = None
        self.points = []
        self.z_min = 0
        self.z_max = 0

    def __len__(self):
        return len(self.points)

    def add_point(self, point):
        self.points.append(point)

        if len(self.points) == 0:
            self.z_min = point[2]
            self.z_max = point[2]

        if point[2] < self.z_min:
            self.z_min = point[2]
        if point[2] > self.z_max:
            self.z_max = point[2]

    def get_mean(self):
        points = []
        for voxel in self.voxels:
            if voxel is not None:
                points.append(voxel.get_mean_point())

        return points

    def make_voxels(self, k_z, d_z, min_point):
        self.voxels = [None] * k_z
        self.points = sorted(self.points, key=lambda point: point[2])

        for i in range(len(self.points)):
            point = self.points[i]
            k = math.trunc((point[2] - min_point[2]) / d_z)

            if self.voxels[k] is not None:
                self.voxels[k].count += 1
                self.voxels[k].max = i
            else:
                self.voxels[k] = Voxel(self.points)

                self.voxels[k].count = 1
                self.voxels[k].min = i
                self.voxels[k].max = i

    def get_level_min_voxel(self):
        for i in range(len(self.voxels)):
            if self.voxels[i] is not None:
                return i
        return -1

    def get_points(self):
        points = []
        for i in range(len(self.voxels)):
            if self.voxels[i] is not None:
                points.extend(self.voxels[i].get_points())
        return points


class CellDivision:
    def __init__(self, points, d_x, d_y, d_z):
        self.d_x = d_x
        self.d_y = d_y
        self.d_z = d_z
        self.points = points
        self.min_point, self.max_point = self._get_min_max_points()

        self.k_x = math.ceil((self.max_point[0] - self.min_point[0]) / self.d_x)
        self.k_y = math.ceil((self.max_point[1] - self.min_point[1]) / self.d_y)
        self.k_z = math.ceil((self.max_point[2] - self.min_point[2]) / self.d_z)

        self.cells = self._cell_division()

    def _cell_division(self):
        cells = [[None] * self.k_x for _ in range(self.k_y)]

        for point in self.points:
            p = math.trunc((point[1] - self.min_point[1]) / self.d_y)
            q = math.trunc((point[0] - self.min_point[0]) / self.d_x)

            if cells[p][q] is None:
                cells[p][q] = Cell()
            cells[p][q].add_point(point)

        for cells_row in cells:
            for cell in cells_row:
                if cell is not None:
                    cell.make_voxels(self.k_z, self.d_z, self.min_point)

        return cells

    def get_mean_points(self):
        mean_points = []

        for cells_row in self.cells:
            for cell in cells_row:
                if cell is not None:
                    # mean_points.add_point(cell.get_mean())
                    voxel_mean_points = cell.get_mean()
                    for mean_point in voxel_mean_points:
                        mean_points.append(mean_point)

        return mean_points

    def _get_min_max_points(self):
        x_min = self.points[0][0]
        x_max = self.points[0][0]

        y_min = self.points[0][1]
        y_max = self.points[0][1]

        z_min = self.points[0][2]
        z_max = self.points[0][2]

        for x, y, z in self.points:
            if x < x_min:
                x_min = x
            if x > x_max:
                x_max = x

            if y < y_min:
                y_min = y
            if y > y_max:
                y_max = y

            if z < z_min:
                z_min = z
            if z > z_max:
                z_max = z

        return [x_min, y_min, z_min], [x_max, y_max, z_max]
