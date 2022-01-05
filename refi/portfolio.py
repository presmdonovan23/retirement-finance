import numpy as np

from refi.series.base_series import BaseSeries


class Portfolio(BaseSeries):

    def __init__(self, assets, glidepath, initial_balance):
        num_periods = len(glidepath)
        super().__init__(num_periods)

        self.initial_balance = initial_balance
        self.assets = np.array(assets)
        self.glidepath = glidepath
        # self._t = 0
        self.allocations = np.array(self.glidepath[0])
        self.total_returns = np.array([np.nan for _ in range(self.num_periods)])

    def get_next_value(self, deposit_amt=0, withdrawal_amt=0):

        if self.period == 0:
            value = self.initial_balance
        else:
            if withdrawal_amt > (self.value + deposit_amt):
                raise ValueError(
                    'Withdrawal amounts ${0} exceeds balance (${1}).'.format(withdrawal_amt, self.value + deposit_amt))

            value = self.value
            value += deposit_amt

            if withdrawal_amt > value:
                raise ValueError('Withdrawal amounts ${0} exceeds balance (${1}).'.format(withdrawal_amt, self.value))

            value -= withdrawal_amt

            pf_return, asset_returns = self._grow()
            value *= (1 + pf_return)

            next_allocations = self.glidepath[self.period]
            self._update_asset_allocation(allocations=next_allocations)

        return value

    def _grow(self):
        for asset in self.assets:
            asset.step()

        returns = np.array([asset.history[self.period-1] for asset in self.assets])
        total_return = (returns * self.allocations).sum()

        self.total_returns[self.period-1] = total_return

        return total_return, returns

    def _update_asset_allocation(self, allocations):
        if len(allocations) != len(self.allocations):
            raise ValueError('Invalid number of asset allocations ({0} passed, {1} required).'.format(len(allocations),
                                                                                                      len(self.allocations)))

        if abs(sum(allocations) - 1) > (10 ** -8):
            raise ValueError('Asset allocations must sum to 1 (sum currently {0}).'.format(sum(allocations)))

        self.allocations = np.array(allocations)
