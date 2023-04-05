from threading import Lock
from typing import List, Tuple

from pyscipopt.scip import Model, PY_SCIP_PARAMSETTING

from .PB import PB, PBData

Coef = int
Lit = int
Term = Tuple[Coef, Lit]
PBConstraint = Tuple[List[Term], int]
PBConstraints = List[PBConstraint]

pb_data = {}
parse_lock = Lock()


class PBSCIPData(PBData):
    def __init__(self, pb_constraints: PBConstraints, lines: str = None, max_lit: int = None):
        super().__init__(pb_constraints, lines, max_lit)

        model = Model()

        model.hideOutput()
        model.setParam('display/verblevel', 0)

        variables = dict()

        for pb_constraint in self._pb_constraints:
            terms, b = pb_constraint
            line = -b
            for term in terms:
                if not term[1] in variables:
                    variables[term[1]] = model.addVar(vtype="B", name="x"+str(term[1]), lb=0, ub=1)
                line += term[0] * variables[term[1]]
            model.addCons(line >= 0)

        model.setPresolve(PY_SCIP_PARAMSETTING.AGGRESSIVE)
        model.presolve()
        model.setPresolve(PY_SCIP_PARAMSETTING.DEFAULT)

        self.model = model

    def get_model(self):
        return self.model


class PBSCIP(PB):
    slug = 'encoding:pb:PBSCIP'


__all__ = [
    'PBSCIP',
    'PBSCIPData',
    # types
    'PBConstraint',
    'PBConstraints'
]
