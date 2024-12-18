from tqdm import tqdm
#%% 111111111111111111111111111111111111

# part 1
import numpy as np
with open("inputs/input1.txt") as file:
    lines = [line.strip("\n").split() for line in file.readlines()]

lines = np.array(lines).astype("int64")
left = lines[:, 0]
right = lines[:, 1]

ordered = np.vstack([
    np.sort(left),
    np.sort(right)
]).T

difs = np.abs(ordered[:, 0] - ordered[:, 1])
print(sum(difs))

# part 2
mults = []
for num in ordered[:, 0]:
    right_occs = sum(ordered[:, 1] == num)
    mults.append(right_occs)
mults = np.array(mults)
print(sum(mults * ordered[:, 0]))
#%% 2222222222222222222222222222222

# part 1
import numpy as np

def is_safe(report):
    n = report[0]
    difs = []
    for num in report[1:]:
        difs.append(n - num)
        n = num
    difs = np.array(difs)
    if sum(difs > 0) != len(difs) and sum(difs < 0) != len(difs):
        return False
    if sum(np.abs(difs) >= 1) == len(difs) and sum(np.abs(difs) <= 3) == len(difs):
        return True
    return False

with open("inputs/input2.txt") as file:
    reports = [line.strip("\n").split() for line in file.readlines()]

safety_vec = []
for report in reports:
    for i in range(len(report)):
        report[i] = int(report[i])
    safety_vec.append(is_safe(report))
print(sum(safety_vec))

# part 2
from itertools import combinations
def pd_is_safe(report):
    combs = combinations(report, len(report) - 1)
    subsafeties = [is_safe(comb) for comb in combs]
    return True in subsafeties

safety_vec2 = []
for report in reports:
    safety_vec2.append(pd_is_safe(report))
print(sum(safety_vec2))

#%% 3333333333333333333333333333333333333333

# part 1
import re
import numpy as np

def find_multiply(garbled_str):
    mults = re.findall(r"mul\([0-9]+,[0-9]+\)", garbled_str)
    nums = np.array([re.findall(r"[0-9]+", mult) for mult in mults]).astype("int64")
    product = nums[:, 0] * nums[:, 1]
    return sum(product)

with open("inputs/input3.txt") as file:
    lines = [line.strip("\n") for line in file.readlines()]
total = "".join(lines)
print(find_multiply(total))

# part 2
def find_multiply_conditional(garbled_str):
    instructions = re.findall(r"mul\([0-9]+,[0-9]+\)|do\(\)|don't\(\)", garbled_str)
    act = True
    valid_instructions = []
    for instruction in instructions:
        if instruction == "don't()":
            act = False
            continue
        elif instruction == "do()":
            act = True
            continue
        elif act:
            valid_instructions.append(instruction)
    nums = np.array([re.findall(r"[0-9]+", mult) for mult in valid_instructions]).astype("int64")
    product = nums[:, 0] * nums[:, 1]
    return sum(product)

print(find_multiply_conditional(total))
#%% 444444444444444444444444444444444444444444

# part 1
import numpy as np
with open("inputs/input4.txt") as file:
    ltr_grid = np.array([[letter for letter in line.strip("\n")] for line in file.readlines()])

def get_vecs(start, grid_dims):
    change_vec = np.array([1, 2, 3])
    row_vec = (np.ones(3) * start[0]).astype("int64")
    col_vec = (np.ones(3) * start[1]).astype("int64")
    up = list(zip(row_vec - change_vec, col_vec))
    right = list(zip(row_vec, col_vec + change_vec))
    down = list(zip(row_vec + change_vec, col_vec))
    left = list(zip(row_vec, col_vec - change_vec))
    up_right = list(zip(row_vec - change_vec, col_vec + change_vec))
    down_right = list(zip(row_vec + change_vec, col_vec + change_vec))
    down_left = list(zip(row_vec + change_vec, col_vec - change_vec))
    up_left = list(zip(row_vec - change_vec, col_vec - change_vec))

    directions = [up, up_right, right, down_right, down, down_left, left, up_left]
    valid_directions = []
    for dir_set in directions:
        for i, (row, col) in enumerate(dir_set):
            if row < 0 or col < 0 or row >= grid_dims[0] or col >= grid_dims[1]:
                i = 0
                break
        if i == 2:
            valid_directions.append(dir_set)
    return valid_directions


def find_starts(grid, character):
    starts = []
    for i, row in enumerate(grid):
        for j, letter in enumerate(row):
            if letter == character:
                starts.append((i, j))
    return starts

