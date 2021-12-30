from refi.series.base_series import BaseSeries


class StaticPreRetirementDeferral(BaseSeries):

    def __init__(self, initial_deferral, cpi, initial_age, retirement_age):
        num_periods = cpi.num_periods
        super().__init__(num_periods)
        self.initial_deferral = initial_deferral  # consumption at retirement in initial_cpi dollars
        self.cpi = cpi
        self.initial_age = initial_age
        self.retirement_age = retirement_age
        self.cumulative_inflation = 0

    def get_next_value(self):

        if self.period < (self.retirement_age - self.initial_age):
            value = self.initial_deferral * (self.cpi.history[self.period] / self.cpi.history[0])
        else:
            value = 0

        return value
