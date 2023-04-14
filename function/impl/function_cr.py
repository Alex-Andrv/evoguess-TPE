import math
import statistics
from itertools import chain
from math import log2
from os import getpid
from random import random
from time import time as now
from typing import Tuple
from ..abc.function import Function

from ..abc.function import aggregate_results
from ..models import WorkerArgs, WorkerResult, \
    WorkerCallable, Payload, Results, Estimation, Status, TimeMap, StatusMap
from .function_gad import GuessAndDetermine, gad_supplements

from function.module.solver import Solver
from function.module.measure import Measure, Propagations
from instance.module.variables import Backdoor

def harmonic_mean(nums):
    return len(nums) / sum(1 / num for num in nums)

def aggregate_results_mean(results: Results) -> Tuple[TimeMap, int, StatusMap, int, int]:
    all_times, all_values, all_statuses, full_ptime = {}, {Status.SOLVED: [], Status.RESOLVED: []}, {}, 0
    for _, ptime, times, values, statuses, _ in results:
        full_ptime += ptime
        for status, time in times.items():
            all_times[status] = all_times.get(status, 0.) + time
        for status, value in values.items():
            all_values[status].extend(value)
        for status, count in statuses.items():
            all_statuses[status] = all_statuses.get(status, 0) + count
    median = harmonic_mean(list(chain.from_iterable(list(all_values.values()))))
    return all_times, median, all_statuses, sum(all_statuses.values()), full_ptime

def ch_worker_fn(args: WorkerArgs, payload: Payload) -> WorkerResult:
    space, solver, measure, instance, bytemask = payload
    backdoor, timestamp = space.unpack(instance, bytemask), now()

    times, values, statuses = {}, {}, {}
    encoding_data = instance.encoding.get_data()
    with solver.use_incremental(encoding_data, measure) as incremental:
        for assumptions, _ in gad_supplements(args, instance, backdoor):
            # todo: use constraints with incremental propagation?
            time, value, status, _ = incremental.propagate(assumptions, add_model=False)

            times[status.value] = times.get(status.value, 0.) + time
            if status.value not in values:
                values[status.value] = []
            if status.value == Status.RESOLVED:
                values[status.value].append(backdoor._length)
            elif status.value == Status.SOLVED:
                values[status.value].append(value)
            elif status.value == Status.INTERRUPTED:
                raise Exception("something strange")
            statuses[status.value] = statuses.get(status.value, 0) + 1
    return getpid(), now() - timestamp, times, values, statuses, args

class ChainReaction(Function):
    slug = 'function:rho'

    def __init__(self, solver: Solver, measure: Measure):
        super().__init__(solver, measure)
        assert isinstance(measure, Propagations)

    def get_worker_fn(self) -> WorkerCallable:
        return ch_worker_fn

    def calculate(self, backdoor: Backdoor, results: Results) -> Estimation:
        times, median, statuses, count, ptime = aggregate_results_mean(results)
        power, time_sum = backdoor.power(), sum(times.values())

        value = math.sqrt(((backdoor.power() / (median + 1)) ** 2 + (1 - median / backdoor._length) ** 2) / 2)

        return {
            'count': count,
            'value': round(value, 6),
            'ptime': round(ptime, 4),
            'size': len(backdoor),
            'statuses': statuses,
            'time_sum': round(time_sum, 4),
        }

__all__ = [
    'ChainReaction'
]