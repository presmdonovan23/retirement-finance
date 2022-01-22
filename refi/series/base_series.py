import numpy as np
import matplotlib.pyplot as plt


class BaseSeries:

    def __init__(self, num_periods):
        self.num_periods = num_periods
        self.history = np.array([np.nan for _ in range(self.num_periods)])
        self.value = np.nan
        self.period = -1

    def plot(self, initial_age=None, name=None):

        xlabel = 'Period' if initial_age is None else 'Age'

        offset = 0 if initial_age is None else initial_age
        x = np.array([period + offset for period in range(self.period + 1)])

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(x, self.history[:self.period + 1], '.-')
        ax.set_xlabel(xlabel)
        ax.set_title(name)
        plt.show()

    def step_all(self):
        while self.period < (self.num_periods - 1):
            self.step()

    def step(self, **kwargs):
        if self.period == (self.num_periods - 1):
            raise IndexError('Final period {0} reached, cannot step further.'.format(self.period))

        self.period += 1

        try:
            self.value = self.get_next_value(**kwargs)
        except BaseException as err:
            print(err)
            self.period -= 1
            raise RuntimeError('get_next_value() failed.')

        self._update_history()

    def get_next_value(self, **kwargs):
        raise NotImplementedError

    def get_previous_value(self):
        return self.history[self.period - 1]

    def _update_history(self):
        self.history[self.period] = self.value


class StaticSeries(BaseSeries):

    def __init__(self, num_periods, static_value):
        super().__init__(num_periods)
        self.static_value = static_value

    def get_next_value(self):
        return self.static_value


class StaticGrowthSeries(BaseSeries):

    def __init__(self, initial_value: float, growth_series: BaseSeries):
        num_periods = growth_series.num_periods  # technically could compute this series for num_periods+1
        super().__init__(num_periods)
        self.initial_value = initial_value
        self.growth_series = growth_series

    def get_next_value(self):
        if self.period > (self.growth_series.period + 1):
            raise ValueError('Cannot get_next_value: cannot calculate value for period {0} when growth_series is only at period {1}.'.format(self.period, self.growth_series.period))

        if self.period == 0:
            value = self.initial_value
        else:
            value = self.get_previous_value() * (1 + self.growth_series.history[self.period-1])

        return value


class PositiveGaussianSeries(BaseSeries):
    min_possible_return = -.9999

    def __init__(self, num_periods, mean, std_dev):
        super().__init__(num_periods)
        self.mean = mean
        self.std_dev = std_dev

    def get_next_value(self):

        val = np.random.normal(loc=self.mean, scale=self.std_dev)
        val = np.clip(val, a_min=self.min_possible_return, a_max=None)

        return val