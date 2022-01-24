import pendulum
from datetime import datetime as dt


class DateDefinitions:

    @classmethod
    def _cnst_lmo(cls):
        today = pendulum.today()
        lmo = today.subtract(days=today.day)
        return lmo

    @classmethod
    def start_mo(cls):
        lyr = cls._cnst_lmo().year
        return dt.strftime(dt(lyr, 1, 1), '%Y-%m-%d')

    @classmethod
    def last_mo(cls):
        return dt.strftime(cls._cnst_lmo(), '%Y-%m-%d')

    @classmethod
    def last_12months(cls):
        lmo = cls._cnst_lmo()
        last_12mos = lmo.subtract(months=11)
        l12_yr = last_12mos.year
        l12_mon = last_12mos.month
        start_date = dt(l12_yr, l12_mon, 1)
        end_date = dt(lmo.year, lmo.month, lmo.day)
        return (dt.strftime(start_date, '%Y-%m-%d'), dt.strftime(end_date, '%Y-%m-%d'))

    @classmethod
    def final_calculated_mo(cls):
        return dt.strftime(cls._cnst_lmo(), '%Y-%m')

    @classmethod
    def yearly_end_date(cls):
        lyr = cls._cnst_lmo().year
        return dt.strftime(dt(lyr, 12, 31), '%Y-%m-%d')
    
    @classmethod
    def paid_date_cutoff(cls):
        lyr = cls._cnst_lmo().year
        cutoff_yr = int(lyr) - 1
        return dt.strftime(dt(cutoff_yr, 12, 31), '%Y-%m-%d')