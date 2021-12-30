import unittest
import numpy as np

import refi.series.base_series as base_series
from refi.series.consumption import StaticRetirementConsumption
from refi.series.deferral import StaticPreRetirementDeferral


class SeriesTest(unittest.TestCase):

    def test_PositiveGaussian_and_StaticGrowth(self):
        num_years = 50
        mean_inflation = .02
        std_dev_inflation = .005
        inflation_scenario = base_series.PositiveGaussianSeries(num_years, mean=mean_inflation, std_dev=std_dev_inflation)
        consumption_scenario = base_series.StaticGrowthSeries(initial_value=10000, growth_series=inflation_scenario)

        inflation_scenario.step()
        self.assertGreaterEqual(inflation_scenario.history[0], inflation_scenario.min_possible_return)
        self.assertTrue(np.isnan(inflation_scenario.history[1]))
        self.assertEqual(len(consumption_scenario.history), len(inflation_scenario.history))

        inflation_scenario.step()
        consumption_scenario.step()
        self.assertEqual(consumption_scenario.history[0], consumption_scenario.initial_value)

        consumption_scenario.step()
        self.assertEqual(consumption_scenario.history[1], consumption_scenario.history[0] * (1 + inflation_scenario.history[0]))

        consumption_scenario.step()
        try:
            e = None
            consumption_scenario.step()
        except BaseException as err:
            e = err
        self.assertEqual(type(e), RuntimeError)
        self.assertEqual(consumption_scenario.period, 2)

        while inflation_scenario.period < (inflation_scenario.num_periods - 1):
            inflation_scenario.step()

        while consumption_scenario.period < (consumption_scenario.num_periods - 1):
            consumption_scenario.step()

        self.assertTrue(all(~np.isnan(inflation_scenario.history)))
        self.assertTrue(all(~np.isnan(consumption_scenario.history)))

    def test_StaticRetirementConsumption_and_StaticPreRetirementDeferral(self):

        retirement_consumption = 75000
        initial_deferral = 19500
        initial_cpi = 100
        initial_age = 30
        retirement_age = 65
        retirement_period = retirement_age - initial_age
        num_years = 90 - initial_age + 1

        mean_inflation = .02
        std_dev_inflation = .005

        inflation = base_series.PositiveGaussianSeries(num_years, mean=mean_inflation, std_dev=std_dev_inflation)
        cpi = base_series.StaticGrowthSeries(initial_value=initial_cpi, growth_series=inflation)

        inflation.step_all()
        cpi.step_all()

        consumption = StaticRetirementConsumption(retirement_consumption, cpi, initial_age, retirement_age)
        deferral = StaticPreRetirementDeferral(initial_deferral, cpi, initial_age, retirement_age)

        consumption.step_all()
        deferral.step_all()

        self.assertAlmostEqual(cpi.history[retirement_period-1] / initial_cpi, deferral.history[retirement_period-1] / initial_deferral)
        self.assertAlmostEqual(cpi.history[retirement_period] / initial_cpi, consumption.history[retirement_period] / retirement_consumption)

        self.assertAlmostEqual(1 + inflation.history[5], deferral.history[6] / deferral.history[5])

        self.assertFalse(any((deferral.history > 0) & (consumption.history > 0)), 'Some periods have non-zero deferral and consumption.')


if __name__ == '__main__':
    unittest.main()
