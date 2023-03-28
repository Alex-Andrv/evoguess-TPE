import random
from typing import List, TYPE_CHECKING

import optuna
from optuna import Study, Trial
from optuna.distributions import IntDistribution, CategoricalDistribution
from optuna.samplers import TPESampler
from optuna.trial import TrialState, FrozenTrial

from instance.module.variables import Backdoor, Interval
from typings.optional import Int
from ..abc import Algorithm
from ..abc.algorithm import PointManager

if TYPE_CHECKING:
    from core.model.point import Vector, Point


class TreeStructuredParzen(Algorithm):
    slug = 'algorithm:TPE'

    @staticmethod
    def get_mask(cnt_var_in_backdoor, max_backdoor_mask_len):
        mask = [1] * cnt_var_in_backdoor + [0] * (max_backdoor_mask_len - cnt_var_in_backdoor)
        random.shuffle(mask)
        return mask

    def __init__(self, min_update_size: int, max_backdoor_mask_len: int, n_startup_trials: int = 5000, top_n: int = 100,
                 max_cnt_var: int = 30, max_queue_size: Int = None):
        super().__init__(min_update_size, max_queue_size)
        self.max_backdoor_mask_len = max_backdoor_mask_len
        # название так себе, возможно стоит использовать SearchSet TODO remove comment
        sampler: TPESampler = optuna.samplers.TPESampler(seed=42, n_startup_trials=0, constant_liar=True, warn_independent_sampling=False)
        self.study: Study = optuna.create_study(direction='minimize', sampler=sampler,
                                                pruner=optuna.pruners.NopPruner())
        self.top_n = top_n
        self.trails_cache: list[int] = []
        self.used = dict()
        self.max_cnt_var = max_cnt_var
        self.collision = 0
        for n_startup in range(n_startup_trials):
            assert max_cnt_var < max_backdoor_mask_len
            cnt_var_in_backdoor = random.randint(1, max_cnt_var)
            mask = self.get_mask(cnt_var_in_backdoor, max_backdoor_mask_len)
            self.study.enqueue_trial(skip_if_exists=True, params={f'x{i}': mask[i] for i in range(len(mask))})

    def start(self, point: 'Point') -> PointManager:
        mask: List[int] = point.backdoor.get_mask()
        params: dict = {f'x{i}': mask[i] for i in range(len(mask))}
        distributions: dict = {f'x{i}': CategoricalDistribution(choices=[0, 1]) for i in range(len(mask))}
        trial: FrozenTrial = optuna.trial.create_trial(
            state=TrialState.COMPLETE,
            params=params,
            distributions=distributions,
            value=point.value(),
        )
        self.study.add_trial(trial)
        # assert len(self.study.trials) == 1, "aandreev don't understand how evogess work"
        return PointManager(self, point)

    def get_backdoor(self) -> 'Backdoor':

        backdoor: Backdoor = Backdoor(from_vars=Interval(start=1, length=self.max_backdoor_mask_len).variables())

        while not self._get_backdoor(backdoor):
            # TPESample если его использовать параллельно, может генерировать одинаковые точки
            # флаг constant_liar=True сильно не помогает, приходится генерировать точку рандомно, можно считать это
            # стратегией exploration
            cnt_var_in_backdoor = random.randint(1, self.max_cnt_var)
            mask = self.get_mask(cnt_var_in_backdoor, self.max_backdoor_mask_len)
            self.study.enqueue_trial(skip_if_exists=True, params={f'x{i}': mask[i] for i in range(len(mask))})

        return backdoor

    def update(self, vector: 'Vector', *points: 'Point') -> 'Vector':
        for point in points:
            trail_number: int = self.used[repr(point.backdoor)]
            # if trail_number in self.used:
            #     # некоторые значения могут доставаться из кеша и у них будет не верный trail_number
            #     # поэтому приходится их пропускать TODO remove comment
            #     print(f"skipp cached value {trail_number}")
            #     continue
            self.study.tell(trail_number, point.value())
            # сказать оптимизатору, что на trail_number достигается значение point.value() TODO remove comment
            vector.append(point)
            # вероятно нам не нужны все точки. Можно взять top n TODO remove comment
        self.trails_cache = []
        vector.sort()
        return vector[:self.top_n]

    def next(self, vector: 'Vector', count: int) -> List['Backdoor']:
        res = [self.get_backdoor() for _ in range(count)]
        return res

    def __info__(self):
        return {
            'slug': self.slug,
            'max_backdoor_mask_len': self.max_backdoor_mask_len
        }

    def _get_backdoor(self, backdoor):
        trial: Trial = self.study.ask()
        # вернуть trial, с помощью которого можно сгенерировать значения TODO remove comment
        mask: List[int] = backdoor.get_mask()
        for i in range(self.max_backdoor_mask_len):
            take_x_i = trial.suggest_categorical(name=f'x{i}', choices=[0, 1])
            mask[i] = take_x_i

        backdoor._set_mask(mask)
        # метод приватный, но кажется по другому нельзя TODO remove comment

        if repr(backdoor) in self.used:
            self.collision += 1
            print(f"backdoor is used: {self.collision}")
            self.study.tell(trial, state=optuna.trial.TrialState.PRUNED)
            return False
        else:
            self.used[repr(backdoor)] = trial.number
            # необходимо запомнить trail.number, чтобы потом вызвать tell на нем TODO remove comment
            return True


__all__ = [
    'TreeStructuredParzen'
]
