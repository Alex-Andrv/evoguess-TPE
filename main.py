from algorithm.impl.tree_structured_parzen import TreeStructuredParzen
from core.impl import Optimize
from core.module.comparator import MinValueMaxSize
from core.module.limitation import WallTime
from core.module.sampling import Const
from core.module.space import InputSet
from executor.impl import ProcessExecutor
from function.impl import InverseBackdoorSets
from function.module.measure import SolvingTime
from function.module.solver import pysat
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
        space=InputSet(),
        executor=ProcessExecutor(max_workers=32),
        sampling=Const(size=50, split_into=10),
        instance=StreamCipher(
            encoding=CNF(from_file=cnf_file),
            input_set=Interval(start=1, length=64),
            output_set=Interval(start=14375, length=64)
        ),
        function=InverseBackdoorSets(
            measure=SolvingTime(budget=60),
            solver=pysat.Glucose3()
        ),
        algorithm=TreeStructuredParzen(min_update_size=6, max_backdoor_mask_len=64),
        comparator=MinValueMaxSize(),
        logger=OptimizeLogger(logs_path),
        limitation=WallTime(from_string='00:11:00'),
    ).launch()

    for point in solution:
        print(point)
