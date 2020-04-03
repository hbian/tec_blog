from __future__ import division

def get_square_root(n, delta_threshold, max_try):
    init_min = 0
    init_max = n
    for i in xrange(max_try):
        mid = (init_min + init_max) / 2
        square = mid * mid
        delta = abs((square / n) - 1)
        print "{} {} {} {} {}".format(init_min, init_max, mid, square, delta)
        if delta < delta_threshold:
            return mid
        else:
            if square > n:
                init_max = mid
            else:
                init_min = mid
    return mid

if __name__ == '__main__':
    print get_square_root(10, 0.0001, 20)