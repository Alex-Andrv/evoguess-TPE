from output.impl import OptimizeParser
from typings.work_path import WorkPath

if __name__ == '__main__':
    root_path = WorkPath('examples')
    logs_path = root_path.to_path('logs', 'test')

    log_dir = '2023.04.05-06:00:47_2023.04.05-06:01:58'
    # log_dir = '2023.03.31-21:27:12_?'

    log_path = logs_path.to_path(log_dir)

    with OptimizeParser(log_path) as parser:
        for iteration in parser.parse():
            best_point = sorted(iteration.points)[0]
            print(iteration.index, best_point)
