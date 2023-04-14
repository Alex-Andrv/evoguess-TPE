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
from function.module.solver.impl.scip import Scip
from instance.impl import Instance
from instance.module.encoding import CNF
from instance.module.encoding.impl.PBSCIP import PBSCIP
from instance.module.variables import Interval
from output.impl import OptimizeLogger
from typings.work_path import WorkPath

if __name__ == '__main__':
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('SvP_9_4_min_new.opb')

    logs_path = root_path.to_path('logs', 'SvP_9_4')
    solution = Optimize(
        space=SearchSet(
            by_mask=[],
            variables=Interval(start=1, length=9689)
        ),
        executor=ProcessExecutor(max_workers=4),
        sampling=Const(size=256, split_into=64),
        instance=Instance(
            encoding=PBSCIP(from_file=cnf_file)
        ),
        function=RhoFunction(
            penalty_power=2 ** 20,
            measure=SolvingTime(),
            solver=Scip()
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

# [1674 2105 2432 2823 2970 3063 3302 3446 3532 4391 4901 5555 6819 9250 9304](15) by 104192
# [1647 1670 1674 2105 2432 2823 2970 3063 3302 3532 4391 4901 5555 6819 9250 9304](16) by 107776
# [1674 2105 2235 2432 2823 2970 3063 3302 3532 4391 4901 5555 6819 7037 9250 9304](16) by 173056
# [1647 1670 1674 2105 2432 2823 2970 3063 3302 3532 4391 4901 5555 6494 6819 9250 9304](17) by 174080
# [1647 1670 1674 2105 2432 2687 2823 2970 3063 3302 3532 4391 4901 5555 6819 7252 9250 9304](18) by 280576
# [1674 2105 2432 2823 2970 3063 3302 3446 3532 4391 4901 5555 6819 7318 7543 8503 9250 9304](18) by 338944
# [773 1647 1670 1674 2020 2105 2432 2823 2970 3063 3302 3446 3532 4391 4420 4790 4901 5435 5555 6819 7318 9250 9304](23) by inf
# [1243 1647 1670 1674 2105 2432 2823 2970 3063 3302 3446 3532 4391 4901 5555 6819 7318 8503 9250 9304](20) by inf