starts = find_starts(ltr_grid, "X")
count = 0
for start in starts:
    vecs = get_vecs(start, ltr_grid.shape)
    # cursed triple list comprehension
    letters = ["".join(letterset) for letterset in [[ltr_grid[i, j] for i, j in vec] for vec in vecs]]
    count += letters.count("MAS")
print(count)

# part 2
def is_x_mas(position, grid):
    if position[0] - 1 < 0 or \
            position[0] + 1 >= grid.shape[0] or \
            position[1] - 1 < 0 or \
            position[1] + 1 >= grid.shape[1]:
        return False
    upleft = grid[position[0] - 1, position[1] - 1]
    upright = grid[position[0] - 1, position[1] + 1]
    downright = grid[position[0] + 1, position[1] + 1]
    downleft = grid[position[0] + 1, position[1] - 1]

    set1 = {upleft, downright}
    set2 = {upright, downleft}

    if set1 == {"S", "M"} and set1 == set2:
        return True
    return False

tfs = []
starts = find_starts(ltr_grid, "A")
for start in starts:
    tfs.append(is_x_mas(start, ltr_grid))
print(sum(tfs))

#%%  55555555555555555555555555555555555

# part 1
import numpy as np
with open("inputs/input5.txt") as file:
    lines = [line.strip("\n") for line in file.readlines()]
rules = np.array([line.strip("\n").split("|") for line in lines if "|" in line]).astype("int64")
updates = [[int(x) for x in line.strip("\n").split(",")] for line in lines if "|" not in line and len(line) != 0]

def get_afters(pgnum):
    return rules[rules[:, 0] == pgnum, 1]

def is_valid(update):
    for i, num in enumerate(update):
        afters = get_afters(num)
        for after in afters:
            if after in update[:i]:
                return False
    return True

