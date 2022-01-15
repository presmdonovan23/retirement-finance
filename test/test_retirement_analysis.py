import unittest

import refi.utils.constants
import refi.utils.loaders
import refi.retirement_simulation as rs


# to run: python -m unittest test.test_portfolio
class RetirementSimTest(unittest.TestCase):
    initial_balance = 400000

    initial_age = 30
    initial_deferral = 55000
    retirement_age = 60
    retirement_consumption = 100000

    initial_cpi = 275
    retirement_ssb = 10000
    benefits_age = 67
    death_age = 100

    asset_return_pctile = 25

    glidepath = refi.utils.constants.fidelity_glidepath

    def get_sample_ret_sim(self):
        portfolio, deferral, consumption, inflation, cpi, ssb = refi.utils.loaders.load_ret_sim_inputs(
            self.initial_age,
            self.retirement_age,
            self.death_age,
            self.benefits_age,
            self.asset_return_pctile,
            self.initial_cpi,
            self.initial_deferral,
            self.initial_balance,
            self.retirement_consumption,
            self.retirement_ssb,
            self.glidepath
        )

        ret_sim = rs.RetirementSimulation(
            initial_age=self.initial_age,
            retirement_age=self.retirement_age,
            death_age=self.death_age,
            portfolio=portfolio,
            deferral_scenario=deferral,
            consumption_scenario=consumption,
            inflation_scenario=inflation,
            cpi_scenario=cpi,
            ssb_scenario=ssb)

        return ret_sim

    def test_init(self):
        ret_sim = self.get_sample_ret_sim()
        self.assertEqual(ret_sim.initial_age, self.initial_age)
        return ret_sim

    def test_initial_period(self):
        ret_sim = self.get_sample_ret_sim()
        ret_sim.simulate()

        ind = 0
        self.assertEqual(ret_sim.portfolio.history[ind], self.initial_balance)
        self.assertEqual(ret_sim.target_consumption_scenario.history[ind], 0)
        self.assertEqual(ret_sim.deferral_scenario.history[ind], self.initial_deferral)

    def test_second_period(self):
        ret_sim = self.get_sample_ret_sim()
        ret_sim.simulate()

        inflation_rate = refi.utils.constants.geo_mean_inflation_rate

        ind = 1
        pf_ret = ret_sim.portfolio.total_returns[0]
        expected_balance = (self.initial_balance + self.initial_deferral) * (1 + pf_ret)
        expected_consumption = 0
        expected_deferral = self.initial_deferral * (1 + inflation_rate)
        self.assertEqual(ret_sim.portfolio.history[ind], expected_balance)
        self.assertEqual(ret_sim.target_consumption_scenario.history[ind], expected_consumption)
        self.assertEqual(ret_sim.deferral_scenario.history[ind], expected_deferral)

    def test_ret10_balance(self):
        ret_sim = self.get_sample_ret_sim()
        ret_sim.simulate()

        ind = ret_sim.ind_at_ret + 10

        cons = ret_sim.target_consumption_scenario.history[ind]
        ssb = ret_sim.ssb_scenario.history[ind]
        withdrawal = cons - ssb
        pf_ret = ret_sim.portfolio.total_returns[ind]

        expected_balance = (ret_sim.portfolio.history[ind] - withdrawal) * (1 + pf_ret)
        ind = ret_sim.ind_at_ret + 11
        self.assertEqual(ret_sim.portfolio.history[ind], expected_balance)


if __name__ == '__main__':
    unittest.main()
