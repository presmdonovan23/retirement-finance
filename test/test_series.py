import unittest
import numpy as np

from refi import series


class SeriesTest(unittest.TestCase):
    def test_PositiveGaussian_and_StaticGrowth(self):
        num_years = 50
        mean_inflation = .02
        std_dev_inflation = .005
        inflation_scenario = series.PositiveGaussianSeries(num_years, mean=mean_inflation, std_dev=std_dev_inflation)
        consumption_scenario = series.StaticGrowthSeries(initial_value=10000, growth_series=inflation_scenario)

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


if __name__ == '__main__':
    unittest.main()
