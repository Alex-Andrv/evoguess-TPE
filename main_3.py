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
from function.module.solver.impl import MiniSatPB
from instance.impl import Instance
from instance.module.encoding.impl.PBSCIP import PB
from instance.module.variables import Interval
from output.impl import OptimizeLogger
from typings.work_path import WorkPath

if __name__ == '__main__':
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('BvP_7_4_min_new.opb')

    logs_path = root_path.to_path('logs', 'BvP_7_4')
    solution = Optimize(
        space=SearchSet(
            by_mask=[],
            variables=Interval(start=1, length=3492)
        ),
        executor=ProcessExecutor(max_workers=4),
        sampling=Const(size=256, split_into=64),
        instance=Instance(
            encoding=PB(from_file=cnf_file)
        ),
        function=RhoFunction(
            penalty_power=2 ** 10,
            measure=SolvingTime(),
            solver=MiniSatPB("/Users/alexanderandreev/CLionProjects/minisat_latest/cmake-build-debug/minisat")
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

# [27 135 817 866 927 976 1142 1210](8) by 436
# [27 135 817 866 927 976 1142](7) by 443
# [27 135 253 512 817 866 927 954 976 1142 1151 1210 1493 1520 2517 3010](16) by inf
# [27 135 253 512 817 866 927 954 976 1142 1210 1259 1493 1520 3488](15) by inf
# [27 135 817 866 927 954 976 1142 1210 1493 1520 2157 2517 3324](14) by inf
# [27 135 154 253 512 817 866 927 976 1142 1210 1921 3010 3488](14) by inf
# [27 135 817 866 927 976 1142 1210 2157 2517 2647 3010](12) by inf
# [27 135 817 866 927 976 1142 1210 2441 3430](10) by inf