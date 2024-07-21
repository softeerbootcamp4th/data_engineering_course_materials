from bs4 import BeautifulSoup

# HTML 파일 경로 설정
input_html = "romeo.html"
output_txt = "romeo_text_file.txt"

# HTML 파일 읽기
with open(input_html, 'r', encoding='utf-8') as file:
    html_content = file.read()

# BeautifulSoup 객체 생성
soup = BeautifulSoup(html_content, 'html.parser')

# 텍스트 추출
text = soup.get_text()

# 추출된 텍스트를 파일에 저장
with open(output_txt, 'w', encoding='utf-8') as file:
    file.write(text)
