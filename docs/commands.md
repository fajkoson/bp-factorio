# Useful console commands

```text

/editor
/c game.speed=10                                                        # game speed
/c game.player.surface.freeze_daytime=true                              # 24 cycle becomes day only
/c game.player.force.technologies["mining-productivity-3"].level=8000   # set mining productivity to 8000 aka mega base
/c game.player.surface.destroy_decoratives({})                          # destroy all assets on the ground
/c game.forces["enemy"].kill_all_units()                                # kills all units except spawners
/c game.player.surface.peaceful_mode = true                             # they do not attack if you dont
/c game.player.print(game.player.position)                              # get your x,y location
/c game.player.teleport({X, Y})                                         # teleport to that location
/c game.player.teleport({X, Y}, 'surface_name')                         # teleport to other planet
/c game.player.character.destroy()                                      # disconnect your control, become god
/c game.player.create_character()                                       # spawn new character and connect control to it
/c game.player.character_running_speed_modifier=3                       # movement speed
/c game.player.force.laboratory_speed_modifier=1                        # inc. lab speed
/c helpers.write_file("mods.txt", serpent.block(script.active_mods))    # write all cur. act. mods and their version to the file script-output/mods.txt in APPDATA
```
