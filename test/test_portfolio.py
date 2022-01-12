import unittest

import refi.series.base_series as s
import refi.portfolio as pf
import refi.utils.constants


# to run: python -m unittest test.test_portfolio
class PortfolioTest(unittest.TestCase):
    geo_mean_equity_return = .065
    geo_mean_bond_return = .035
    geo_mean_cash_return = .002
    initial_balance = 100000
    glidepath = refi.utils.constants.fidelity_glidepath

    def get_sample_portfolio(self):
        num_periods = 60

        equity = s.StaticSeries(num_periods, self.geo_mean_equity_return)
        bond = s.StaticSeries(num_periods, self.geo_mean_bond_return)
        cash = s.StaticSeries(num_periods, self.geo_mean_cash_return)

        assets = [equity, bond, cash]
        balance = self.initial_balance

        glidepath = self.glidepath
        portfolio = pf.Portfolio(assets, glidepath, balance)

        return portfolio

    def test_init(self):
        portfolio = self.get_sample_portfolio()
        portfolio.step()

        self.assertEqual(portfolio.value, self.initial_balance)
        self.assertListEqual(list(portfolio.allocations), list(self.glidepath[0]))
        self.assertEqual(len(portfolio.assets), 3)

    def test_withdraw(self):
        pass

    def test_step(self):
        portfolio = self.get_sample_portfolio()
        portfolio.step()

        deposit_amt_1 = 1500.5
        return_1 = portfolio.glidepath[0][0] * self.geo_mean_equity_return \
            + portfolio.glidepath[0][1] * self.geo_mean_bond_return \
            + portfolio.glidepath[0][2] * self.geo_mean_cash_return
        portfolio.step(deposit_amt=deposit_amt_1)
        expected_balance_1 = (self.initial_balance + deposit_amt_1) * (1 + return_1)
        self.assertEqual(portfolio.value, expected_balance_1)

        withdrawal_amt_2 = 10000
        return_2 = portfolio.glidepath[1][0] * self.geo_mean_equity_return \
            + portfolio.glidepath[1][1] * self.geo_mean_bond_return \
            + portfolio.glidepath[1][2] * self.geo_mean_cash_return
        portfolio.step(withdrawal_amt=withdrawal_amt_2)
        expected_balance_2 = (portfolio.history[1] - withdrawal_amt_2) * (1 + return_2)
        self.assertEqual(portfolio.value, expected_balance_2)

        n_steps = 40
        for _ in range(n_steps):
            portfolio.step()

        cur_bal = portfolio.value
        withdrawal_amt_3 = 50000
        return_3 = portfolio.glidepath[2+n_steps][0] * self.geo_mean_equity_return \
            + portfolio.glidepath[2+n_steps][1] * self.geo_mean_bond_return \
            + portfolio.glidepath[2+n_steps][2] * self.geo_mean_cash_return
        portfolio.step(withdrawal_amt=withdrawal_amt_3)
        expected_balance_3 = (cur_bal - withdrawal_amt_3) * (1 + return_3)

        self.assertEqual(portfolio.value, expected_balance_3)


if __name__ == '__main__':
    unittest.main()