valid_updates = [update for update in updates if is_valid(update)]
centers = [update[len(update) // 2] for update in valid_updates]
print(sum(centers))

# part 2: recursion!
invalid_updates = [update for update in updates if not is_valid(update)]

def correct_update(update):
    if is_valid(update):
        return update
    for i, num in enumerate(update):
        corrected = update
        afters = get_afters(num)
        for after in afters:
            if after in update[:i]:
                loc = update.index(after)
                #weird python thing allows me to slice beyond the indices of an array
                corrected = corrected[:loc] + [num] + corrected[loc:i] + corrected[i + 1:]
                return correct_update(corrected)

corrected = [correct_update(update) for update in invalid_updates]
centers = [update[len(update) // 2] for update in corrected]
print(sum(centers))

#%% 666666666666666666666666666666666666


# part 1
import numpy as np
with open("inputs/input6.txt") as file:
    lines = np.array([[letter for letter in line.strip("\n")] for line in file.readlines()])

def chart_path(grid):
    pathed_grid = grid.copy()
    # let's recycle an older function here
    loc = list(find_starts(pathed_grid, "^")[0])
    sym = "^"
    while 0 < loc[0] < pathed_grid.shape[0] and 0 < loc[1] < pathed_grid.shape[1]:
        try:
            if sym == "^":
                if pathed_grid[loc[0] - 1, loc[1]] == "#":
                    sym = ">"
                else:
                    pathed_grid[loc[0], loc[1]] = "X"
                    loc[0] -= 1
            elif sym == ">":
                if pathed_grid[loc[0], loc[1] + 1] == "#":
                    sym = "v"
                else:
                    pathed_grid[loc[0], loc[1]] = "X"
                    loc[1] += 1
            elif sym == "v":
                if pathed_grid[loc[0] + 1, loc[1]] == "#":
                    sym = "<"
                else:
                    pathed_grid[loc[0], loc[1]] = "X"
                    loc[0] += 1
            elif sym == "<":
                if pathed_grid[loc[0], loc[1] - 1] == "#":
                    sym = "^"
                else:
                    pathed_grid[loc[0], loc[1]] = "X"
                    loc[1] -= 1
        except IndexError:
            break
    pathed_grid[loc[0], loc[1]] = "X" # mark last position
    return pathed_grid

# recycle it again
pathed = chart_path(lines)
xs = find_starts(pathed, "X")
print(len(xs))

# part 2
def is_looped(grid):
    loc = list(find_starts(grid, "^")[0])
    sym = "^"
    path_dict = {}
    while 0 < loc[0] < grid.shape[0] and 0 < loc[1] < grid.shape[1]:
        if tuple(loc) in path_dict and sym in path_dict[tuple(loc)]:
            return 1
        elif tuple(loc) in path_dict and sym not in path_dict[tuple(loc)]:
            path_dict[tuple(loc)].append(sym)
        elif tuple(loc) not in path_dict:
            path_dict[tuple(loc)] = [sym]
        try:
            if sym == "^":
                if grid[loc[0] - 1, loc[1]] == "#":
                    sym = ">"
                else:
                    loc[0] -= 1
            elif sym == ">":
                if grid[loc[0], loc[1] + 1] == "#":
                    sym = "v"
                else:
                    loc[1] += 1
            elif sym == "v":
                if grid[loc[0] + 1, loc[1]] == "#":
                    sym = "<"
                else:
                    loc[0] += 1
            elif sym == "<":
                if grid[loc[0], loc[1] - 1] == "#":
                    sym = "^"
                else:
                    loc[1] -= 1
        except IndexError:
            break
    return 0


looped = []
possible_obstruction_locations = xs
for i, j in possible_obstruction_locations:
    mapcopy = lines.copy()
    if mapcopy[i, j] == "^":
        continue
    mapcopy[i, j] = "#"
    looped.append(is_looped(mapcopy))
print(sum(looped))
#%%  77777777777777777777777777777777777777777777777777777777

# part 1
with open("inputs/input7.txt") as file:
    calibrations = [line.strip("\n") for line in file.readlines()]
leftsides = [int(rule.split(":")[0]) for rule in calibrations]
rightsides = [[int(x) for x in rule.split(": ")[1].split()] for rule in calibrations]

def is_valid(left, right):
    if len(right) == 2:
        if left in [right[0] + right[1], right[0] * right[1]]:
            return True
        else:
            return False
    else:
        return is_valid(left, [right[0] + right[1]] + right[2:]) or is_valid(left, [right[0] * right[1]] + right[2:])

valid_testvals = []
for left, right in zip(leftsides, rightsides):
    if is_valid(left, right):
        valid_testvals.append(left)
print(sum(valid_testvals))

# part 2
def is_valid2(left, right):
    if len(right) == 2:
        if left in [right[0] + right[1], right[0] * right[1], int(str(right[0]) + str(right[1]))]:
            return True
        else:
            return False
    else:
        return is_valid2(left, [right[0] + right[1]] + right[2:]) or \
            is_valid2(left, [right[0] * right[1]] + right[2:]) or \
            is_valid2(left, [int(str(right[0]) + str(right[1]))] + right[2:])

valid_testvals = []
for left, right in zip(leftsides, rightsides):
    if is_valid2(left, right):
        valid_testvals.append(left)
print(sum(valid_testvals))
#%% 88888888888888888888888888888888888

# part 1
import numpy as np
from itertools import combinations

with open("inputs/input8.txt") as file:
    lines = np.array([[letter for letter in line.strip("\n")] for line in file.readlines()])

def get_sym_locs(grid):
    symlocs = (grid != ".").nonzero()
    symlocs = list(zip(symlocs[0], symlocs[1]))
    symset = set()
    for i, j in symlocs:
        symset = symset.union({grid[i, j]})
    symdict = {}
    for sym in symset:
        locs = (grid == sym).nonzero()
        locs = list(zip(locs[0], locs[1]))
        if len(locs) > 1:
            symdict[sym] = locs
    return symdict

def place_res(t1_loc, t2_loc, grid_dims):
    rise = t1_loc[0] - t2_loc[0]
    run = t1_loc[1] - t2_loc[1]
    pres_1 = [t1_loc[0] + rise, t1_loc[1] + run]
    pres_2 = [t1_loc[0] - rise, t1_loc[1] - run]
    pres_3 = [t2_loc[0] + rise, t2_loc[1] + run]
    pres_4 = [t2_loc[0] - rise, t2_loc[1] - run]
    possible_resonances = [pres_1, pres_2, pres_3, pres_4]
    resonances = [tuple(res) for res in possible_resonances \
                  if tuple(res) not in [t1_loc, t2_loc] \
                  and 0 <= res[0] < grid_dims[0] and 0 <= res[1] < grid_dims[1]]
    return resonances


def chart_resonance(tower_locs, grid_dims):
    pairs = list(combinations(tower_locs, 2))
    resonances = []
    for pair in pairs:
        resonances += place_res(pair[0], pair[1], grid_dims)
    return resonances

def map_res(grid):
    sym_locs = get_sym_locs(grid)
    res_locs = []
    for sym in sym_locs:
        charted = chart_resonance(sym_locs[sym], grid.shape)
        res_locs += charted
    return list(set(res_locs))

print(len(map_res(lines)))

def place_cascading_resonance(t1_loc, t2_loc, grid_dims):
    rise = t1_loc[0] - t2_loc[0]
    run = t1_loc[1] - t2_loc[1]
    resonances = []
    resloc = list(t1_loc)
    while 0 <= resloc[0] + rise < grid_dims[0] and 0 <= resloc[1] + run < grid_dims[1]:
        resloc[0] += rise
        resloc[1] += run
        if tuple(resloc) not in [t1_loc, t2_loc]:
            resonances.append(tuple(resloc))
    resloc = list(t1_loc)
    while 0 <= resloc[0] - rise < grid_dims[0] and 0 <= resloc[1] - run < grid_dims[1]:
        resloc[0] -= rise
        resloc[1] -= run
        if tuple(resloc) not in [t1_loc, t2_loc]:
            resonances.append(tuple(resloc))
    return list(set(resonances).union({t1_loc, t2_loc}))

def chart_cascading_resonance(tower_locs, grid_dims):
    pairs = list(combinations(tower_locs, 2))
    resonances = []
    for pair in pairs:
        resonances += place_cascading_resonance(pair[0], pair[1], grid_dims)
    return resonances

def map_cascading_res(grid):
    sym_locs = get_sym_locs(grid)
    res_locs = []
    for sym in sym_locs:
        charted = chart_cascading_resonance(sym_locs[sym], grid.shape)
        res_locs += charted
    return list(set(res_locs))

print(len(map_cascading_res(lines)))

#%%  999999999999999999999999999999999999999999999

# part 1
import numpy as np
import sys
sys.setrecursionlimit(20000)

with open("inputs/input9.txt") as file:
    disk_map = file.readlines()[0].strip("\n")

def image_disk(dmap):
    file_blocks = list(dmap[::2])
    space_blocks = list(dmap[1::2])
    file_blocks.append(dmap[-1])
    space_blocks.append(0)
    return np.array(list(zip(range(len(file_blocks)), file_blocks, space_blocks))).astype("int64")

def compress(remaining_dimage, cur_state = []):
    if type(remaining_dimage) == type(""):
        remaining_dimage = image_disk(remaining_dimage)
    if remaining_dimage.shape[0] == 0:
        return cur_state
    if remaining_dimage.shape[0] == 1:
        file = remaining_dimage[0]
        cur_state += file[1] * [file[0]]
        return cur_state
    else:
        file = remaining_dimage[0]
        remaining_dimage = remaining_dimage[1:]
        packfile = remaining_dimage[-1]
        cur_state += file[1] * [file[0]]
        remaining_space = file[2]
        for i in range(remaining_space):
            cur_state += [packfile[0]]
            packfile[1] -= 1
            if packfile[1] == 0:
                remaining_dimage = remaining_dimage[:-1]
                if remaining_dimage.shape[0] == 0:
                    break
                packfile = remaining_dimage[-1]
        return compress(remaining_dimage, cur_state = cur_state)

def checksum(dmap):
    compressed_disk = compress(dmap)
    result = 0
    for i, num in enumerate(compressed_disk):
        result += i * num
    return result

print(checksum(disk_map))

# part 2
def build_disk(rep, image = True):
    if not image:
        dimage = image_disk(rep)
    else:
        dimage = rep
    disk = []
    for file in dimage:
        disk += file[1] * [file[0]]
        disk += file[2] * ["."]
    return np.array(disk)

def compress2(dimage, curfile = -1):
    if type(dimage) == type(""):
        dimage = image_disk(dimage)
    if curfile == -1:
        curfile = max(dimage[:, 0])
    if curfile == 0:
        return dimage
    packfile_index = (dimage[:, 0] == curfile).nonzero()[0][0]
    packfile_info = dimage[packfile_index]
    prefile_info = dimage[packfile_index - 1]
    for i, file in enumerate(dimage):
        if i >= packfile_index:
            return compress2(dimage, curfile - 1)
        if file[2] >= packfile_info[1]:
            prefile_info[2] += packfile_info[1] + packfile_info[2]
            packfile_info[2] = file[2] - packfile_info[1]
            file[2] = 0
            dimage = np.vstack([
                dimage[: i + 1],
                packfile_info,
                dimage[i + 1 : packfile_index],
                dimage[packfile_index + 1:]
            ])
            return compress2(dimage, curfile - 1)

def checksum2(dmap):
    compressed_image = compress2(dmap)
    compressed_built = build_disk(compressed_image)
    result = 0
    for i, num in enumerate(compressed_built):
        if num.isnumeric():
            result += i * int(num)
    return result

print(checksum2(disk_map))

#%% 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10


