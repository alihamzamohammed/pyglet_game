import renderer as rn

DOWN = (0, -2) # Custom DOWN value taking into account double block height of player sprite

def bounce_modifier(func):
    
    def bounce(value, original):
        newval = value
    
        if rn.tilemap_walls.get_neighbor(rn.tilemap_walls.get_at_pixel(rn.player.x, rn.player.y), DOWN).tile is not None:
            if "sourcecode" in rn.tilemap_walls.get_neighbor(rn.tilemap_walls.get_at_pixel(rn.player.x, rn.player.y), DOWN).tile.properties:
                if rn.tilemap_walls.get_neighbor(rn.tilemap_walls.get_at_pixel(rn.player.x, rn.player.y), DOWN).tile.properties["sourcecode"] == "bouncePack":
                    newval = value * rn.tilemap_walls.get_neighbor(rn.tilemap_walls.get_at_pixel(rn.player.x, rn.player.y), DOWN).tile.properties["bounce_multiplier"]
    
        newfunc = func(newval, original)
        return newfunc
    
    return bounce

#    #DEBUG:
#
#def move_modifier(func):
#
#    def move(value):
#        newval = value
#        if rn.tilemap_walls.get_neighbor(rn.tilemap_walls.get_at_pixel(rn.player.x, rn.player.y), DOWN).tile is not None:
#            if "sourcecode" in rn.tilemap_walls.get_neighbor(rn.tilemap_walls.get_at_pixel(rn.player.x, rn.player.y), DOWN).tile.properties:
#                if rn.tilemap_walls.get_neighbor(rn.tilemap_walls.get_at_pixel(rn.player.x, rn.player.y), DOWN).tile.properties["sourcecode"] == "bouncePack":
#                    newval = newval * 2
#        
#        newfunc = func(newval)
#        return newfunc
#
#    return move
            

# TODO: This sorce code will also contain custom sound effects.