from helpful_funcs import *
import sys, time, datetime

def first_algo(palette1, palette2, distance_algo):
    # new algo
    distances = []
    for color1 in palette1:
        for color2 in palette2:
            # distances.append([[color1,color2], distance_between_colors(hex2rgb_color(color1), hex2rgb_color(color2), config["distance_methods"][config["distance_method_index"]])])
            distances.append([[color1,color2], distance_between_colors(color1, color2, distance_algo)])
    #sort palette
    distances = sorted(distances,key=lambda x: x[1])
    new_matches = []
    used_colours = []
    for value in distances:
        if (value[0][0] not in used_colours and value[0][1] not in used_colours):
            new_matches.append(value)
            used_colours.append(value[0][0])
            used_colours.append(value[0][1])
    # calculate error
    # base_error = sum(distance_between_colors(hex2rgb_color(x[0][0]), hex2rgb_color(x[0][1]), config["distance_methods"][config["distance_method_index"]]) for x in new_matches)
    base_error = sum(distance_between_colors(x[0][0], x[0][1], distance_algo) for x in new_matches)
    
    return base_error, new_matches

def pyro_algorithm(palette1, palette2, distance_algo):
    # Pyro - START
    pyro_matches = []
    # reverse and copy
    my_colors_reduced = palette2.copy()
    def calc_dist(color1, color2):
        return distance_between_colors(color1, color2, distance_algo)
    for color1 in palette1:
        _distances = [[color2, calc_dist(color1, color2)] for color2 in my_colors_reduced]
        # find the shortest distance
        _sorted_distances = sorted(_distances,key=lambda x: x[1])
        #print(f"{_sorted_distances = }")
        # keep the 1st one chuck the rest
        color2, shortest_dist = _sorted_distances[0]
        pyro_matches.append([[color1, color2], shortest_dist])
        # now rebuild the list of colors with 1 less element
        my_colors_reduced = [color for color in my_colors_reduced if color != color2]


    # calculate error
    pyro_error = sum(x[1] for x in pyro_matches)
    
    return pyro_error, pyro_matches

def brute_force(palette1, palette2, distance_algo):
    better_palette = []
    # BRUTE FORCE ;)
    from itertools import permutations

    best = -1
    total_perms = math.factorial(len(palette2))
    start_time = time.time()
    for idx, x in enumerate(permutations(palette2)):
        score = sum(distance_between_colors(col1, col2, distance_algo) for col1, col2 in zip(palette1,x))
        if best == -1 or score < best:
            better_palette = list(zip(palette1,x))
        if idx % 10_000 == 0:
            time_taken = time.time() - start_time
            eta = datetime.timedelta(seconds=int(time_taken * (total_perms / max(1,idx))-time_taken))
            print(f"Brute Force: [{('-' * int((idx//(total_perms/100)))):100}] ETA: {eta}\r",end="")

    return best, better_palette