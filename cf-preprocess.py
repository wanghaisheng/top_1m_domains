
import modin.pandas as pd
import os
import time
import ray
# Look at the Ray documentation with respect to the Ray configuration suited to you most.
# ray.shutdown()
ray.init(ignore_reinit_error=True)
def merge_csv_files(file_paths, output_path):
    # Read all CSV files into a list of DataFrames
    dfs = []
    for file in file_paths:
        df = pd.read_csv(file)
        rank=os.path.basename(file).split('-')[4]
        # ('cloudflare-radar-domains-top-','').replace('-20240617-20240624.csv','')
        print(rank)
        df['cfrank']=rank

        # df['source_file'] = os.path.basename(file)  # Add a column to track the source file
        dfs.append(df[:1000000])
        print(f"File: {file}, Domains: {len(df)}")

    # Merge all DataFrames on the 'domain' column
    # # 假设 dfs 是包含所有DataFrame的列表

    # 从第二个DataFrame开始合并
    # 假设 dfs 是包含所有DataFrame的列表
    # 使用pd.concat一次性合并所有的DataFrame
    all_df = pd.concat(dfs, ignore_index=True)

    # 按'domain'进行分组，并使用idxmin找到每个'domain'对应的最小'cfrank'索引
    idx_to_keep = all_df.groupby('domain')['cfrank'].idxmin()

    # 使用找到的索引过滤DataFrame，只保留'cfrank'最小的行
    merged_df = all_df.loc[idx_to_keep].reset_index(drop=True)

    # 打印最终结果的头部
    merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]

    # 打印最终结果
    
    # Sort by domain
    merged_df = merged_df.sort_values('domain')
    
 
    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv(output_path, index=False)
    
    print(f"Merged CSV saved to {output_path}")
    print(f"Total number of unique domains in merged file: {len(merged_df)}")




l=[
'cloudflare-radar-domains-top-1000000-20240701-20240708.csv',
r'c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-500000-20240617-20240624.csv',
r'c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-200000-20240617-20240624.csv',
r'c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-100000-20240617-20240624.csv', 
r'c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-50000-20240617-20240624.csv', 
r'c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-20000-20240617-20240624.csv', 
r'c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-10000-20240617-20240624.csv', 
r'c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-5000-20240617-20240624.csv',
r'c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-2000-20240617-20240624.csv',
r'c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-1000-20240617-20240624.csv',
r'c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-500-20240617-20240624.csv', 
r'c:\Users\Administrator\Downloads\cloudflare-radar-domains-top-200-20240617-20240624.csv']





output_path =r'D:\Download\audio-visual\a_ideas\cloudflare-radar-domains-top-1000000-rank.csv'



merge_csv_files(l, output_path)
# import modin.pandas as pd
# df =pd.read_csv(output_path)
# count=df['domain']
# print(len(list(set(count))))
