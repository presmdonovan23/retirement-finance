from base_series import BaseSeries


class StaticRetirementSSB(BaseSeries):

    def __init__(self, initial_retirement_ssb, initial_cpi, cpi_series, initial_age, retirement_age):
        num_periods = cpi_series.num_periods + 1
        super().__init__(num_periods)
        self.initial_retirement_ssb = initial_retirement_ssb  # consumption at retirement in initial_cpi dollars
        self.initial_cpi = initial_cpi
        self.cpi_series = cpi_series
        self.initial_age = initial_age
        self.retirement_age = retirement_age

    def get_next_value(self):

        if self.period < (self.retirement_age - self.initial_age):
            value = 0
        else:
            value = self.initial_retirement_ssb * (self.cpi_series.value / self.initial_cpi)

        return value
