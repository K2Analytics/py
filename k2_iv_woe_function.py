# -*- coding: utf-8 -*-
"""
@website: https://k2analytics.co.in
@blog: https://k2analytics.co.in/blog
@email: info@k2analytics.co.in
"""



def woe(df, target,var,bins = 10,fill_na = True):
    df = df.copy()


    if(df[var].dtype.kind in 'biufc'):
        df['decile']=pd.qcut(df[i].rank(method='first'), bins, labels=False) ### Rank 
        if (fill_na== True):
            df['decile'] = df['decile'].fillna(value="Missing")
        Rank=df.groupby('decile').apply(lambda x: pd.Series([
            np.sum(x[target]),
            np.size(x[target][x[target]==0]),
            ],
            index=(["cnt_resp","cnt_non_resp"])
            )).reset_index()


    else:
        if (fill_na== True):
            df[var] = df[var].fillna(value="Missing")
        Rank=df.groupby(var).apply(lambda x: pd.Series([
            np.sum(x[target]),
            np.size(x[target][x[target]==0]),
            ],
            index=(["cnt_resp","cnt_non_resp"])
            )).reset_index()

    Rank["pct_resp"]=Rank["cnt_resp"]/np.sum(Rank["cnt_resp"])
    Rank["pct_non_resp"]=Rank["cnt_non_resp"]/np.sum(Rank["cnt_non_resp"])
    Rank["WOE"] = np.log(Rank["pct_resp"] / Rank["pct_non_resp"])


    return(Rank)
    



def iv(df, target,bins = 10,fill_na = True,rm_cols =[]):
    df = df.copy()
    col_names = df.dtypes.index
    col_names = col_names.delete(df.columns.get_loc(target)) 
    
    for i in rm_cols:
        col_names = col_names.delete(df.columns.get_loc(i)) 
    
    iv_df = pd.DataFrame()
    for i in col_names:
        if(df[var].dtype.kind in 'biufc'):
            df['decile']=pd.qcut(df[i].rank(method='first'), bins, labels=False) ### Rank 
            if (fill_na== True):
                df['decile'] = df['decile'].fillna(value="Missing")
            Rank=df.groupby('decile').apply(lambda x: pd.Series([
                np.sum(x[target]),
                np.size(x[target][x[target]==0]),
                ],
                index=(["cnt_resp","cnt_non_resp"])
                )).reset_index()
        else:
            if (fill_na== True):
                df[i] = df[i].fillna(value="Missing")
            Rank=df.groupby(i).apply(lambda x: pd.Series([
                np.sum(x[target]),
                np.size(x[target][x[target]==0]),
                ],
                index=(["cnt_resp","cnt_non_resp"])
                )).reset_index()    
        Rank["pct_resp"]=Rank["cnt_resp"]/np.sum(Rank["cnt_resp"])
        Rank["pct_non_resp"]=Rank["cnt_non_resp"]/np.sum(Rank["cnt_non_resp"])
        Rank["resp_minus_non_resp"] = Rank["pct_resp"] - Rank["pct_non_resp"]
        Rank["WOE"] = np.log(Rank["pct_resp"] / Rank["pct_non_resp"])
        Rank["IV"] = Rank["resp_minus_non_resp"] * Rank["WOE"]
        iv_df_1 = pd.DataFrame({'Var':[i], "IV":[Rank["IV"].sum()]})
        iv_df = iv_df.append(iv_df_1)

    iv_df = iv_df.sort_values('IV', ascending=False).reset_index(drop = True)
    return(iv_df)
    
