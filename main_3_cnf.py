from algorithm.impl import Elitism
from algorithm.module.crossover import TwoPoint
from algorithm.module.mutation import Doer
from algorithm.module.selection import Roulette
from core.impl import Optimize
from core.module.comparator import MinValueMaxSize
from core.module.limitation import WallTime
from core.module.sampling import Const
from core.module.space import SearchSet
from executor.impl import ProcessExecutor
from function.impl import RhoFunction
from function.module.measure import SolvingTime
from function.module.solver.impl import Glucose3
from instance.impl import Instance
from instance.module.encoding import CNF
from instance.module.variables import Interval
from output.impl import OptimizeLogger
from typings.work_path import WorkPath

if __name__ == '__main__':
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('BvP_7_4.cnf')

    logs_path = root_path.to_path('logs', 'BvP_7_4')
    solution = Optimize(
        space=SearchSet(
            by_mask=[],
            variables=Interval(start=1, length=3492)
        ),
        executor=ProcessExecutor(max_workers=3),
        sampling=Const(size=1024, split_into=256),
        instance=Instance(
            encoding=CNF(from_file=cnf_file)
        ),
        function=RhoFunction(
            penalty_power=2 ** 20,
            measure=SolvingTime(),
            solver=Glucose3()
        ),
        algorithm=Elitism(
            elites_count=2,
            population_size=6,
            mutation=Doer(),
            crossover=TwoPoint(),
            selection=Roulette(),
            min_update_size=6
        ),
        comparator=MinValueMaxSize(),
        logger=OptimizeLogger(logs_path),
        limitation=WallTime(from_string='09:30:00'),
    ).launch()

    for point in solution:
        print(point)


# [1638 1871 2011 2125 2153 2233 2264 2289 2321 2384 2565 2885 2939](13) by 9208
# [1638 1871 2011 2125 2153 2233 2264 2289 2321 2384 2565 2885 2939](13) by 9208
# [1228 1638 1871 2011 2125 2153 2233 2264 2289 2321 2384 2565 2885 2939](14) by 26464
# [1638 1871 2011 2125 2153 2154 2175 2233 2264 2289 2321 2384 2565 2885 2939](15) by 33760
# [1438 1638 1871 2011 2125 2153 2222 2233 2264 2289 2321 2384 2565 2885 2939](15) by 39712
# [1638 1787 1871 1926 1953 2011 2125 2153 2233 2264 2289 2321 2384 2565 2885 2939](16) by 66496
# [321 1638 1871 2011 2125 2153 2233 2264 2289 2321 2384 2565 2885 2939 3043 3165](16) by 73216
# [802 1638 1871 1926 1953 2011 2125 2153 2233 2264 2289 2304 2321 2384 2405 2565 2885 2939](18) by 263680