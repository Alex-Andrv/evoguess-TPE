# function submodule imports
# other imports
import sys
sys.path.append('/nfs/home/aandreev/evoguess-TPE')
from function.module.solver.impl.scip import Scip
from instance.module.encoding.impl.PBSCIP import PBSCIP


from core.impl import Combine
from executor.impl import ProcessExecutor
from function.module.measure import SolvingTime, Conflicts
# instance module imports
from function.module.solver.impl import Glucose4
from instance.impl import Instance
from instance.module.encoding import CNF
from instance.module.variables import Indexes, make_backdoor
from output.impl import OptimizeLogger
from typings.work_path import WorkPath

if __name__ == '__main__':
    str_backdoors = [
        '1708 2393 3313 3322',
        '2190 3536 3560 3729 4066 4069 4107 4246 4422 4942'
    ]
    backdoors = [
        make_backdoor(Indexes(from_string=str_vars))
        for str_vars in str_backdoors
    ]

    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('dvk.opb')
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
