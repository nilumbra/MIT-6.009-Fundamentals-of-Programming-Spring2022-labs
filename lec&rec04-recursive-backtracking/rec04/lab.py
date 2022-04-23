# TENT PACKING

# Pack a tent with different sleeping bag shapes leaving no empty squares
#
# INPUTS:
#   tent_size = (rows, cols) for tent grid
#   covered_squares = set of (r, c) tuples giving location of rocks
#   bag_list = list of sets, each decribing a sleeping bag shape
#      Each set contains (r, c) tuples enumerating contiguous grid
#      squares occupied by the bag, coords are relative to the upper-
#      left corner of the bag.  You can assume every bag occupies
#      at least the grid (0,0).
#
# Example bag_list entries:
#      vertical 3x1 bag: { (0,0), (1,0), (2,0) }
#      horizontal 1x3 bag: { (0,0), (0,1), (0,2) }
#      square bag: { (0,0), (0,1), (1,0), (1,1) }
#      L-shaped bag: { (0,0), (1,0), (1,1) }
#      C-shaped bag: { (0,0), (0,1), (1,0), (2,0), (2,1) }
#      reverse-C-shaped bag: { (0,0), (0,1), (1,1), (2,0), (2,1) }
#
# OUTPUT:
#   None if no packing can be found; otherwise a list giving the
#   placement and type for each placed bag expressed as a dictionary
#   with keys
#     "anchor": (r, c) for upper-left corner of bag
#     "shape": index of bag on bag list
#
def pack(tent_size, covered_squares, bag_list):
    raise NotImplementedError



bag_list = [
    {(0, 0), (1, 0), (2, 0)},  # vertical 3x1 bag
    {(0, 0), (0, 1), (0, 2)},  # horizontal 1x3 bag
    {(0, 0), (0, 1), (1, 0), (1, 1)},  # square bag
    {(0, 0), (1, 0), (1, 1)},  # L-shaped bag
    {(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)},  # C-shaped bag
    {(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)},  # reverse C-shaped bag
]

if __name__ == '__main__':

    tent_size = (2, 3)
    rocks = set()
    res=pack(tent_size, rocks, bag_list)
    print_pack(tent_size, rocks, bag_list, res)
