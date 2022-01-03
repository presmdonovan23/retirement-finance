class RetirementAnalysis:
    
    def __init__(self, initial_age, retirement_age, death_age, portfolio, deferral_scenario, consumption_scenario, inflation_scenario, cpi_scenario, ssb_scenario):

        self.initial_age = initial_age
        self.retirement_age = retirement_age
        self.death_age = death_age

        self.portfolio = portfolio

        self.deferral_scenario = deferral_scenario
        self.consumption_scenario = consumption_scenario
        self.inflation_scenario = inflation_scenario
        self.cpi_scenario = cpi_scenario
        self.ssb_scenario = ssb_scenario

        self._validate_initial_inputs()

    def _validate_initial_inputs(self):
        if self.deferral_scenario.period != -1:
            raise ValueError('Cannot initialize RetirementAnalysis: deferral_scenario.period = {0}.'.format(self.deferral_scenario.period))

        if self.ssb_scenario.period != -1:
            raise ValueError('Cannot initialize RetirementAnalysis: ssb_scenario.period = {0}.'.format(self.ssb_scenario.period))

        if self.inflation_scenario.period != -1:
            raise ValueError('Cannot initialize RetirementAnalysis: inflation_scenario.period = {0}.'.format(self.inflation_scenario.period))

        if self.cpi_scenario.period != -1:
            raise ValueError('Cannot initialize RetirementAnalysis: cpi_scenario.period = {0}.'.format(self.cpi_scenario.period))

        if self.consumption_scenario.period != -1:
            raise ValueError('Cannot initialize RetirementAnalysis: consumption_scenario.period = {0}.'.format(self.consumption_scenario.period))

    def simulate(self):
        
        for age in range(self.initial_age, self.retirement_age):
            self._step()

    def _step(self):
        self.inflation_scenario.step()
        self.cpi_scenario.step()
        self.deferral_scenario.step()
        self.consumption_scenario.step()
        self.ssb_scenario.step()

        deposit_amt = self.deferral_scenario.value
        withdrawal_amt = self._get_withdrawal()

        self.portfolio.step(deposit_amt=deposit_amt, withdrawal_amt=withdrawal_amt)

    def _get_withdrawal(self):
        return self.consumption_scenario.value - self.ssb_scenario.value

    def plot(self):
        self.inflation_scenario.plot(initial_age=self.initial_age, name='Inflation')
        self.cpi_scenario.plot(initial_age=self.initial_age, name='CPI')
        self.deferral_scenario.plot(initial_age=self.initial_age, name='Deferral')
        self.consumption_scenario.plot(initial_age=self.initial_age, name='Consumption')
        self.ssb_scenario.plot(initial_age=self.initial_age, name='SSB')
