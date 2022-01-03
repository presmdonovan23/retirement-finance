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
        # self.balance = balance

        # self.history = dict({
        #     'balance': np.array([self.balance]),
        #     'allocations': np.array([self.allocations]),
        #     'returns': np.array([]),
        #     'deposits': np.array([]),
        #     'withdrawals': np.array([])
        # })

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
            #print('before grow: ', self.value)
            pf_return, asset_returns = self._grow()
            value *= (1 + pf_return)
            #print('after grow', self.value)
            next_allocations = self.glidepath[self.period]
            self._update_asset_allocation(allocations=next_allocations)

        return value

    # def get_total_return(self, period=None):
    #     if period is None:
    #         period = self.period
    #
    #     returns = np.array([asset.history[period - 1] for asset in self.assets])
    #     total_return = (returns * self.glidepath[period-1]).sum()
    #
    #     return total_return

    # def get_historical_returns(self):
    #     historical_returns = np.array([None for _ in range(self.period+1)])
    #     for period in range(self.period):
    #         historical_returns[period] = self.get_total_return(period=period)
    #
    #     return historical_returns

    # def _deposit(self, amount):
    #     self.value += amount
    #
    # def _withdraw(self, amount):
    #     if amount > self.value:
    #         raise ValueError('Withdrawal amounts ${0} exceeds balance (${1}).'.format(amount, self.value))
    #
    #     self.value -= amount

    def _grow(self):
        for asset in self.assets:
            asset.step()

        returns = np.array([asset.history[self.period-1] for asset in self.assets])
        total_return = (returns * self.allocations).sum()

        self.total_returns[self.period-1] = total_return
        #total_return = self.get_total_return(period=self.period)

        #self.value *= (1 + total_return)

        return total_return, returns

    def _update_asset_allocation(self, allocations):
        if len(allocations) != len(self.allocations):
            raise ValueError('Invalid number of asset allocations ({0} passed, {1} required).'.format(len(allocations),
                                                                                                      len(self.allocations)))

        if abs(sum(allocations) - 1) > (10 ** -8):
            raise ValueError('Asset allocations must sum to 1 (sum currently {0}).'.format(sum(allocations)))

        self.allocations = np.array(allocations)
