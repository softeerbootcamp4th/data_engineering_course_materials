#!/usr/bin/env python3

import PyPDF2

def pdf_to_text(pdf_path : str, txt_path : str) -> None:
    """
    PDF 파일을 텍스트 파일로 변환
    
    pdf_path: PDF 파일 경로
    txt_path: 텍스트 파일 경로
    """
    
    # PDF 파일 열기
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        number_of_pages = len(reader.pages)
        
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            # 모든 페이지를 순회하며 텍스트 추출
            for page_number in range(number_of_pages):
                page = reader.pages[page_number]
                text = page.extract_text()
                
                if text:
                    # 추출한 텍스트를 파일에 쓰기
                    txt_file.write(text)
                    txt_file.write('\n')


# 테스트
pdf_path = './pride_and_prejudice.pdf'
txt_path = './mapreduce/input.txt'
pdf_to_text(pdf_path, txt_path)
