from output.impl import OptimizeParser
from typings.work_path import WorkPath

if __name__ == '__main__':
    root_path = WorkPath('examples')
    logs_path = root_path.to_path('logs', 'WvC')

    log_dir = '2023.04.14-01:17:40_?'
    # log_dir = '2023.03.31-21:27:12_?'

    log_path = logs_path.to_path(log_dir)

    with OptimizeParser(log_path) as parser:
        for iteration in parser.parse():
            best_point = sorted(iteration.points)[0]
            print(iteration.index, best_point)


# 0 [](0) by 1024
# 1 [939 2830 2877](3) by 1024
# 2 [939 2830 2877](3) by 1024
# 3 [457 716 1751 1858 2333](5) by 1024
# 4 [716 1078 1432 2473 2830 2877](6) by 1024
# 5 [31 341 1289 1751 1858 2124 2333](7) by 1024
# 6 [261 457 716 1614 1751 1858 2333 2894 2921](9) by 1024
# 7 [261 457 716 1614 1751 1858 2333 2894 2921](9) by 1024