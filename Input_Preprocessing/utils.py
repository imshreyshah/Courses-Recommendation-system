import numpy as np

def reduce_mem_usage(df,print_log = False, verbose=True):
    ''' Data usage reduction function. Returns the modified dataframe\n
    Parameters\n
        df: pandas.DataFrame
            Dataframe whose size is to be reduced
        print_log: bool, default False
            If True prints the amount of memory reduced
    Returns - Modified Dataframe\n
    '''
    
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    
    #Noting the memory usage at beggining
    start_mem = df.memory_usage().sum() / 1024**2
    
    for col in df.columns:
        col_type = df[col].dtypes
        
        #If any of the column dtype is one amongst the numerics, check for possible reduction
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                
                else:
                    df[col] = df[col].astype(np.float64)

    #Noting the memory usage at end
    end_mem = df.memory_usage().sum() / 1024**2
    
    #Print the memory reduction if print_log == True
    if(print_log == True):
        print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
        print('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))

    return df