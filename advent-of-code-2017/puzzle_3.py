find_num = 289326

def layer_start(layer):
    # 0 -> 1  ,  1 -> 2  ,  2 ->10
    if layer == 0:
        return 1
    layer -= 1
    layer_w = layer * 2 + 1
    return layer_w * layer_w + 1


def middle_right(layer, start):
    if layer <= 1:
        return start
    up = layer - 1
    return start + up


for test_layer in range(2000):
    start = layer_start(test_layer)
    end = layer_start(test_layer + 1) - 1 
    if find_num <= end and find_num >= start:
        print("Number is in layer:", test_layer)
        right = middle_right(test_layer, start)
        left = right + (4 * test_layer)
        print("  Left", left, " Right", right)
        if find_num == left or find_num == right:
            print("    Found as left/right, so dist:", test_layer - 1)
        if find_num > right and find_num < left:
            print("    Found to be in the top half")
            top_left = left - test_layer
            top_right = right + test_layer
            if find_num <= top_right:
                print("    Above right middle, so dist:", test_layer + (find_num - right))
            elif find_num >= top_left:
                print("    Above left middle, so dist:", test_layer + (left - find_num))
            else:
                middle = int((top_left - top_right) / 2) + top_right
                print("    Not above left or right, dist:", test_layer + abs(middle - find_num))
        if find_num > left:
            # Did not make this, answer was in top half ;)
            print("    Found to be in the bottom half")

# 37   36  35    34    33    32   31
# 38   17  16    15    14    13   30
# 39   18   5     4     3    12   29
# 40   19   6     1     2    11   28
# 41   20   7     8     9    10   27
# 42   21  22    23    24    25   26
# 43   44  45    46    47    48   49   50

