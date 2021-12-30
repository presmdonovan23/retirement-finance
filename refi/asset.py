import numpy as np

from series import BaseSeries


class StaticReturnAsset(BaseSeries):

    def __init__(self, num_periods, gm_return):
        super().__init__(num_periods)
        self.gm_return = gm_return

    def get_next_value(self):
        return self.gm_return


class StaticInflation:
    def __init__(self, num_periods, initial_cpi, gm_inflation):
        super().__init__(num_periods)
        self.initial_cpi = initial_cpi
        self.gm_inflation = gm_inflation

    def get_next_value(self):
        return self.value * (1 + self.gm_inflation)

    def _update_history(self):
        self.hist_cpi = np.append(self.hist_cpi, self.current_cpi)

    def print_history(self):
        print('Historical CPI:')
        print(self.hist_cpi)