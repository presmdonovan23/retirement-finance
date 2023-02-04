import numpy as np


class RetirementSimulation:
    
    def __init__(self, initial_age, retirement_age, death_age, portfolio, deferral_scenario, consumption_scenario, inflation_scenario, cpi_scenario, ssb_scenario):

        self.period = -1
        self.initial_age = initial_age
        self.retirement_age = retirement_age
        self.death_age = death_age
        self.ind_at_ret = self.retirement_age - self.initial_age
        self.portfolio = portfolio

        self.deferral_scenario = deferral_scenario
        # TODO: Error is thrown when portfolio depletes. need separate target consumption and withdrawal scenarios in order to produce realized consumption
        self.target_consumption_scenario = consumption_scenario
        self.inflation_scenario = inflation_scenario
        self.cpi_scenario = cpi_scenario
        self.ssb_scenario = ssb_scenario
        self.consumption = self._initialize_lifetime_array()
        self._validate_initial_inputs()

    def _initialize_lifetime_array(self, default_value=np.nan):
        arr = np.array([default_value for _ in range(self.initial_age, self.death_age)])
        return arr

    def _validate_initial_inputs(self):
        if self.deferral_scenario.period != -1:
            raise ValueError('Cannot initialize RetirementSimulation: deferral_scenario.period = {0}.'.format(self.deferral_scenario.period))

        if self.ssb_scenario.period != -1:
            raise ValueError('Cannot initialize RetirementSimulation: ssb_scenario.period = {0}.'.format(self.ssb_scenario.period))

        if self.inflation_scenario.period != -1:
            raise ValueError('Cannot initialize RetirementSimulation: inflation_scenario.period = {0}.'.format(self.inflation_scenario.period))

        if self.cpi_scenario.period != -1:
            raise ValueError('Cannot initialize RetirementSimulation: cpi_scenario.period = {0}.'.format(self.cpi_scenario.period))

        if self.target_consumption_scenario.period != -1:
            raise ValueError('Cannot initialize RetirementSimulation: consumption_scenario.period = {0}.'.format(self.target_consumption_scenario.period))

    def simulate(self):
        self.initialize()

        for age in range(self.initial_age, self.death_age):
            self.period += 1
            self._step()

    def initialize(self):
        self.period += 1
        self.portfolio.step()
        self.inflation_scenario.step()
        self.cpi_scenario.step()
        self.deferral_scenario.step()
        self.target_consumption_scenario.step()
        self.ssb_scenario.step()

    def _step(self):

        deposit_amt = self.deferral_scenario.value
        withdrawal_amt = self._get_withdrawal()
        self.portfolio.step(deposit_amt=deposit_amt, withdrawal_amt=withdrawal_amt)

        self.inflation_scenario.step()
        self.cpi_scenario.step()
        self.deferral_scenario.step()
        self.target_consumption_scenario.step()
        self.ssb_scenario.step()


    def _get_withdrawal(self):
        target_withdrawal = self.target_consumption_scenario.value - self.ssb_scenario.value
        withdrawal = min(self.portfolio.value, target_withdrawal)
        return withdrawal

    def plot(self):
        self.portfolio.plot(initial_age=self.initial_age, name='Balance')
        self.inflation_scenario.plot(initial_age=self.initial_age, name='Inflation')
        self.cpi_scenario.plot(initial_age=self.initial_age, name='CPI')
        self.deferral_scenario.plot(initial_age=self.initial_age, name='Deferral')
        self.target_consumption_scenario.plot(initial_age=self.initial_age, name='Consumption')
        self.ssb_scenario.plot(initial_age=self.initial_age, name='SSB')
        
        
