# function submodule imports
# other imports
import sys
sys.path.append('/path/to/directory')
from core.impl import Combine
from executor.impl import ProcessExecutor
from function.module.measure import SolvingTime
from function.module.solver import pysat
# instance module imports
from function.module.solver.impl import MiniSatPB, Glucose4
from instance.impl import Instance
from instance.module.encoding import CNF
from instance.module.encoding.impl.PB import PB
from instance.module.variables import Indexes, make_backdoor
from output.impl import OptimizeLogger
from typings.work_path import WorkPath

if __name__ == '__main__':
    str_backdoors = [
        '1929 2224 2596 2598 2599 2607 2655 2923 3390 4060',
    ]
    backdoors = [
        make_backdoor(Indexes(from_string=str_vars))
        for str_vars in str_backdoors
    ]

    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('KvW_12_12.cnf')
    logs_path = root_path.to_path('logs', 'pvs_4_7_comb')
    estimation = Combine(
        instance=Instance(
            encoding=CNF(from_file=cnf_file)
        ),
        measure=SolvingTime(),
        solver=Glucose4(),
        logger=OptimizeLogger(logs_path),
        executor=ProcessExecutor(max_workers=1)
    ).launch(*backdoors)

    print(estimation)
