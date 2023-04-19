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
        '452 608 1051 1260 2277 2395 2657 2970 3395 3854 4060'
    ]
    backdoors = [
        make_backdoor(Indexes(from_string=str_vars))
        for str_vars in str_backdoors
    ]

    root_path = WorkPath('examples')
    data_path = root_path.to_path('data')
    cnf_file = data_path.to_file('KvD.opb')
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
