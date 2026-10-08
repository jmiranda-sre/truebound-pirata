scoreboard players set #is_server temp 1
execute at @e[tag=frame_5] run setblock ~ ~2 ~ air
execute at @e[tag=frame_5] run setblock ^2 ^ ^ air
execute at @e[tag=frame_5] run setblock ^-2 ^ ^ air
kill @e[tag=more_maps]
data merge entity @e[type=text_display,tag=server,limit=1] {view_range:1}
