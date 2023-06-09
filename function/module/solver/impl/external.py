import os
import re
from subprocess import Popen, TimeoutExpired, PIPE
from tempfile import NamedTemporaryFile as NTFile
from time import time as now

from function.module.measure import Measure
from instance.module.encoding import EncodingData, CNFData
from instance.module.encoding.impl.PBSCIP import PBData
from instance.module.variables.vars import Constraints, Supplements, Assumptions
from util.iterable import concat
from ..solver import Report, Solver, IncrSolver

STATUSES = {
    10: True,
    20: False,
}


class External(Solver):
    limits = {}
    statistic = {}
    root_options = set()
    stdin_file = None
    stdout_file = None
    executable_file = None

    solution = re.compile(r'^v ([-\d ]*)', re.MULTILINE)

    def __init__(self, from_executable: str):
        self.from_executable = from_executable

    def solve(self, encoding_data: EncodingData, measure: Measure,
              supplements: Supplements, add_model: bool = True) -> Report:
        timeout, files, launch_args = None, [], [self.from_executable]

        if isinstance(encoding_data, CNFData):
            source = encoding_data.source(supplements)
        else:
            raise TypeError('External solvers works only with CNF or CNF+ encodings')

        if self.stdin_file is not None:
            with NTFile(delete=False) as in_file:
                in_file.write(source)
                files.append(in_file.name)
                launch_args.append(self.stdin_file % in_file.name)

        if self.stdout_file is not None:
            with NTFile(delete=False) as out_file:
                files.append(out_file.name)
                launch_args.append(self.stdout_file % out_file.name)

        key, value = measure.get_budget()
        if value is not None and key == 'time':
            timeout = value + len(source) * 6e-08
        if value is not None and key in self.limits:
            launch_args.append(self.limits[key] % value)

        timestamp = now()
        process = Popen(launch_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        try:
            data = None if self.stdin_file else source.encode()
            output, error = process.communicate(data, timeout)
            # todo: handle error

            if self.stdout_file is not None:
                with open(files[-1], 'r+') as handle:
                    output = handle.read()
            else:
                output = output.decode()

            stats = {'time': now() - timestamp}
            for key, pattern in self.statistic.items():
                result = pattern.search(output)
                stats[key] = result and int(result.group(1))

            status = STATUSES.get(process.returncode)
            solution = concat(*[
                [int(var) for var in line.split()]
                for line in self.solution.findall(output)
            ]) if add_model and status else None
        except TimeoutExpired:
            process.terminate()
            status, solution = None, None
            stats = {'time': now() - timestamp}
        finally:
            [os.remove(file) for file in files]

        # print(len(supplements[0]), status, stats['time'])
        value, status = measure.check_and_get(stats, status)
        return Report(stats['time'], value, status, solution)

    def propagate(self, encoding_data: EncodingData, measure: Measure,
                  supplements: Supplements, add_model: bool = True) -> Report:
        raise RuntimeError('External solvers supports only solve procedure')

    def use_incremental(self, encoding_data: EncodingData, measure: Measure,
                        constraints: Constraints = ()) -> IncrSolver:
        raise RuntimeError('External solvers supports only solve procedure')


class Kissat(External):
    slug = 'solver:ext:kissat'

    stdin_file = None
    stdout_file = None
    limits = {
        'time': '--time=%d',
        'conflicts': '--conflicts=%d',
        'decisions': '--decisions=%d',
    }
    statistic = {
        'restarts': re.compile(r'^c restarts:\s+(\d+)', re.MULTILINE),
        'conflicts': re.compile(r'^c conflicts:\s+(\d+)', re.MULTILINE),
        'decisions': re.compile(r'^c decisions:\s+(\d+)', re.MULTILINE),
        'propagations': re.compile(r'^c propagations:\s+(\d+)', re.MULTILINE),
        'learned_literals': re.compile(r'^c clauses_learned:\s+(\d+)', re.MULTILINE),
    }


class IncrMiniSatPB(IncrSolver):
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
        return self.solver.propagate(self.encoding_data, self.measure, (assumptions, []), False)

    def propagate(self, assumptions: Assumptions, add_model: bool = True) -> Report:
        return self.solver.propagate(self.encoding_data, self.measure, (assumptions, []), False)


class MiniSatPB(External):
    slug = 'solver:ext:minisatpb'

    STATUSES_MINISATPB = {
        10: True,  # SATISFIABLE
        20: True,  # UNSATISFIABLE
        0: False  # INDETERMINATE
    }

    stdin_file = None
    stdout_file = None
    limits = {
        'time': '--time=%d',
        'conflicts': '--conflicts=%d',
        'decisions': '--decisions=%d',
    }
    statistic = {
        'restarts': re.compile(r'^restarts\s+:\s+(\d+)', re.MULTILINE),
        'conflicts': re.compile(r'^conflicts\s+:\s+(\d+)', re.MULTILINE),
        'decisions': re.compile(r'^decisions\s+:\s+(\d+)', re.MULTILINE),
        'propagations': re.compile(r'^propagations\s+:\s+(\d+)', re.MULTILINE),
        'learned_literals': re.compile(r'^conflict literals\s+:\s+(\d+)', re.MULTILINE),
    }

    def solve(self, encoding_data: EncodingData, measure: Measure,
              supplements: Supplements, add_model: bool = True) -> Report:
        return self.propagate(encoding_data, measure, supplements, add_model)

    def propagate(self, encoding_data: EncodingData, measure: Measure,
                  supplements: Supplements, add_model: bool = True) -> Report:
        # assert measure.key == "time", "only time support"

        timeout, files, launch_args = None, [], [self.from_executable]

        if isinstance(encoding_data, PBData):
            source = encoding_data.source(supplements)
        else:
            raise TypeError('MiniSatPB solvers works only with PB encodings')

        if self.stdin_file is not None:
            with NTFile(delete=False) as in_file:
                in_file.write(source)
                files.append(in_file.name)
                launch_args.append(self.stdin_file % in_file.name)

        if self.stdout_file is not None:
            with NTFile(delete=False) as out_file:
                files.append(out_file.name)
                launch_args.append(self.stdout_file % out_file.name)

        options: set = self.root_options.copy()
        options.add("-only-propagate")
        options.add("-opb")

        key, value = measure.get_budget()
        if value is not None and key == 'time':
            timeout = value + len(source) * 6e-08
        if value is not None and key in self.limits:
            launch_args.append(self.limits[key] % value)
        [launch_args.append(option) for option in options]

        timestamp = now()
        process = Popen(launch_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        try:
            data = None if self.stdin_file else source.encode()
            output, error = process.communicate(data, timeout)
            # todo: handle error
            error = error.decode() # minisat print in error
            if self.stdout_file is not None:
                with open(files[-1], 'r+') as handle:
                    output = handle.read()
            else:
                output = output.decode()

            stats = {'time': now() - timestamp}
            for key, pattern in self.statistic.items():
                result = pattern.search(error)
                stats[key] = result and int(result.group(1))

            status = self.STATUSES_MINISATPB.get(process.returncode)
            assert status != None, 'status can\'t be null'
            # solution = concat(*[
            #     [int(var) for var in line.split()]
            #     for line in self.solution.findall(output)
            # ]) if add_model and status else None
        except TimeoutExpired:
            process.terminate()
            status, solution = None, None
            stats = {'time': now() - timestamp}
        finally:
            [os.remove(file) for file in files]
        assert status != None
        # print(len(supplements[0]), status, stats['time'])
        value, status = measure.check_and_get(stats, status)
        return Report(stats['time'], value, status, None)

    def use_incremental(self, encoding_data: EncodingData, measure: Measure,
                        constraints: Constraints = ()) -> IncrMiniSatPB:
        return IncrMiniSatPB(encoding_data, measure, constraints, self)


__all__ = [
    'Kissat',
    'MiniSatPB'
]
