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
from function.module.solver.impl.scip import Scip
from instance.impl import Instance
from instance.module.encoding.impl.PBSCIP import PB, PBSCIP
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
            encoding=PB(from_file=cnf_file)
        ),
        function=RhoFunction(
            penalty_power=2 ** 20,
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

# [1177 1903 2100 2214 2281 3039 3351 3451 3478 3569 3694 3991 8056 8605 8626 8775](16) by 284416
# [1177 1903 2100 2214 2281 2411 3039 3351 3451 3478 3569 3694 3991 8056 8605 8626 8775](17) by 285184
# [1177 1903 2100 2214 2281 3039 3351 3451 3478 3569 3694 3991 5970 8056 8605 8626 8775](17) by 346112
# [1177 1903 2100 2214 2281 3039 3351 3451 3478 3569 3694 3991 4436 5501 8056 8605 8626 8775](18) by 437248
# [1177 1903 2100 2214 2281 2641 3039 3351 3451 3478 3569 3694 3991 7736 8056 8605 8626 8775](18) by 464896
# [1177 1903 2100 2214 2281 3039 3351 3451 3478 3569 3694 3991 6437 7736 8056 8605 8626 8775](18) by 517120
# [1177 1903 2100 2214 2281 3039 3351 3451 3478 3569 3694 3991 7146 7736 7871 8056 8605 8626 8775](19) by 673792
# [1177 1696 1903 1942 2100 2214 2281 2411 3039 3351 3451 3478 3569 3694 3991 6646 8056 8605 8626 8775](20) by inf