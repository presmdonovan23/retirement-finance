import numpy as np


class RetirementAnalysis:
    
    def __init__(self):
        # self.initial_balance = initial_balance
        # self.initial_cpi = initial_cpi
        self.initial_age = initial_age
        self.retirement_age = retirement_age
        self.death_age = death_age

        self.portfolio = portfolio

        self.deferral_scenario = deferral_scenario
        self.consumption_scenario = consumption_scenario
        self.inflation_scenario = inflation_scenario


    def simulate(self):
        
        for age in range(self.initial_age, self.retirement_age):
            deferral_amt = self._get_deferral()
            target_consumption = self._get_target_consumption()
            ssb = self._get_ssb()
            withdrawal_amt = self._get_withdrawal()

            self.portfolio.step(deferral_amt=deferral_amt, withdrawal_amt=withdrawal_amt)

    def _get_target_consumption(self):
        return self.consumption_scenario.tgt_consumption

    def _get_deferral(self):
        return self.deferral_scenario.deferral

    def _get_ssb(self):
        return self.ssb_scenario.ssb

    def _get_withdrawal(self):
        return self.consumption_scenario.value - self.ssb