import pandas as pd

def _read_file(filename):
    df = pd.read_csv(filename)
    df = df.drop('Id', axis=1)

    MSZonind =  {'A': 1, 'C (all)': 2, 'C': 2, 'FV': 3, 'I': 4, 'RH': 5, 'RL': 6, 'RP': 7, 'RM': 8}
    df['MSZoning'] = df['MSZoning'].replace(to_replace=MSZonind)
    sum_list = [x for x in df['MSZoning'] if str(x) != 'nan']
    MSZonind = {None: sum(sum_list)/len(sum_list)}
    df['MSZoning'] = df['MSZoning'].replace(to_replace=MSZonind)

    GarageCars ={None: 0}
    GarageArea = {None: 0}
    GarageQual = {None: 0, 'Po': 1, 'Fa': 2, 'TA': 3, 'Gd': 4, 'Ex': 5}
    df['GarageQual'] = df['GarageQual'].replace(to_replace=GarageQual)
    GarageYrBlt = {None: 0}
    df['GarageYrBlt'] = df['GarageYrBlt'].replace(to_replace=GarageYrBlt)
    GarageCond = {None: 0, 'Po': 1, 'Fa': 2, 'TA': 3, 'Gd': 4, 'Ex': 5}
    df['GarageCond'] = df['GarageCond'].replace(to_replace=GarageCond)
    GarageFinish = {None: 0, 'Unf': 1, 'RFn': 2, 'Fin': 3}
    df['GarageFinish'] = df['GarageFinish'].replace(to_replace=GarageFinish)
    GarageType = {None: 0, 'Detchd': 1, 'CarPort': 2, 'BuiltIn': 3, "Basment": 4, 'Attchd': 5, "2Types": 6}
    df['GarageType'] = df['GarageType'].replace(to_replace=GarageType)
    FireplaceQu = {None: 0, 'Po': 1, 'Fa': 2, 'TA': 3, 'Gd': 4, 'Ex': 5}
    df['FireplaceQu'] = df['FireplaceQu'].replace(to_replace=FireplaceQu)
    Functional = {'Sal': 0, "Sev": 1, 'Maj2': 2, 'Maj1': 3, 'Mod': 4, 'Min2': 5, 'Min1': 6, 'Typ': 7}
    df['Functional'] = df['Functional'].replace(to_replace=Functional)
    KitchenQual = {None: 0, 'Po': 1, 'Fa': 2, 'TA': 3, 'Gd': 4, 'Ex': 5}
    df['KitchenQual'] = df['KitchenQual'].replace(to_replace=KitchenQual)
    Electrical = {'Mix': 0, 'FuseP': 1, 'FuseF': 2, 'FuseA': 3, 'SBrkr': 4}
    df['Electrical'] = df['Electrical'].replace(to_replace=Electrical)
    CentralAir = {'N': 0, 'Y': 1}
    df['CentralAir'] = df['CentralAir'].replace(to_replace=CentralAir)
    HeatingQC = {None: 0, 'Po': 1, 'Fa': 2, 'TA': 3, 'Gd': 4, 'Ex': 5}
    df['HeatingQC'] = df['HeatingQC'].replace(to_replace=HeatingQC)
    Heating = {'Floor': 0, 'GasA': 1, 'GasW': 2, 'Grav': 3, 'OthW': 4, 'Wall': 5}
    df['Heating'] = df['Heating'].replace(to_replace=Heating)
    BsmtFinType2 = {None: 0, 'Unf': 1, 'LwQ': 2, "Rec": 3, 'BLQ': 4, 'ALQ': 5, 'GLQ': 6}
    df['BsmtFinType2'] = df['BsmtFinType2'].replace(to_replace=BsmtFinType2)
    BsmtFinType1 = {None: 0, 'Unf': 1, 'LwQ': 2, "Rec": 3, 'BLQ': 4, 'ALQ': 5, 'GLQ': 6}
    df['BsmtFinType1'] = df['BsmtFinType1'].replace(to_replace=BsmtFinType1)
    BsmtExposure = {None: 0, 'No': 1, 'Mn': 2, 'Av': 3, 'Gd': 4}
    df['BsmtExposure'] = df['BsmtExposure'].replace(to_replace=BsmtExposure)
    BsmtCond = {None: 0, 'Po': 1, 'Fa': 2, 'TA': 3, 'Gd': 4, 'Ex': 5}
    df['BsmtCond'] = df['BsmtCond'].replace(to_replace=BsmtCond)
    BsmtQual = {None: 0, 'Po': 1, 'Fa': 2, 'TA': 3, 'Gd': 4, 'Ex': 5}
    df['BsmtQual'] = df['BsmtQual'].replace(to_replace=BsmtQual)
    Foundation = {'Wood': 0, 'Stone': 1, 'Slab': 2, 'PConc': 3, 'CBlock': 4, 'BrkTil': 5}
    df['Foundation'] = df['Foundation'].replace(to_replace=Foundation)
    LotFrontage = {None: 0}
    df['LotFrontage'] = df['LotFrontage'].replace(to_replace=LotFrontage)
    PavedDrive = {'Y': 0, 'P': 1, 'N': 2}
    df['PavedDrive'] = df['PavedDrive'].replace(to_replace=PavedDrive)
    Street = {'Grvl': 0, 'Pave': 1}
    df['Street'] = df['Street'].replace(to_replace=Street)
    Alley = {None: 0, 'Grvl': 1, 'Pave': 2}
    df['Alley'] = df['Alley'].replace(to_replace=Alley)
    LotShape = {'Reg': 0, 'IR1': 1, 'IR2': 2, 'IR3': 3}
    df['LotShape'] = df['LotShape'].replace(to_replace=LotShape)
    LandContour = {'Lvl': 0, 'Bnk': 1, 'HLS': 2, 'Low': 3}
    df['LandContour'] = df['LandContour'].replace(to_replace=LandContour)
    Utilities = {'AllPub': 0, 'NoSewr': 1, 'NoSeWa': 2, 'ELO': 3}
    df['Utilities'] = df['Utilities'].replace(to_replace=Utilities)
    LotConfig = {'Inside': 0, 'Corner': 1, 'CulDSac': 2, 'FR2': 3, 'FR3': 4}
    df['LotConfig'] = df['LotConfig'].replace(to_replace=LotConfig)
    LandSlope = {'Gtl': 0, 'Mod': 1, 'Sev': 2}
    df['LandSlope'] = df['LandSlope'].replace(to_replace=LandSlope)
    Neighborhood = {'Blmngtn': 0, 'Blueste': 1, 'BrDale': 2, 'BrkSide': 3, 'ClearCr': 4, 'CollgCr': 5, 'Crawfor': 6,
                         'Edwards': 7, 'Gilbert': 8, 'IDOTRR': 9, 'MeadowV': 10, 'Mitchel': 11, 'NAmes': 12,
                         'NoRidge': 13, 'NPkVill': 14, 'NridgHt': 15, 'NWAmes': 16, 'OldTown': 17, 'SWISU': 18,
                         'Sawyer': 19, 'SawyerW': 20, 'Somerst': 21, 'StoneBr': 22, 'Timber': 23, 'Veenker': 24}
    df['Neighborhood'] = df['Neighborhood'].replace(to_replace=Neighborhood)
    Condition1 = {'Artery': 0, 'Feedr': 1, 'Norm': 2, 'RRNn': 3, 'RRAn': 4, 'PosN': 5, 'PosA': 6, 'RRNe': 7,
                       'RRAe': 8}
    df['Condition1'] = df['Condition1'].replace(to_replace=Condition1)
    Condition2 = {'Artery': 0, 'Feedr': 1, 'Norm': 2, 'RRNn': 3, 'RRAn': 4, 'PosN': 5, 'PosA': 6, 'RRNe': 7,
                       'RRAe': 8}
    df['Condition2'] = df['Condition2'].replace(to_replace=Condition2)
    BldgType = {'1Fam': 0, '2fmCon': 1, 'Duplex': 2, 'TwnhsE': 3, 'Twnhs': 4}
    df['BldgType'] = df['BldgType'].replace(to_replace=BldgType)

    HouseStyle = {'1Story': 0, '1.5Fin': 1, '1.5Unf': 2, '2Story': 3, '2.5Fin': 4, '2.5Unf': 5, 'SFoyer': 6, 'SLvl': 7}
    df['HouseStyle'] = df['HouseStyle'].replace(to_replace=HouseStyle)

    RoofStyle = {'Flat': 0, 'Gable': 1, 'Gambrel': 2, 'Hip': 3, 'Mansard': 4, 'Shed': 5}
    df['RoofStyle'] = df['RoofStyle'].replace(to_replace=RoofStyle)
    RoofMatl = {'ClyTile': 0, 'CompShg': 1, 'Membran': 2, 'Metal': 3, 'Roll': 4, 'Tar&Grv': 5, 'WdShake': 6,
                     'WdShngl': 7}
    df['RoofMatl'] = df['RoofMatl'].replace(to_replace=RoofMatl)
    Exterior1st = {None: 17, 'AsbShng': 0, 'AsphShn': 1, 'BrkComm': 2, 'BrkFace': 3, 'CBlock': 4, 'CemntBd': 5, 'HdBoard': 6,
                        'ImStucc': 7, 'MetalSd': 8, 'Other': 9, 'Plywood': 10, 'PreCast': 11, 'Stone': 12, 'Stucco': 13,
                        'VinylSd': 14, 'Wd Sdng': 15, 'WdShing': 16}
    df['Exterior1st'] = df['Exterior1st'].replace(to_replace=Exterior1st)
    Exterior2nd = {None: 17, 'AsbShng': 0, 'AsphShn': 1, 'Brk Cmn': 2, 'BrkFace': 3, 'CBlock': 4, 'CmentBd': 5, 'HdBoard': 6,
                        'ImStucc': 7, 'MetalSd': 8, 'Other': 9, 'Plywood': 10, 'PreCast': 11, 'Stone': 12, 'Stucco': 13,
                        'VinylSd': 14, 'Wd Sdng': 15, 'Wd Shng': 16}
    df['Exterior2nd'] = df['Exterior2nd'].replace(to_replace=Exterior2nd)
    MasVnrType = {None: 0, 'BrkCmn': 1, 'BrkFace': 2, 'CBlock': 3, 'None': 4, 'Stone': 5}
    df['MasVnrType'] = df['MasVnrType'].replace(to_replace=MasVnrType)
    MasVnrArea = {None: 0}
    df['MasVnrArea'] = df['MasVnrArea'].replace(to_replace=MasVnrArea)
    ExterQual = {None: 0, 'Po': 1, 'Fa': 2, 'TA': 3, 'Gd': 4, 'Ex': 5}
    df['ExterQual'] = df['ExterQual'].replace(to_replace=ExterQual)
    ExterCond = {None: 0, 'Po': 1, 'Fa': 2, 'TA': 3, 'Gd': 4, 'Ex': 5}
    df['ExterCond'] = df['ExterCond'].replace(to_replace=ExterCond)

    PoolQC = {None: 0, 'Po': 1, 'Fa': 2, 'TA': 3, 'Gd': 4, 'Ex': 5}
    df['PoolQC'] = df['PoolQC'].replace(to_replace=PoolQC)
    Fence = {None: 0, 'MnWw': 1, 'GdWo': 2, 'MnPrv': 3, 'GdPrv': 4}
    df['Fence'] = df['Fence'].replace(to_replace=Fence)
    SaleType = {None: 0, 'WD': 1, 'CWD': 2, 'VWD': 3, 'New': 4, 'COD': 5, 'Con': 6, 'ConLw': 7, 'ConLI': 8, 'ConLD': 9,
                'Oth': 10}
    df['SaleType'] = df['SaleType'].replace(to_replace=SaleType)
    SaleCondition = {'Normal': 0, 'Abnorml': 1, 'AdjLand': 2, 'Alloca': 3, 'Family': 4, 'Partial': 5}
    df['SaleCondition'] = df['SaleCondition'].replace(to_replace=SaleCondition)
    MiscFeature = {None: 0, 'Elev': 1, 'Gar2': 2, 'Othr': 3, 'Shed': 4, 'TenC': 5}
    df['MiscFeature'] = df['MiscFeature'].replace(to_replace=MiscFeature)
    return df