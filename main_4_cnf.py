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
from function.impl.function_cr import ChainReaction, quadratic_weight_harmonic_mean, harmonic_mean
from function.module.measure import SolvingTime, Propagations
from function.module.solver.impl import Glucose3, Minisat22
from instance.impl import Instance
from instance.module.encoding import CNF
from instance.module.variables import Interval
from output.impl import OptimizeLogger
from typings.work_path import WorkPath

if __name__ == '__main__':
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('KvW_12_12.cnf')

    logs_path = root_path.to_path('logs', 'KvW_12_12')
    solution = Optimize(
        space=SearchSet(
            by_mask=[],
            variables=Interval(start=1, length=5088)
        ),
        executor=ProcessExecutor(max_workers=4),
        sampling=Const(size=1024 * 4, split_into=1024),
        instance=Instance(
            encoding=CNF(from_file=cnf_file)
        ),
        function=ChainReaction(
            measure=Propagations(),
            solver=Glucose3(),
            mean_fun=harmonic_mean
        ),
        algorithm=Elitism(
            elites_count=9,
            population_size=20,
            mutation=Doer(),
            crossover=TwoPoint(),
            selection=Roulette(),
            min_update_size=20
        ),
        comparator=MinValueMaxSize(),
        logger=OptimizeLogger(logs_path),
        limitation=WallTime(from_string='09:30:00'),
    ).launch()

    for point in solution:
        print(point)


# [159 257 261 341 1240 2411 3579 3781 3807 4380 4645 5365 6033](13) by 12256
# [159 257 261 341 1240 2411 3579 3781 3807 4380 4645 5365 6033](13) by 12256
# [159 200 257 261 341 1240 2411 3579 3781 3807 4380 4645 5365 6033](14) by 24448
# [159 257 261 341 447 1240 2411 3579 3781 3807 4380 4645 5144 5365 6033](15) by 44672
# [159 257 261 341 1240 2242 2319 2411 3579 3781 3807 4380 4645 5365 6033](15) by 47648
# [159 257 261 341 1240 1535 2411 3579 3781 3807 4291 4380 4645 5365 6033 6045](16) by 84736
# [159 257 261 341 929 973 1240 1586 2411 3579 3781 3807 4380 4645 4855 5365 6033](17) by 140928
# [159 257 261 341 1240 2351 2411 3234 3387 3579 3781 3807 4380 4645 5365 6033 6544](17) by 143616