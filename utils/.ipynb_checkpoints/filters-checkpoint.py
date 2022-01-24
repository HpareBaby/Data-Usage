import pandas as pd

class ProgramFilter:

    @staticmethod
    def is_foc(dataframe, status):
        _df = dataframe.copy()
        _searchfor = '^FOC.*$'
        if status is True:
            result = _df[_df['program'].str.contains(_searchfor, regex=True)]
        else:
            result = _df[~_df['program'].str.contains(_searchfor, regex=True)]
        return result 

    @staticmethod
    def is_mc(dataframe, status):
        _df = dataframe.copy()
        _searchfor = '^MC.*$'
        if status is True:
            result = _df[_df['program'].str.contains(_searchfor, regex=True)]
        else:
            result = _df[~_df['program'].str.contains(_searchfor, regex=True)]
        return result

    @staticmethod
    def is_trial(dataframe, status):
        _df = dataframe.copy()
        if status is True:
            result = _df[_df['program']=='Trial']
        else: 
            result = _df[_df['program']!='Trial']
        return result

    @staticmethod
    def is_extra(dataframe, status):
        _df = dataframe.copy()
        if status is True:
            result = _df[_df['program']=='Extra']
        else:
            result = _df[_df['program']!='Extra']
        return result
    
    def is_internal(dataframe, status):
        _df = dataframe.copy()
        _searchfor = '^Internal.*$'
        if status is True:
            result = _df[_df['program'].str.contains(_searchfor, regex=True)]
        else:
            result = _df[~_df['program'].str.contains(_searchfor, regex=True)]
        return result    

class PSGeneralFilters:

    @staticmethod
    def has_cpe(dataframe, has_id=True):
        _searchfor = '[A-Z]{2,4}\d{6}'
        _df = dataframe.copy()
        _df['cid'].fillna('None',inplace=True)
        if has_id is True:
            result = _df[_df['cid'].str.contains(_searchfor,regex=True)]
        else: 
            result = _df[~_df['cid'].str.contains(_searchfor,regex=True)]
        return result
    
    @staticmethod
    def is_streaming(dataframe, status=True):
        _df = dataframe.copy()
        if status is True:
            result = _df[_df['installation_type']=='Streaming']
        else:
            result = _df[_df['installation_type']!='Streaming']
        return result

    @staticmethod
    def is_service_id_999(dataframe, status=True):
        _df = dataframe.copy()
        _serachfor = '9{3}$'
        if status is True:
            result = _df[_df['service_id'].str.contains(_serachfor, na=False)]
        else:
            result = _df[~_df['service_id'].str.contains(_serachfor, na=False)]
        return result

    @staticmethod
    def active_btd_filter(dataframe, status=True):
        _df = dataframe.copy()
        return _df[~((_df['status']=='active') & (_df['billing_terminate_date'].notna()))]

    @staticmethod
    def is_postpaid(dataframe, status=True):
        _df = dataframe.copy()
        if status is True:
            result = _df[_df['plan']=='Postpaid']
        else:
            result = _df[_df['plan']!='Postpaid']
        return result