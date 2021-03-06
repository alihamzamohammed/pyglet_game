import renderer as rn
import time as t

DOWN = (0, -2) # Custom DOWN value taking into account double block height of player sprite

#    #DEBUG:

onTile = False
currentTime = 0
duration = 0
multiplier = 0
immuneTime = 0
def move_modifier(func):

    def move(value):
        global onTile, currentTime, duration, multiplier, immuneTime
        newval = value

        if not onTile and t.perf_counter() > immuneTime + 1:
            try:
                if rn.tilemap_walls.get_neighbor(rn.tilemap_walls.get_at_pixel(rn.player.x, rn.player.y), DOWN).tile is not None:
                    if "sourcecode" in rn.tilemap_walls.get_neighbor(rn.tilemap_walls.get_at_pixel(rn.player.x, rn.player.y), DOWN).tile.properties:
                        if rn.tilemap_walls.get_neighbor(rn.tilemap_walls.get_at_pixel(rn.player.x, rn.player.y), DOWN).tile.properties["sourcecode"] == "movePackHold":
                            multiplier = rn.tilemap_walls.get_neighbor(rn.tilemap_walls.get_at_pixel(rn.player.x, rn.player.y), DOWN).tile.properties["move_multiplier"]
                            duration = rn.tilemap_walls.get_neighbor(rn.tilemap_walls.get_at_pixel(rn.player.x, rn.player.y), DOWN).tile.properties["move_duration"]
                            onTile = True
                            currentTime = t.perf_counter()
            except AttributeError:
                pass
        elif onTile:
            if t.perf_counter() < currentTime + duration:
                newval = newval * multiplier
            else:
                newval = value
                onTile = False
                immuneTime = t.perf_counter()
        
        newfunc = func(newval)
        return newfunc

    return move

def bounce_modifier(func):

    def bounce(value, orig):
        global onTile
        newval = value
        
        if onTile:
            multiplier = rn.tilemap_walls.get_neighbor(rn.tilemap_walls.get_at_pixel(rn.player.x, rn.player.y), DOWN).tile.properties["bounce_multiplier"]
            newval = newval * multiplier

        newfunc = func(newval, orig)

        return newfunc
    
    return bounce


# TODO: This sorce code will also contain custom sound effects.