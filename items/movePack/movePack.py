import renderer as rn
import time as t

DOWN = (0, -2) # Custom DOWN value taking into account double block height of player sprite

#    #DEBUG:

onTile = False
currentTime = 0
duration = 0
multiplier = 0
def move_modifier(func):

    def move(value):
        global onTile, currentTime, duration, multiplier
        newval = value
        if not onTile:
            if rn.tilemap_walls.get_neighbor(rn.tilemap_walls.get_at_pixel(rn.player.x, rn.player.y), DOWN).tile is not None:
                if "sourcecode" in rn.tilemap_walls.get_neighbor(rn.tilemap_walls.get_at_pixel(rn.player.x, rn.player.y), DOWN).tile.properties:
                    if rn.tilemap_walls.get_neighbor(rn.tilemap_walls.get_at_pixel(rn.player.x, rn.player.y), DOWN).tile.properties["sourcecode"] == "movePack":
                        multiplier = rn.tilemap_walls.get_neighbor(rn.tilemap_walls.get_at_pixel(rn.player.x, rn.player.y), DOWN).tile.properties["move_multiplier"]
                        duration = rn.tilemap_walls.get_neighbor(rn.tilemap_walls.get_at_pixel(rn.player.x, rn.player.y), DOWN).tile.properties["move_duration"]
                        onTile = True
                        currentTime = t.perf_counter()
        else:
            if t.perf_counter() < currentTime + duration:
                newval = newval * multiplier
            else:
                newval = value
                onTile = False
        
        newfunc = func(newval)
        return newfunc

    return move
            

# TODO: This sorce code will also contain custom sound effects.