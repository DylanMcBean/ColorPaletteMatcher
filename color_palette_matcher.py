import json
import os

import exrex
from algorithms import *

dir_path = os.path.dirname(os.path.realpath(__file__)) # Get Exact File Path
config = json.load(open(f"{dir_path}/config.json"))

my_colors = [
    "#fdbebe", "#fc9d9d", "#fb7d7d", "#fa5c5c",
    "#fdcbbe", "#fcb09d", "#fb967d", "#fa7c5c",
    "#fdeabe", "#fce09d", "#fbd57d", "#facb5c", "#c8a24a",
    "#beeffd", "#9de8fc", "#7de0fb", "#5cd8fa", "#4aadc8",
    "#6a6969", "#373636", "#2d2e2e", "#1e1e1e",
    "#f5f4e8", "#f3f1e2", "#c2c1b5", "#929188"
]
test_colors = [
    "#b2b2b2", "#ffffff", "#656565",
    "#000000", "#686868", "#181818",
    "#b21818", "#ff5454", "#650000",
    "#18b218", "#54ff54", "#006500",
    "#b26818", "#ffff54", "#655e00",
    "#1818b2", "#5454ff", "#000065",
    "#b218b2", "#ff54ff", "#650065",
    "#18b2b2", "#54ffff", "#006565"
]

# smaller arrays for quicker brute forcing and ease of use
if config["random_palettes"]:
    color_count = config["random_palette_color_count"]
    my_colors = [exrex.getone("#[0-9A-F]{6}") for x in range(color_count)] # Create random palettes with [color_count] colors
    test_colors = [exrex.getone("#[0-9A-F]{6}") for x in range(color_count)]

distance_algo = config["distance_methods"][config["distance_method_index"]]
first_algo_result = first_algo(test_colors, my_colors, distance_algo)
pyros_algo_result = pyro_algorithm(test_colors, my_colors, distance_algo)
brute_algo_result = brute_force(test_colors, my_colors, distance_algo)

correct_first = get_correct_palette(test_colors, first_algo_result)
correct_pyros = get_correct_palette(test_colors, pyros_algo_result)
correct_brute = get_correct_palette(test_colors, brute_algo_result)

save_palette_image([test_colors,correct_first,correct_pyros,correct_brute], 32, dir_path)
