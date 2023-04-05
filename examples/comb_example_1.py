# function submodule imports
from function.module.solver import pysat
from function.module.measure import SolvingTime

# instance module imports
from function.module.solver.impl.scip import Scip
from instance.impl import Instance
from instance.module.encoding import CNF
from instance.module.encoding.impl.PB import PB
from instance.module.variables import Indexes, make_backdoor

# other imports
from core.impl import Combine
from output.impl import OptimizeLogger
from typings.work_path import WorkPath
from executor.impl import ProcessExecutor


if __name__ == '__main__':
    str_backdoors = [
        '279 1280 1465 1828 1858 2220'
    ]
    backdoors = [
        make_backdoor(Indexes(from_string=str_vars))
        for str_vars in str_backdoors
    ]

    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('WvC.opb')
    logs_path = root_path.to_path('logs', 'sgen_150_comb')
    combine = Combine(
        instance=Instance(
            encoding=PB(from_file=cnf_file)
        ),
        measure=SolvingTime(),
        solver=Scip(),
        logger=OptimizeLogger(logs_path),
        executor=ProcessExecutor(max_workers=8)
    )

    estimation = combine.launch(*backdoors)
    print(estimation)
