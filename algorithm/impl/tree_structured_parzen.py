from typing import List, TYPE_CHECKING

import optuna
from optuna import Study, Trial
from optuna.samplers import TPESampler

from instance.module.variables import Backdoor, Interval
from typings.optional import Int
from ..abc import Algorithm

if TYPE_CHECKING:
    from core.model.point import Vector, Point


class TreeStructuredParzen(Algorithm):
    slug = 'algorithm:TPE'

    def __init__(self, min_update_size: int, max_backdoor_mask_len: int, max_queue_size: Int = None):
        super().__init__(min_update_size, max_queue_size)
        self.max_backdoor_mask_len = max_backdoor_mask_len  # название так себе
        sampler: TPESampler = optuna.samplers.TPESampler(seed=42)
        self.study: Study = optuna.create_study(direction='minimize', sampler=sampler)
        self.trails_cache: list[int] = []
        self.used = set()

    def get_backdoor(self) -> 'Backdoor':
        trail: Trial = self.study.ask()
        backdoor: Backdoor = Backdoor(from_vars=Interval(start=1, length=self.max_backdoor_mask_len).variables())
        mask: List[int] = backdoor.get_mask()
        for i in range(self.max_backdoor_mask_len):
            take_x_i = trail.suggest_int(f'x{i}', 0, 1, step=1)
            mask[i] = take_x_i
        backdoor.set_trial_number(trail.number)
        return backdoor._set_mask(mask)


    def update(self, vector: 'Vector', *points: 'Point') -> 'Vector':
        for point in points:
            trail_number: int = point.backdoor.trial_number
            if trail_number in self.used:
                print(f"skipp cached value {trail_number}")
                continue
            self.study.tell(trail_number, point.value())
            self.used.add(trail_number)
            vector.append(point)
        self.trails_cache = []
        return vector

    def next(self, vector: 'Vector', count: int) -> List['Backdoor']:
        res = [self.get_backdoor() for _ in range(count)]
        return res

    def __info__(self):
        return {
            'slug': self.slug,
            'max_backdoor_mask_len': self.max_backdoor_mask_len
        }


__all__ = [
    'TreeStructuredParzen'
]
