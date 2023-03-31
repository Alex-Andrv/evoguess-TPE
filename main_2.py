from algorithm.impl import Elitism
from algorithm.impl.tree_structured_parzen import TreeStructuredParzen
from algorithm.module.crossover import TwoPoint
from algorithm.module.mutation import Doer
from algorithm.module.selection import Roulette
from core.impl import Optimize
from core.module.comparator import MinValueMaxSize
from core.module.limitation import WallTime
from core.module.sampling import Const
from core.module.space import InputSet, SearchSet
from executor.impl import ProcessExecutor
from function.impl import InverseBackdoorSets, RhoFunction
from function.module.measure import SolvingTime, Propagations
from function.module.solver import pysat, Kissat
from instance import Instance
from instance.impl import StreamCipher
from instance.module.encoding import CNF
from instance.module.variables import Interval
from output.impl import OptimizeLogger
from typings.work_path import WorkPath

if __name__ == '__main__':
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('a5_1_64_1.cnf')

    logs_path = root_path.to_path('logs', 'test')
    solution = Optimize(
        space=SearchSet(
            by_mask=[],
            variables=Interval(start=1, length=500)
        ),
        executor=ProcessExecutor(max_workers=8),
        sampling=Const(size=1024, split_into=256),
        instance=Instance(
            encoding=CNF(from_file=cnf_file)
        ),
        function=RhoFunction(
            penalty_power=2 ** 40,
            measure=Propagations(),
            solver=Kissat("/Users/alexanderandreev/CLionProjects/kissat/build/kissat")
        ),
        # algorithm=Elitism(
        #     elites_count=2,
        #     population_size=6,
        #     mutation=Doer(),
        #     crossover=TwoPoint(),
        #     selection=Roulette(),
        #     min_update_size=6
        # ),
        algorithm=TreeStructuredParzen(min_update_size=6, max_backdoor_mask_len=500, min_cnt_var=20,
                                       max_cnt_var=40, n_startup_trials=1000),
        comparator=MinValueMaxSize(),
        logger=OptimizeLogger(logs_path),
        limitation=WallTime(from_string='08:00:00'),
    ).launch()

    for point in solution:
        print(point)
