import pandas as pd
import os

# 현재 스크립트 파일의 절대 경로
script_path = os.path.abspath(__file__)
print(f'Script absolute path: {script_path}')

# 현재 스크립트 파일이 위치한 디렉토리의 경로
script_dir = os.path.dirname(script_path)
print(f'Script directory: {script_dir}')


def convert_to_csv(input_file, output_csv_file):
    # 텍스트 파일을 읽어 DataFrame으로 변환
    df = pd.read_csv(input_file, sep='\t', header=None, names=['Word', 'Count'])

    # DataFrame을 CSV 파일로 저장
    df.to_csv(output_csv_file, index=False)
    
    
def convert_to_sorted_csv(input_file, output_csv_file):
    # 텍스트 파일을 읽어 DataFrame으로 변환
    df = pd.read_csv(input_file, sep='\t', header=None, names=['Word', 'Count'])

    # Count 열을 기준으로 내림차순 정렬
    df = df.sort_values(by='Count', ascending=False)
    
    # DataFrame을 CSV 파일로 저장
    df.to_csv(output_csv_file, index=False)

if __name__ == "__main__":
    input_file = f'{script_dir}/part-00000'  # HDFS에서 다운로드한 파일 경로
    output_csv_file = f'{script_dir}/part-00000.csv'  # 저장할 CSV 파일 경로
    output_sorted_csv_file = f'{script_dir}/part-00000_sorted.csv'  # 저장할 CSV 파일 경로

    convert_to_csv(input_file, output_csv_file)
    convert_to_sorted_csv(input_file, output_sorted_csv_file)
    print(f'File has been converted to CSV and saved as {output_csv_file}')
