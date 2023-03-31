from algorithm.impl.tree_structured_parzen import TreeStructuredParzen
from core.impl import Optimize
from core.module.comparator import MinValueMaxSize
from core.module.limitation import WallTime
from core.module.sampling import Const
from core.module.space import InputSet, SearchSet
from executor.impl import ProcessExecutor
from function.impl import InverseBackdoorSets, RhoFunction
from function.module.measure import SolvingTime, Propagations
from function.module.solver import pysat
from instance import Instance
from instance.impl import StreamCipher
from instance.module.encoding import CNF
from instance.module.variables import Interval
from output.impl import OptimizeLogger
from typings.work_path import WorkPath

if __name__ == '__main__':
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('a5_1_64.cnf')

    logs_path = root_path.to_path('logs', 'test')
    solution = Optimize(
        space=SearchSet(
            by_mask=[],
            variables=Interval(start=1, length=150)
        ),
        executor=ProcessExecutor(max_workers=16),
        sampling=Const(size=16384, split_into=4096),
        instance=Instance(
            encoding=CNF(from_file=cnf_file)
        ),
        function=RhoFunction(
            penalty_power=2 ** 30,
            measure=Propagations(),
            solver=pysat.Glucose3()
        ),
        algorithm=TreeStructuredParzen(min_update_size=6, max_backdoor_mask_len=150),
        comparator=MinValueMaxSize(),
        logger=OptimizeLogger(logs_path),
        limitation=WallTime(from_string='11:00:00'),
    ).launch()

    for point in solution:
        print(point)
