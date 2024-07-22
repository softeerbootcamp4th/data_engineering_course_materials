import json
import pandas as pd

def process_chunk(chunk):
    # JSON 객체를 DataFrame으로 변환
    df = pd.json_normalize(chunk)
    return df

filename = 'untracked/asin2category.json'
chunk_size = 10000  # 한 번에 읽을 JSON 객체 수
dfs = []

with open(filename, 'r') as f:
    chunk = []
    for line in f:
        chunk.append(json.loads(line))
        if len(chunk) >= chunk_size:
            df_chunk = process_chunk(chunk)
            dfs.append(df_chunk)
            chunk = []

    # 마지막 남은 chunk 처리
    if chunk:
        df_chunk = process_chunk(chunk)
        dfs.append(df_chunk)

# 모든 청크를 하나의 DataFrame으로 병합
df = pd.concat(dfs, ignore_index=True)

print(df)
