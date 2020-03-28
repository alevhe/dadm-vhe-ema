import pandas as pd
import numpy as np

def _add_columns(df, columns):
    dataframe = pd.DataFrame(0, index=df.index, columns=columns)
    df = pd.concat([df, dataframe], axis=1)
    return df

def _data_encode(df, column_name):
    zip_ohe = pd.get_dummies(df[column_name], prefix=column_name)
    df = df.drop(column_name, axis=1)
    df = pd.concat([df, zip_ohe], axis=1)
    return df

# missing completely at random
def _average_and_encode(df, column_name):
    #replacement = {None: "NA"}
    #df[column_name] = df[column_name].replace(to_replace=replacement)
    return _data_encode(df, column_name)

#set 0 because they are values
def _value_and_encode(df, column_name):
    replacement = {None: "NA"}
    df[column_name] = df[column_name].replace(to_replace=replacement)
    return _data_encode(df, column_name)


#set 0 because they are values
def _garage_and_encode(df, columns_to_check):
    list_index = list()
    for column_id in range(len(columns_to_check)):
        data_to_check = df[columns_to_check[column_id]]
        list_index.append([x for x in data_to_check.index if str(data_to_check[x]) == "nan"])
    total_list = list()
    if len(list_index) > 0:
        for col in list_index[0]:
            found = False
            for row in list_index:
                if col not in row:
                    found = True
            if not found:
                total_list.append(col)
    total_list_or = list()
    if len(list_index) > 0:
        for col in list_index:
            for r in col:
                if r not in total_list_or:
                    total_list_or.append(r)
    lines_to_modify = [x for x in total_list_or if x in total_list]

    for c in columns_to_check:
        df[c][lines_to_modify] = "Na"
        df = _data_encode(df, c)
    return df

def _condition_and_encode(df, column_name, columns_to_check):
    list_index = list()
    for column_id in range(len(columns_to_check)):
        data_to_check = df[columns_to_check[column_id]]
        list_index.append([x for x in data_to_check.index if str(data_to_check[x]) == "nan"])
    total_list = list()
    if len(list_index) > 0:
        for col in list_index[0]:
            found = False
            for row in list_index:
                if col not in row:
                    found = True
            if not found:
                total_list.append(col)

    lines_to_set_mean = [x for x in df[column_name].index if str(df.iloc[x][column_name]) == 'nan' and x in total_list]
    lines_to_set_zero = [x for x in df[column_name].index if str(df.iloc[x][column_name]) == 'nan' and x not in lines_to_set_mean]

    if len(lines_to_set_mean) > 0:
        sum_list = [x for x in df[column_name] if str(x) != 'nan']
        df[column_name][lines_to_set_mean] = sum(sum_list) / len(sum_list)
        if column_name == 'BsmtFinSF1' or column_name == 'BsmtFinSF2':
            tl = [x for x in total_list if x not in lines_to_set_mean]
            df[columns_to_check[0]][tl] = "NA"
    if len(lines_to_set_zero) > 0:
        df[column_name][lines_to_set_zero] = 0
    return df

def _masvnr_and_encode(df):
    column_name = "MasVnrArea"
    data_to_check = df["MasVnrType"]
    total_list = [x for x in data_to_check.index if data_to_check[x] == "None"]

    lines_to_set_mean = [x for x in df[column_name].index if str(df.iloc[x][column_name]) == 'nan' and x not in total_list]
    lines_to_set_zero = [x for x in df[column_name].index if str(df.iloc[x][column_name]) == 'nan' and x not in lines_to_set_mean]

    if len(lines_to_set_mean) > 0:
        sum_list = [x for x in df[column_name] if str(x) != 'nan']
        df[column_name][lines_to_set_mean] = sum(sum_list) / len(sum_list)
    if len(lines_to_set_zero) > 0:
        df[column_name][lines_to_set_zero] = 0
    return df


