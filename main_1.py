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
from function.impl.function_cr import ChainReaction
from function.module.measure import SolvingTime, Propagations
from function.module.solver.impl import MiniSatPB
from instance.impl import Instance
from instance.module.encoding.impl.PBSCIP import PB
from instance.module.variables import Interval
from output.impl import OptimizeLogger
from typings.work_path import WorkPath

if __name__ == '__main__':
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('BvP_6_4.opb')

    logs_path = root_path.to_path('logs', 'PvS_6_4')
    solution = Optimize(
        space=SearchSet(
            by_mask=[],
            variables=Interval(start=1, length=2276)
        ),
        executor=ProcessExecutor(max_workers=4),
        sampling=Const(size=256, split_into=64),
        instance=Instance(
            encoding=PB(from_file=cnf_file)
        ),
        function=ChainReaction(
            measure=Propagations(),
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

# [344 500 888 891 1058 1581 1773 2108 2286 3153 3530 3594 3756 3771 4001 4227 4261](17) by 224256
# [245 344 500 888 891 1058 1581 1773 2108 3153 3530 3594 3756 3771 4001 4227 4261](17) by 224256
# [344 500 888 891 1058 1581 1773 2108 3153 3530 3594 3720 3756 3771 4001 4227 4261](17) by 285184
# [344 500 888 891 1058 1581 1773 2108 2286 3153 3530 3594 3756 3771 4001 4227 4230 4261](18) by 375808
# [245 344 500 888 891 1058 1581 1773 2108 3046 3153 3530 3594 3756 3771 4001 4227 4261](18) by 381952
# [344 500 888 891 1058 1240 1581 1773 2108 2286 3153 3530 3594 3756 3771 4001 4227 4261 5244 5287 5854](21) by inf
# [344 500 888 891 1058 1581 1773 1833 2108 2286 3153 3530 3594 3756 3771 4001 4227 4261 4553 5244 5287](21) by inf
# [60 137 344 500 888 891 1058 1581 1773 2108 2286 3153 3530 3594 3756 3771 4001 4025 4227 4261](20) by inf