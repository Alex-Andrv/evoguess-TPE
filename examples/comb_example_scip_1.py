# function submodule imports
# other imports
import sys
sys.path.append('/nfs/home/aandreev/evoguess-TPE')
from function.module.solver.impl.scip import Scip
from instance.module.encoding.impl.PBSCIP import PBSCIP


from core.impl import Combine
from executor.impl import ProcessExecutor
from function.module.measure import SolvingTime
# instance module imports
from instance.impl import Instance
from instance.module.variables import Indexes, make_backdoor
from output.impl import OptimizeLogger
from typings.work_path import WorkPath

if __name__ == '__main__':
    str_backdoors = [
        '366 463 1871',
        '5 18 21 31 169 424 783 1078 2982'
    ]
    backdoors = [
        make_backdoor(Indexes(from_string=str_vars))
        for str_vars in str_backdoors
    ]

    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('cvd.opb')
    logs_path = root_path.to_path('logs', 'sgen_150_comb')
    combine = Combine(
        instance=Instance(
            encoding=PBSCIP(from_file=cnf_file)
        ),
        measure=SolvingTime(),
        solver=Scip(),
        logger=OptimizeLogger(logs_path),
        executor=ProcessExecutor(max_workers=1)
    )

    estimation = combine.launch(*backdoors)
    print(estimation)