def _condition_or_encode(df, column_name, columns_to_check, values_to_check):
    list_index = list()
    for column_id in range(len(columns_to_check)):
        data_to_check = df[columns_to_check[column_id]]
        list_index.append([x for x in data_to_check.index if str(data_to_check[x]) == values_to_check[column_id]])
    total_list = list()
    if len(list_index) > 0:
        for col in list_index:
            for r in col:
                if r not in total_list:
                    total_list.append(r)
    #TODO check all the combination of presence
    #TODO check the mean of the percentage of unfinished

    lines_to_set_zero = [x for x in df[column_name].index if str(df.iloc[x][column_name]) == 'nan' and x not in total_list]
    lines_to_set_mean = [x for x in df[column_name].index if str(df.iloc[x][column_name]) == 'nan' and x not in lines_to_set_zero]

    if len(lines_to_set_zero) > 0:
        df[column_name][lines_to_set_zero]= 0
    if len(lines_to_set_mean) > 0:
        sum_list = [x for x in df[column_name] if str(x) != 'nan']
        df[column_name][lines_to_set_mean] = sum(sum_list) / len(sum_list)
    return df

def _condition_or_encode_bsmt(df, column_name, columns_to_check, values_to_check):
    list_index = list()
    for column_id in range(len(columns_to_check)):
        data_to_check = df[columns_to_check[column_id]]
        list_index.append([x for x in data_to_check.index if
                       str(data_to_check[x]) == values_to_check[column_id] or str(data_to_check[x]) == "nan"])
    total_list = list()
    if len(list_index) > 0:
        for col in list_index:
            for r in col:
                if r not in total_list:
                    total_list.append(r)
    #TODO check all the combination of presence
    #TODO check the mean of the percentage of unfinished

    lines_to_set_zero = [x for x in df[column_name].index if str(df.iloc[x][column_name]) == 'nan' and x not in total_list]
    lines_to_set_mean = [x for x in df[column_name].index if str(df.iloc[x][column_name]) == 'nan' and x not in lines_to_set_zero]

    if len(lines_to_set_zero) > 0:
        df[column_name][lines_to_set_zero]= 0
    if len(lines_to_set_mean) > 0:
        sum_list = [x for x in df[column_name] if str(x) != 'nan']
        df[column_name][lines_to_set_mean] = sum(sum_list) / len(sum_list)
    return df

def _min_and_encode(df, column_name, columns_to_check):
    list_index = list()
    for column_id in range(len(columns_to_check)):
        data_to_check = df[columns_to_check[column_id]]
        list_index.append([x for x in data_to_check.index if str(data_to_check[x]) == "nan"])
    total_list = list()
    if len(list_index) > 0:
        for col in list_index:
            for r in col:
                if r not in total_list:
                    total_list.append(r)
    lines_to_set_mean = [x for x in df[column_name].index if str(df.iloc[x][column_name]) == 'nan' and x  in total_list]
    lines_to_set_min = [x for x in df[column_name].index if str(df.iloc[x][column_name]) == 'nan' and x not in lines_to_set_mean]
    if len(lines_to_set_mean) > 0:
        sum_list = [x for x in df[column_name] if str(x) != 'nan']
        df[column_name][lines_to_set_mean] = sum(sum_list) / len(sum_list)
    if len(lines_to_set_min) > 0:
        df[column_name][lines_to_set_min] = df[column_name].min()
    return df

def _pool_encode(df, column_name, column_to_check):
    data_to_check = df[column_to_check]
    actual_col = df[column_name]
    list_index = [x for x in data_to_check.index if data_to_check[x] == 0 and str(actual_col[x]) == "nan"]
    df[column_name][list_index] = "NA"
    return _average_and_encode(df, column_name)

def _kitchen_encode(df, column_name, column_to_check):
    data_to_check = df[column_to_check]
    actual_col = df[column_name]
    list_index = [x for x in data_to_check.index if data_to_check[x] == 0 and str(actual_col[x]) == "nan"]
    df[column_name][list_index] = "NA"
    return _average_and_encode(df, column_name)

