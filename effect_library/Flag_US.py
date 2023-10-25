import random

state = {}

def sparkling_star(i_star, dist_star):
    life_spark = 50 # nr. of frames a spark will live until it extinguishes
    if not(dist_star) and random.random() < .01:
        state[i_star] = life_spark
    intensity = 1
    if i_star in state:
        intensity += 2 * (state[i_star] / life_spark)
        state[i_star] -=1
        if state[i_star] <= 0:
            del state[i_star]
    return rgb(intensity, intensity, intensity)

def render(index, frame):
    nr_british_colonies = 13
    n_stars = max(1, min(5, round(num_pixels / 20)))
    # The stripes should occupy 60% of the flag width or pixel string length,
    # however for the stripes to look even, we adjust this percentage so each
    # stripe occupies the same number of pixels
    width_cols_rel = round(num_pixels * .6 / nr_british_colonies) * \
            nr_british_colonies / num_pixels
    width_cant = num_pixels * (1 - width_cols_rel)
    width_cols = num_pixels - width_cant
    pix_star = 1 if num_pixels < 200 else 2
    if index < width_cant:
        # canton with stars
        i_star = int(index / round(width_cant / (n_stars + 1)))
        dist_star =  index % round(width_cant / (n_stars + 1))
        if i_star < 1 or i_star > n_stars or dist_star >= pix_star:
            return dim(blue)
        else:
            return sparkling_star(i_star, dist_star)
    elif not(int((index - width_cant) / (width_cols / nr_british_colonies)) % 2):
        return red
    else:
        return white
