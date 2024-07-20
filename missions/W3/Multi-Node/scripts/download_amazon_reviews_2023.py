import argparse
import os
from urllib.request import urlopen

BLOCK_SIZE = 1024 * 1024

parser = argparse.ArgumentParser(prog='download_amazon_reviews_2023')
parser.add_argument('num_files', type=int)


if __name__ == '__main__':
    args = parser.parse_args()

    if not os.path.exists('./amazon-reviews-2023'):
        os.mkdir('./amazon-reviews-2023')

    with urlopen('https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/resolve/main/all_categories.txt') as response:
        with open('./amazon-reviews-2023/all_categories.txt', 'wb') as f:
            f.write(response.read())

    with open('./amazon-reviews-2023/all_categories.txt', 'r') as f:
        num_files = 0
        for filename in f:
            filename = filename.strip()
            if filename == '':
                break
            
            download_msg = f'Downloading {filename} from huggingfaces... '
            print(download_msg, end='')
            url = f'https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/resolve/main/raw/review_categories/{filename}.jsonl'
            
            with urlopen(url) as response:
                with open(f'./amazon-reviews-2023/{filename}.jsonl', 'wb') as f:
                    filesize_mb = 1
                    bytes_block = response.read(BLOCK_SIZE)
                    while len(bytes_block) > 0:
                        f.write(bytes_block)
                        filesize_mb += 1
                        bytes_block = response.read(BLOCK_SIZE)
                        print('\r' + download_msg, filesize_mb, "MB", end='')
            print('\r' + download_msg + 'Done!            ')
            num_files += 1
            if args.num_files is not None and num_files == args.num_files:
                break
        
    os.remove('./amazon-reviews-2023/all_categories.txt')