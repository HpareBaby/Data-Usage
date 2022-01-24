import os
import sys
import calendar
import pandas as pd 
import numpy as np
from scipy import stats
from jinja2 import Template
from datetime import datetime as dt

# Custom modules
abs_path = os.path.dirname(os.path.realpath(__file__))
wk_path = os.path.normpath(abs_path + os.sep + os.pardir + os.sep + os.pardir)
sys.path.append(wk_path)

from utils.file_helper import FileHandler
from utils.database_connector import DBConn
from utils.query_template import QTemplate
from utils.cutoff_date import DateDefinitions
from helper.columns import ColumnName

conn = DBConn()
qtemplate = QTemplate()
file_handler = FileHandler()

def data_usage_df(year):
    column_names = ["record_year", "record_month", "customer_id", "total_mb"]
    yr =year
    query = Template(qtemplate.DataUsage()).render(this_year=yr)
    data = conn.query_to_postgresql(query)
    monthly_data_usage = pd.DataFrame(data, columns=column_names)
    return monthly_data_usage

def data_usage_year_list():
    last_date = DateDefinitions.last_mo()
    lyr = int(last_date[:4])
    yr_list = np.arange(2020, lyr+1, 1)
    return yr_list

def avg_data_usage_calc(dataframe, year):
    """
    calculate the all data usage in one year 
    Note data usage is very little data, so this code is embedded here
    """
    _df = dataframe.copy()
    df_mo = _df.groupby(by='customer_id')['record_month'].apply(np.unique).reset_index()
    df_usage = _df.groupby(by='customer_id')['total_mb'].sum().reset_index()
    df_m = pd.merge(df_mo, df_usage, on='customer_id')
    df_m['month_count'] = df_m['record_month'].apply(lambda x : len(x))
    cols_name = '_'.join(['avg', str(year)])
    df_m[cols_name] = df_m['total_mb']/df_m['month_count']
    df_m.drop(['record_month', 'total_mb', 'month_count'],axis=1, inplace=True)
    return df_m

def is_one_yr(yr):
    _yr = yr
    df_init = data_usage_df(_yr)
    df_i = avg_data_usage_calc(df_init, _yr)
    return df_i

def is_two_yr(yr_list):
    _yr1 = yr_list[0]
    _yr2 = yr_list[1]
    df_yr1 = data_usage_df(_yr1)
    df_yr2 = data_usage_df(_yr2)
    df_1 = avg_data_usage_calc(df_yr1, _yr1)
    df_2 = avg_data_usage_calc(df_yr2, _yr2)
    df_m = pd.merge(df_1, df_2, on='customer_id', how='outer')
    return df_m

def is_more_two_yr(yr_list):
    _yr1 = yr_list[0]
    _yr2 = yr_list[1]
    df_mo1 = data_usage_df(_yr1)
    df_mo2 = data_usage_df(_yr2)
    df_1 = avg_data_usage_calc(df_mo1, _yr1)
    df_2 = avg_data_usage_calc(df_mo2, _yr2)
    df_m = pd.merge(df_1, df_2, on='customer_id', how='outer')
    for i in yr_list[2:]:
        _yr_n = i
        df_u = data_usage_df(_yr_n)
        df_n = avg_data_usage_calc(df_u, _yr_n)
        df_m = pd.merge(df_m, df_n, on='customer_id', how='outer')
    return df_m

# transform the data based on the year [mx2]
def yearly_avg_data_usage():
    yr_list = data_usage_year_list()
    yr_list_m = yr_list[:-1]
    if len(yr_list_m) == 1:
        _yr = yr_list[0]
        df_avg = is_one_yr(_yr)
    if len(yr_list_m) == 2:
        _yrl = yr_list
        df_avg = is_two_yr(_yrl)
    if len(yr_list_m) > 2:
        _yrl = yr_list
        df_avg = is_more_two_yr(_yrl)
    return df_avg

# transfrom the latest year data to columns [mxn]
def transformation():
    selected_cols = ['customer_id', 'total_mb']
    yr_list = data_usage_year_list()
    current_year = yr_list[-1]
    df = data_usage_df(current_year)
    mos_list = np.unique(df['record_month'].to_list())
    _mo_1 = "-".join([str(current_year),str(mos_list[0]),'mb'])
    _mo_2 = "-".join([str(current_year),str(mos_list[1]),'mb'])
    df_1 = df.loc[df['record_month'] == mos_list[0]][selected_cols]
    df_1.rename({'total_mb': _mo_1}, axis=1, inplace=True)
    df_2 = df.loc[df['record_month'] == mos_list[1]][selected_cols]
    df_2.rename({'total_mb': _mo_2}, axis=1, inplace=True)
    df_m = pd.merge(df_1, df_2, on='customer_id', how='outer')
    for i in mos_list[2:]:
        cols_name = "-".join([str(current_year),str(i),'mb'])
        df_n = df.loc[df['record_month'] == i][selected_cols]
        df_n.rename({'total_mb': cols_name}, axis=1, inplace=True)
        df_m = pd.merge(df_m, df_n, on='customer_id', how='outer')
    return df_m


def main():
    # merge previous average data usage and newly data usaget [mxn]
    df_avg = yearly_avg_data_usage()
    df_m = transformation()
    df_merged_all = pd.merge(df_avg, df_m, on='customer_id', how='outer')
    df_merged_cal = df_merged_all.copy()

    # calculate the whole average data usage [convert argumented matrix]
    col_names = df_merged_cal.columns
    df_merged_cal['total_months'] = df_merged_cal.fillna(0).astype(bool).sum(axis=1)
    df_merged_cal['total_months'] = df_merged_cal['total_months'] - 1
    df_merged_cal.loc[:, 'total_usage'] = df_merged_cal.loc[:, col_names[1:]].sum(axis=1)
    df_merged_cal['avg_usage'] = df_merged_cal['total_usage']/df_merged_cal['total_months']
    df_merged_cal['avg_usage'] = df_merged_cal['avg_usage'].apply(lambda x : '{:.1e}'.format(x))

    # groups information
    grouping_data_file = 'grouping_ids'
    groups_ids = file_handler.csv_reader('grouping_ids', 'interim', 'grouping_ids')

    df_merged_groups = pd.merge(groups_ids, df_merged_cal, on='customer_id', how='right')

    # add create date and months
    df_merged_groups['final_calculated_month'] = DateDefinitions.final_calculated_mo()
    df_merged_groups['write_date'] = dt.now()

    file_handler.saved_as_csv(df_merged_groups, 'data_usage', 'predictors', 'data_usage')

if __name__ == '__main__':
    main()