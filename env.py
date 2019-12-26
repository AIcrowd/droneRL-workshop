import numpy as np
from enum import Enum

class Tile(Enum):
    EMPTY = 0
    DRONE = 1
    PACKET = 2
    DROPZONE = 3
    DRONEWPAQUET = 4
        
class Arena():
    drone_density = 0.05
    
    def __init__(self, drone_names):
        # Compute arena size
        arena_side_size = int(np.ceil(np.sqrt(
            len(drone_names) / Arena.drone_density)))
        self.shape = (arena_side_size, arena_side_size)
        
        # Create arena grid
        self.grid = np.full(self.shape, fill_value=Tile.EMPTY)
        
        # Spawn objects
        n = len(drone_names)
        self.spawn(n*[Tile.DRONE] + 2*n*[Tile.PACKET])
    
    def spawn(self, objects):
        # Pick empty tiles
        idxs = np.arange(self.grid.size).reshape(self.grid.shape)
        available_idxs = idxs[self.grid == Tile.EMPTY]
        selected_idxs = np.random.choice(
            available_idxs, size=len(objects), replace=False)
        
        # Spawn objects
        np.put(self.grid, selected_idxs, objects)
    
    def __str__(self):
        # Convert grid tiles to text
        def tile_to_char(tile):
            if tile is Tile.EMPTY:
                return ' '
            if tile is Tile.DRONE:
                return '§'
            if tile is Tile.PACKET:
                return 'x'
            if tile is Tile.DROPZONE:
                return 'o'
            return '?'
        grid_char = np.vectorize(tile_to_char)(self.grid)
        
        # Assemble tiles into a grid
        lines = ['+---'*self.shape[1]+'+']
        for i, row in enumerate(grid_char):
            line_str = '| '
            for j, tile_str in enumerate(row):
                line_str += tile_str + ' | '
            lines.append(line_str)
            lines.append('+---'*self.shape[1]+'+')
            
        return '\n'.join(lines)