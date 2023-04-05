# function submodule imports
# other imports
from core.impl import Combine
from executor.impl import ProcessExecutor
from function.module.measure import SolvingTime
from function.module.solver import pysat
# instance module imports
from instance.impl import Instance
from instance.module.encoding import CNF
from instance.module.variables import Indexes, make_backdoor
from output.impl import OptimizeLogger
from typings.work_path import WorkPath

if __name__ == '__main__':
    str_backdoors = [
        '387 1445 1584 1610 3049',
    ]
    backdoors = [
        make_backdoor(Indexes(from_string=str_vars))
        for str_vars in str_backdoors
    ]

    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('pvs_4_7.cnf', 'sort')
    logs_path = root_path.to_path('logs', 'pvs_4_7_comb')
    estimation = Combine(
        instance=Instance(
            encoding=CNF(from_file=cnf_file)
        ),
        measure=SolvingTime(),
        solver=pysat.Glucose3(),
        logger=OptimizeLogger(logs_path),
        executor=ProcessExecutor(max_workers=4)
    ).launch(*backdoors)

    print(estimation)
