import numpy as np


class Portfolio:

    def __init__(self, assets, glidepath, balance):
        self.assets = np.array(assets)
        self.glidepath = glidepath
        self._t = 0
        self.allocations = np.array(self.glidepath[self._t])
        self.balance = balance

        self.hist_balance = np.array([self.balance])
        self.hist_allocations = np.array([self.allocations])
        self.hist_pf_returns = np.array([])
        self.hist_asset_returns = np.array([])
        self.hist_deposits = np.array([])
        self.hist_withdrawals = np.array([])

    def step(self, deposit_amt=0, withdrawal_amt=0):

        if withdrawal_amt > (self.balance + deposit_amt):
            raise ValueError(
                'Withdrawal amounts ${0} exceeds balance (${1}).'.format(withdrawal_amt, self.balance + deposit_amt))

        self._deposit(amount=deposit_amt)
        self._withdraw(amount=withdrawal_amt)
        pf_return, asset_returns = self._grow()

        next_allocations = self.glidepath[self._t + 1]
        self._update_asset_allocation(allocations=next_allocations)

        self._update_history(deposit_amt, withdrawal_amt, pf_return, asset_returns)

        self._t += 1

    def print_history(self):
        print('Historical balance:')
        print(self.hist_balance)
        print('Historical returns:')
        print(self.hist_pf_returns)
        print('Historical deposits:')
        print(self.hist_deposits)
        print('Historical withdrawals:')
        print(self.hist_withdrawals)

    def _update_history(self, deposit_amt, withdrawal_amt, pf_return, asset_returns):
        self.hist_balance = np.append(self.hist_balance, self.balance)
        self.hist_allocations = np.append(self.hist_allocations, self.allocations)
        self.hist_pf_returns = np.append(self.hist_pf_returns, pf_return)
        self.hist_asset_returns = np.append(self.hist_asset_returns, asset_returns)
        self.hist_deposits = np.append(self.hist_deposits, deposit_amt)
        self.hist_withdrawals = np.append(self.hist_withdrawals, withdrawal_amt)

    def _deposit(self, amount):
        self.balance += amount

    def _withdraw(self, amount):
        if amount > self.balance:
            raise ValueError('Withdrawal amounts ${0} exceeds balance (${1}).'.format(amount, self.balance))

        self.balance -= amount

    def _grow(self):
        for asset in self.assets:
            asset.step()

        returns = np.array([asset.value for asset in self.assets])
        total_return = (returns * self.allocations).sum()
        self.balance *= (1 + total_return)

        return total_return, returns

    def _update_asset_allocation(self, allocations):
        if len(allocations) != len(self.allocations):
            raise ValueError('Invalid number of asset allocations ({0} passed, {1} required).'.format(len(allocations),
                                                                                                      len(self.allocations)))

        if abs(sum(allocations) - 1) > (10 ** -8):
            raise ValueError('Asset allocations must sum to 1 (sum currently {0}).'.format(sum(allocations)))

        self.allocations = np.array(allocations)
