import math

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
my_colors = [(20,200,200),(80,20,200),(100,20,0)]
test_colors = [(0,0,0),(100,0,50),(10,50,200)]


def hex2rgb_color(hex_color): # From: Sir Vival of the PUNniest
    hex_color = int(hex_color.removeprefix('#'), 16)
    return [(hex_color >> shift)&0xff  for shift in [16, 8, 0]]

def rgb2lab_color(inputColor):
    # FOUND HERE --> https://stackoverflow.com/a/16020102
    num = 0
    RGB = [0, 0, 0]

    for value in inputColor :
        value = float(value) / 255

        if value > 0.04045 :
            value = ( ( value + 0.055 ) / 1.055 ) ** 2.4
        else :
            value = value / 12.92

        RGB[num] = value * 100
        num = num + 1

    XYZ = [0, 0, 0,]

    X = RGB [0] * 0.4124 + RGB [1] * 0.3576 + RGB [2] * 0.1805
    Y = RGB [0] * 0.2126 + RGB [1] * 0.7152 + RGB [2] * 0.0722
    Z = RGB [0] * 0.0193 + RGB [1] * 0.1192 + RGB [2] * 0.9505
    XYZ[ 0 ] = round( X, 4 )
    XYZ[ 1 ] = round( Y, 4 )
    XYZ[ 2 ] = round( Z, 4 )

    XYZ[ 0 ] = float( XYZ[ 0 ] ) / 95.047         # ref_X =  95.047   Observer= 2°, Illuminant= D65
    XYZ[ 1 ] = float( XYZ[ 1 ] ) / 100.0          # ref_Y = 100.000
    XYZ[ 2 ] = float( XYZ[ 2 ] ) / 108.883        # ref_Z = 108.883

    num = 0
    for value in XYZ :

        if value > 0.008856 :
            value = value ** ( 0.3333333333333333 )
        else :
            value = ( 7.787 * value ) + ( 16 / 116 )

        XYZ[num] = value
        num = num + 1

    Lab = [0, 0, 0]

    L = ( 116 * XYZ[ 1 ] ) - 16
    a = 500 * ( XYZ[ 0 ] - XYZ[ 1 ] )
    b = 200 * ( XYZ[ 1 ] - XYZ[ 2 ] )

    Lab [ 0 ] = round( L, 4 )
    Lab [ 1 ] = round( a, 4 )
    Lab [ 2 ] = round( b, 4 )

    return Lab

def distance_between_colors(col1,col2,mode):
    ensure_rgb = lambda c: (hex2rgb_color(c) if isinstance(c, str) else c) # From: Sir Vival of the PUNniest
    rgb_col1 = ensure_rgb(col1)
    rgb_col2 = ensure_rgb(col2)
    
    if mode.lower() == "euclidian":
        return sum((a - b)**2 for a,b in zip(rgb_col1, rgb_col2)) # Optimization From: Sir Vival of the PUNniest
    elif mode.lower() == "delta-e":
        return CIEDE2000(rgb2lab_color(rgb_col1), rgb2lab_color(rgb_col2))

