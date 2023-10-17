import pandas as pd
import numpy as np

def convert_to_average(values):
    clean_str = [float(x) for x in values.strip('"[]"').split(", ")]
    return np.mean(clean_str)

files = ["mea_kp_ns_verification_target_GA_32_CR_0.7.csv", 
        "mea_kp_ns_verification_target_GA_32_CR_0.8.csv",
        "mea_kp_ns_verification_target_GA_32_CR_0.9.csv",
        "mea_kp_ns_verification_target_GA_32_CR_1.0.csv"]
dfs = []
cols = ["GA_0.7", "GA_0.8", "GA_0.9", "GA_1.0"]
for file in files:
    df = pd.read_csv(file, index_col=0)
    #for col in df.columns:
    #    df[col] = df[col].apply(convert_to_average)
    
    print(f"Done with dataset: {file}.\n {df.head()}")
    df = df[cols]
    print(f"Rearrange cols: \n{df.head()}")
    dfs.append(df)

final_df = pd.concat(dfs)
print(final_df)
final_df.to_csv("ns_performance_GAs.csv", index=False)

