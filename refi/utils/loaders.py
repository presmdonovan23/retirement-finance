import refi.utils.constants as constants
import refi.series.base_series as base_series
from refi.series.consumption import StaticRetirementConsumption
from refi.series.ssb import StaticRetirementSSB
from refi.series.deferral import StaticPreRetirementDeferral


def load_asset_series(num_years, pctile):
    equity_return = constants.equity_return_dist[pctile]
    bond_return = constants.bond_return_dist[pctile]
    cash_return = constants.cash_return_dist[pctile]

    equity = base_series.StaticSeries(num_years, equity_return)
    bond = base_series.StaticSeries(num_years, bond_return)
    cash = base_series.StaticSeries(num_years, cash_return)

    return equity, bond, cash


def load_inflation_series(num_years, initial_cpi):
    inflation_rate = constants.geo_mean_inflation_rate
    inflation = base_series.StaticSeries(num_years, inflation_rate)
    cpi = base_series.StaticGrowthSeries(initial_value=initial_cpi, growth_series=inflation)

    return inflation, cpi


def load_behavioral_series(initial_deferral, retirement_consumption, benefits_age, retirement_ssb, cpi, initial_age, retirement_age):
    deferral = StaticPreRetirementDeferral(initial_deferral, cpi, initial_age, retirement_age)
    consumption = StaticRetirementConsumption(retirement_consumption, cpi, initial_age, retirement_age)
    ssb = StaticRetirementSSB(retirement_ssb, cpi, initial_age, benefits_age)

    return deferral, consumption, ssb