def CIEDE2000(Lab_1, Lab_2):
    # FOUND HERE --> https://github.com/lovro-i/CIEDE2000/
    '''Calculates CIEDE2000 color distance between two CIE L*a*b* colors'''
    C_25_7 = 6103515625 # 25**7
    
    L1, a1, b1 = Lab_1[0], Lab_1[1], Lab_1[2]
    L2, a2, b2 = Lab_2[0], Lab_2[1], Lab_2[2]
    C1 = math.sqrt(a1**2 + b1**2)
    C2 = math.sqrt(a2**2 + b2**2)
    C_ave = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(C_ave**7 / (C_ave**7 + C_25_7)))
    
    L1_, L2_ = L1, L2
    a1_, a2_ = (1 + G) * a1, (1 + G) * a2
    b1_, b2_ = b1, b2
    
    C1_ = math.sqrt(a1_**2 + b1_**2)
    C2_ = math.sqrt(a2_**2 + b2_**2)
    
    if b1_ == 0 and a1_ == 0: h1_ = 0
    elif a1_ >= 0: h1_ = math.atan2(b1_, a1_)
    else: h1_ = math.atan2(b1_, a1_) + 2 * math.pi
    
    if b2_ == 0 and a2_ == 0: h2_ = 0
    elif a2_ >= 0: h2_ = math.atan2(b2_, a2_)
    else: h2_ = math.atan2(b2_, a2_) + 2 * math.pi

    dL_ = L2_ - L1_
    dC_ = C2_ - C1_    
    dh_ = h2_ - h1_
    if C1_ * C2_ == 0: dh_ = 0
    elif dh_ > math.pi: dh_ -= 2 * math.pi
    elif dh_ < -math.pi: dh_ += 2 * math.pi        
    dH_ = 2 * math.sqrt(C1_ * C2_) * math.sin(dh_ / 2)
    
    L_ave = (L1_ + L2_) / 2
    C_ave = (C1_ + C2_) / 2
    
    _dh = abs(h1_ - h2_)
    _sh = h1_ + h2_
    C1C2 = C1_ * C2_
    
    if _dh <= math.pi and C1C2 != 0: h_ave = (h1_ + h2_) / 2
    elif _dh  > math.pi and _sh < 2 * math.pi and C1C2 != 0: h_ave = (h1_ + h2_) / 2 + math.pi
    elif _dh  > math.pi and _sh >= 2 * math.pi and C1C2 != 0: h_ave = (h1_ + h2_) / 2 - math.pi 
    else: h_ave = h1_ + h2_
    
    T = 1 - 0.17 * math.cos(h_ave - math.pi / 6) + 0.24 * math.cos(2 * h_ave) + 0.32 * math.cos(3 * h_ave + math.pi / 30) - 0.2 * math.cos(4 * h_ave - 63 * math.pi / 180)
    
    h_ave_deg = h_ave * 180 / math.pi
    if h_ave_deg < 0: h_ave_deg += 360
    elif h_ave_deg > 360: h_ave_deg -= 360
    dTheta = 30 * math.exp(-(((h_ave_deg - 275) / 25)**2))
    
    R_C = 2 * math.sqrt(C_ave**7 / (C_ave**7 + C_25_7))  
    S_C = 1 + 0.045 * C_ave
    S_H = 1 + 0.015 * C_ave * T
    
    Lm50s = (L_ave - 50)**2
    S_L = 1 + 0.015 * Lm50s / math.sqrt(20 + Lm50s)
    R_T = -math.sin(dTheta * math.pi / 90) * R_C

    k_L, k_C, k_H = 1, 1, 1
    
    f_L = dL_ / k_L / S_L
    f_C = dC_ / k_C / S_C
    f_H = dH_ / k_H / S_H
    
    dE_00 = math.sqrt(f_L**2 + f_C**2 + f_H**2 + R_T * f_C * f_H)
    return dE_00

best_scores = {x:[] for x in test_colors}
my_color_scores = {x:[] for x in my_colors}

# generate initial distance map
for color1 in my_colors:
    for color2 in test_colors:
        dist = distance_between_colors(color1, color2, "delta-e") # defaulting to delta-e, can change later for user input
        my_color_scores[color1].append([color2,dist])
    my_color_scores[color1] = sorted(my_color_scores[color1], key=lambda x: x[1])
breakpoint

# loop until there is no changes left
while True:
    best_hash = hash(str(best_scores.items()) + str(my_color_scores.items()))
    # add the first element of each score to its corosponding best score if not already there
    for color in my_color_scores:
        if len(my_color_scores[color]) > 0:
            if not [color,my_color_scores[color][0][1]] in best_scores[my_color_scores[color][0][0]]:
                best_scores[my_color_scores[color][0][0]].append([color,my_color_scores[color][0][1]])

    # loop over best scores and remove the extra ones aswell as removing themselves from color_scores array
    for color in best_scores:
        if len(best_scores[color]):
            best_scores[color] = sorted(best_scores[color], key=lambda x: x[1])
            if len(best_scores[color]) > 1:
                for color2 in best_scores[color][1:]:
                    my_color_scores[color2[0]].remove([color,color2[1]])
                    best_scores[color].remove(color2)
                breakpoint

    # break if there have been no changes made
    if hash(str(best_scores.items()) + str(my_color_scores.items())) == best_hash:
        break

# print array
base_score = 0
for color in best_scores:
    try:
        print(f"{color} = {best_scores[color][0][0]}, Distance: {best_scores[color][0][1]:,}")
    except IndexError as e:
        print(f"{color} = None")
    base_score += best_scores[color][0][1]

# BRUTE FORCE ;)
from itertools import permutations

print(f"\n{list(zip(test_colors,my_colors))}\nScore To beat: {base_score:,}")

best = base_score
total_perms = math.factorial(len(my_colors))
counter = 0
for x in permutations(my_colors):
    score = sum(distance_between_colors(col1, col2, "delta-e") for col1, col2 in zip(test_colors,x))
    if score < best:
        print(f"Found New Best: {(best:=score):,}  --> {list(zip(test_colors,x))}")
    if (counter:=counter+1) % 10_000 == 0:
        print(f"{counter} / {total_perms}\r",end="")
print(f"\nInceased by {base_score-best:,}")