def _read_file(filename):
    df = pd.read_csv(filename)
    df = df.drop('Id', axis=1)

    # if second field none => 0 otherwise mean
    df = _masvnr_and_encode(df)
    df = _condition_and_encode(df, 'BsmtFinSF1', ['BsmtFinType1'])
    df = _condition_and_encode(df, 'BsmtFinSF2', ['BsmtFinType2'])
    df = _condition_and_encode(df, 'TotalBsmtSF', ['BsmtFinType1','BsmtFinType2'])
    df = _condition_and_encode(df, 'BsmtFullBath', ['BsmtFinType1', 'BsmtFinType2'])
    df = _condition_and_encode(df, 'BsmtHalfBath', ['BsmtFinType1', 'BsmtFinType2'])


    df = _condition_or_encode(df, 'GarageCars', ['GarageType', 'GarageCond', 'GarageQual'], ['nan', 'nan', 'nan'])
    df = _condition_or_encode(df, 'GarageArea', ['GarageType', 'GarageCond', 'GarageQual'], ['nan', 'nan', 'nan'])

    df = _condition_or_encode_bsmt(df, 'BsmtUnfSF', ['BsmtFinType1', 'BsmtFinType2'], ['Unf', 'Unf'])

    df = _min_and_encode(df, 'GarageYrBlt', ['GarageType', 'GarageCond', 'GarageQual'])


    # the following fields were the following of which we took the mean
    df = _average_and_encode(df, 'SaleType')
    df = _average_and_encode(df, 'ExterCond')
    df = _average_and_encode(df, 'ExterQual')
    df = _average_and_encode(df, 'MasVnrType')
    df = _average_and_encode(df, 'Exterior1st')
    df = _average_and_encode(df, 'Exterior2nd')
    df = _average_and_encode(df, 'Utilities')
    df = _average_and_encode(df, 'MSZoning')
    df = _average_and_encode(df, 'Functional')
    df = _kitchen_encode(df, 'KitchenQual', 'KitchenAbvGr')
    df = _average_and_encode(df, 'Electrical')
    df = _average_and_encode(df, 'BsmtFinType1')
    df = _average_and_encode(df, 'BsmtFinType2')

    # the following fields maintain the nan as zero
    df = _value_and_encode(df, 'Alley')
    df = _value_and_encode(df, 'FireplaceQu')
    df = _value_and_encode(df, 'MiscFeature')
    df = _value_and_encode(df, 'BsmtQual')
    df = _value_and_encode(df, 'BsmtCond')
    df = _value_and_encode(df, 'BsmtExposure')
    df = _value_and_encode(df, 'Fence')
    df = _garage_and_encode(df, ['GarageType', 'GarageCond', 'GarageQual', 'GarageFinish'])

    #the following fields doon't expect to see nan
    df = _data_encode(df, 'MSSubClass')
    df = _data_encode(df, 'OverallQual')
    df = _data_encode(df, 'OverallCond')
    df = _data_encode(df, 'SaleCondition')
    df = _data_encode(df, 'Heating')
    df = _data_encode(df, 'HeatingQC')
    df = _data_encode(df, 'Foundation')
    df = _data_encode(df, 'PavedDrive')
    df = _data_encode(df, 'LotShape')
    df = _data_encode(df, 'LandContour')
    df = _data_encode(df, 'LotConfig')
    df = _data_encode(df, 'LandSlope')
    df = _data_encode(df, 'Neighborhood')
    df = _data_encode(df, 'Condition1')
    df = _data_encode(df, 'Condition2')
    df = _data_encode(df, 'BldgType')
    df = _data_encode(df, 'HouseStyle')
    df = _data_encode(df, 'RoofStyle')
    df = _data_encode(df, 'RoofMatl')

    df = _pool_encode(df, 'PoolQC', 'PoolArea')

    #se non c'è vuol dire che è 0 giusto?
    LotFrontage = {None: 0}
    df['LotFrontage'] = df['LotFrontage'].replace(to_replace=LotFrontage)

    df = _data_encode(df, 'CentralAir')
    df = _data_encode(df, 'Street')
    return df