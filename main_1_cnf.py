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
from function.module.solver.impl import Glucose3, Minisat22
from instance.impl import Instance
from instance.module.encoding import CNF
from instance.module.variables import Interval
from output.impl import OptimizeLogger
from typings.work_path import WorkPath

if __name__ == '__main__':
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('PvS_8_4.cnf')

    logs_path = root_path.to_path('logs', 'test')
    solution = Optimize(
        space=SearchSet(
            by_mask=[],
            variables=Interval(start=1, length=6885)
        ),
        executor=ProcessExecutor(max_workers=4),
        sampling=Const(size=1024, split_into=256),
        instance=Instance(
            encoding=CNF(from_file=cnf_file)
        ),
        function=RhoFunction(
            penalty_power=2 ** 20,
            measure=SolvingTime(),
            solver=Minisat22()
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