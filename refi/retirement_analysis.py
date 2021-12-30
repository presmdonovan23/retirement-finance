class RetirementAnalysis:
    
    def __init__(self, initial_age, retirement_age, death_age, portfolio, deferral_scenario, consumption_scenario, inflation_scenario, ssb_scenario):
        
        self.initial_age = initial_age
        self.retirement_age = retirement_age
        self.death_age = death_age

        self.portfolio = portfolio

        self.deferral_scenario = deferral_scenario
        self.consumption_scenario = consumption_scenario
        self.inflation_scenario = inflation_scenario
        self.ssb_scenario = ssb_scenario

    def simulate(self):
        
        for age in range(self.initial_age, self.retirement_age):
            self._step()

    def _step(self):
        self.inflation_scenario.step()
        self.deferral_scenario.step()
        self.consumption_scenario.step()
        self.ssb_scenario.step()

        deferral_amt = self.deferral_scenario.value
        withdrawal_amt = self._get_withdrawal()

        self.portfolio.step(deferral_amt=deferral_amt, withdrawal_amt=withdrawal_amt)

    def _get_withdrawal(self):
        return self.consumption_scenario.value - self.ssb_scenario.value