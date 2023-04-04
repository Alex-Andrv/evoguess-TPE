from function.module.measure import Measure
from function.module.solver import Solver, Report, IncrSolver
from instance.module.encoding import EncodingData
from instance.module.encoding.impl.PB import PBData
from instance.module.variables.vars import Supplements, Constraints, Assumptions
from pyscipopt.scip import Model


def propagate(measure, encoding_data: EncodingData, assumptions):
    if not isinstance(encoding_data, PBData):
        raise TypeError('SCIP works only with PB encodings')

    model = Model(sourceModel=encoding_data.get_model(), threadsafe=False)

    for var_assumption in assumptions:
        var_index = abs(var_assumption) - 1
        variable = model.getVars()[var_index]

        if var_assumption > 0:
            model.addCons(variable == 1)
        else:
            model.addCons(variable == 0)

    model.presolve()

    # evoguess: The status is ``True`` if conflict arisen
    # during propagation or all literals in formula assigned.
    # Otherwise, the status is ``False``.
    status = model.getStatus() == "infeasible"
    stats = {'time': model.getPresolvingTime()}
    value, status = measure.check_and_get(stats, status)

    return Report(stats['time'], value, status, None)


class IncrScip(IncrSolver):
    # вот я хз что я сделал
    solver = None
    last_fixed_value = None

    def __init__(self, encoding_data: EncodingData, measure: Measure,
                 constraints: Constraints, solver: Solver):
        super().__init__(encoding_data, measure, constraints)
        self.solver = solver

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def solve(self, assumptions: Assumptions, add_model: bool = True) -> Report:
        return propagate(self.measure, self.encoding_data, assumptions)

    def propagate(self, assumptions: Assumptions, add_model: bool = True) -> Report:
        return propagate(self.measure, self.encoding_data, assumptions)


class Scip(Solver):
    slug = 'solver:scip'

    def propagate(self, encoding_data: EncodingData, measure: Measure,
                  supplements: Supplements, add_model: bool) -> Report:
        assert measure.key == "time", "support only time"
        assert add_model == False
        if not isinstance(encoding_data, PBData):
            raise TypeError('SCIP works only with PB encodings')

        assumptions, _ = supplements
        return propagate(measure, encoding_data, assumptions)

    def use_incremental(self, encoding_data: EncodingData, measure: Measure,
                        constraints: Constraints = ()) -> IncrSolver:
        assert constraints == ()
        return IncrScip(encoding_data, measure, constraints, self)
