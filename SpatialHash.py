import itertools


class SpatialHash:
    # we shouldn't make the buckets narrower than the interaction radius
    def __init__(self, cell_size, width, height):
        self.buckets = [
            [set() for _ in range(width // cell_size + 1)]
            for _ in range(height // cell_size + 1)
        ]
        self.cell_size = cell_size

    def _hash(self, point):
        return int(point.pos[0] / self.cell_size), int(point.pos[1] / self.cell_size)

    def insert_particle(self, particle):
        bucket_x, bucket_y = self._hash(particle)
        self.buckets[bucket_y][bucket_x].add(particle)
        # TODO potentially move particles when they're updated instead of recreating spatial hash each frame

    def _run(self, a, b, mod):
        return map(lambda x: x % mod, range(a, b))

    def neighbor_particles(self, particle):
        num_cells_x = len(self.buckets[0])
        num_cells_y = len(self.buckets)
        particle_bucket_x, particle_bucket_y = self._hash(particle)

        surrounding_indices = [
            (j, i)
            for j in self._run(
                particle_bucket_x - 1, particle_bucket_x + 2, num_cells_x
            )
            for i in self._run(
                particle_bucket_y - 1, particle_bucket_y + 2, num_cells_y
            )
        ]

        surrounding_buckets = [self.buckets[i][j] for j, i in surrounding_indices]
        neighbors = set()
        for bucket in surrounding_buckets:
            neighbors = neighbors.union(bucket)
        return neighbors
