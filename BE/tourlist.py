import requests
import pandas as pd

def cave():
    # 파라미터 설정
    keyword = '동굴'  # 검색할 키워드
    page_no = 1  # 페이지 번호
    num_of_rows = 1000  # 한 페이지에 표시할 데이터 수
    service_key = 'YjJ6%2Fr8ksXQJXkOYslKdlA2GgmKG%2FuSY2VyRC8uer9e89lIY0uY6dmwxB8VYEhMGZMnPVnHfjSqey3BYG41SwQ%3D%3D'  # 서비스 키
    content_type_id = 12  # 콘텐츠 타입 ID
    cat3 = 'A01011900'  # 카테고리 3

    def fetch_data(keyword, page_no, num_of_rows, service_key, content_type_id, cat3):
        # URL 생성
        url = f"http://apis.data.go.kr/B551011/KorService1/searchKeyword1?numOfRows={num_of_rows}&pageNo={page_no}&MobileOS=ETC&MobileApp=Test&_type=JSON&keyword={keyword}&contentTypeId={content_type_id}&cat3={cat3}&serviceKey={service_key}"

        # 데이터 요청
        response = requests.get(url)
        
        # 상태 코드 확인
        if response.status_code == 200:
            contents = response.json()  # JSON으로 변환
            items = contents.get('response', {}).get('body', {}).get('items', {}).get('item', [])
            return items
        else:
            return {"error": f"Request failed with status code {response.status_code}"}

    # 데이터 가져오기
    items = fetch_data(keyword, page_no, num_of_rows, service_key, content_type_id, cat3)

    # 데이터프레임으로 변환
    if isinstance(items, list):
        df = pd.DataFrame(items)
        df = df[df['firstimage'].str.strip() != '']
    else:
        print("No items found or error occurred.")
    return df


def flower():
    category_dict = {'A01010500': '공원', 'A01010600': '공원', 'A01010700': '공원'}
    for cat3,keyword in category_dict.items():
        page_no = 1  # 페이지 번호
        num_of_rows = 500  # 한 페이지에 표시할 데이터 수
        service_key = 'YjJ6%2Fr8ksXQJXkOYslKdlA2GgmKG%2FuSY2VyRC8uer9e89lIY0uY6dmwxB8VYEhMGZMnPVnHfjSqey3BYG41SwQ%3D%3D'  # 서비스 키
        content_type_id = 12  # 콘텐츠 타입 ID

        def fetch_data(keyword, page_no, num_of_rows, service_key, content_type_id, cat3):
            # URL 생성
            url = f"http://apis.data.go.kr/B551011/KorService1/searchKeyword1?numOfRows={num_of_rows}&pageNo={page_no}&MobileOS=ETC&MobileApp=Test&_type=JSON&keyword={keyword}&contentTypeId={content_type_id}&cat3={cat3}&serviceKey={service_key}"

            # 데이터 요청
            response = requests.get(url)
            
            # 상태 코드 확인
            if response.status_code == 200:
                contents = response.json()  # JSON으로 변환
                items = contents.get('response', {}).get('body', {}).get('items', {}).get('item', [])
                return items
            else:
                return {"error": f"Request failed with status code {response.status_code}"}

        # 데이터 가져오기
        items = fetch_data(keyword, page_no, num_of_rows, service_key, content_type_id, cat3)

        # 데이터프레임으로 변환
        if isinstance(items, list):
            df = pd.DataFrame(items)
            df = df[df['firstimage'].str.strip() != '']
        else:
            print("No items found or error occurred.")
        return df

# 파라미터 설정
def market():
    category_dict = {'A04010100': '시장', 'A04010200': '시장', 'A01010900': '시장'}
    for cat3,keyword in category_dict.items():
        page_no = 1  # 페이지 번호
        num_of_rows = 500  # 한 페이지에 표시할 데이터 수
        service_key = 'YjJ6%2Fr8ksXQJXkOYslKdlA2GgmKG%2FuSY2VyRC8uer9e89lIY0uY6dmwxB8VYEhMGZMnPVnHfjSqey3BYG41SwQ%3D%3D'  # 서비스 키
        content_type_id = 38  # 콘텐츠 타입 ID

        def fetch_data(keyword, page_no, num_of_rows, service_key, content_type_id, cat3):
            # URL 생성
            url = f"http://apis.data.go.kr/B551011/KorService1/searchKeyword1?numOfRows={num_of_rows}&pageNo={page_no}&MobileOS=ETC&MobileApp=Test&_type=JSON&keyword={keyword}&contentTypeId={content_type_id}&cat3={cat3}&serviceKey={service_key}"

            # 데이터 요청
            response = requests.get(url)
            
            # 상태 코드 확인
            if response.status_code == 200:
                contents = response.json()  # JSON으로 변환
                items = contents.get('response', {}).get('body', {}).get('items', {}).get('item', [])
                return items
            else:
                return {"error": f"Request failed with status code {response.status_code}"}

        # 데이터 가져오기
        items = fetch_data(keyword, page_no, num_of_rows, service_key, content_type_id, cat3)

        # 데이터프레임으로 변환
        if isinstance(items, list):
            df = pd.DataFrame(items)
            df = df[df['firstimage'].str.strip() != '']
        else:
            print("No items found or error occurred.")
        return df

def mountains():
    # 파라미터 설정
    keyword = '산'  # 검색할 키워드
    page_no = 1  # 페이지 번호
    num_of_rows = 1000  # 한 페이지에 표시할 데이터 수
    service_key = 'YjJ6%2Fr8ksXQJXkOYslKdlA2GgmKG%2FuSY2VyRC8uer9e89lIY0uY6dmwxB8VYEhMGZMnPVnHfjSqey3BYG41SwQ%3D%3D'  # 서비스 키
    content_type_id = 12  # 콘텐츠 타입 ID
    cat3 = 'A01010400'  # 카테고리 3

    def fetch_data(keyword, page_no, num_of_rows, service_key, content_type_id, cat3):
        # URL 생성
        url = f"http://apis.data.go.kr/B551011/KorService1/searchKeyword1?numOfRows={num_of_rows}&pageNo={page_no}&MobileOS=ETC&MobileApp=Test&_type=JSON&keyword={keyword}&contentTypeId={content_type_id}&cat3={cat3}&serviceKey={service_key}"

        # 데이터 요청
        response = requests.get(url)
        
        # 상태 코드 확인
        if response.status_code == 200:
            contents = response.json()  # JSON으로 변환
            items = contents.get('response', {}).get('body', {}).get('items', {}).get('item', [])
            return items
        else:
            return {"error": f"Request failed with status code {response.status_code}"}

    # 데이터 가져오기
    items = fetch_data(keyword, page_no, num_of_rows, service_key, content_type_id, cat3)

    # 데이터프레임으로 변환
    if isinstance(items, list):
        df = pd.DataFrame(items)
        df = df[df['firstimage'].str.strip() != '']
    else:
        print("No items found or error occurred.")
    return df


# 파라미터 설정
def museum():
    category_dict = {'A02060100': '박물관', 'A02060200': '기념관', 'A02060300': '전시관'}
    for cat3,keyword in category_dict.items():
        page_no = 1  # 페이지 번호
        num_of_rows = 500  # 한 페이지에 표시할 데이터 수
        service_key = 'YjJ6%2Fr8ksXQJXkOYslKdlA2GgmKG%2FuSY2VyRC8uer9e89lIY0uY6dmwxB8VYEhMGZMnPVnHfjSqey3BYG41SwQ%3D%3D'  # 서비스 키
        content_type_id = 14  # 콘텐츠 타입 ID

        def fetch_data(keyword, page_no, num_of_rows, service_key, content_type_id, cat3):
            # URL 생성
            url = f"http://apis.data.go.kr/B551011/KorService1/searchKeyword1?numOfRows={num_of_rows}&pageNo={page_no}&MobileOS=ETC&MobileApp=Test&_type=JSON&keyword={keyword}&contentTypeId={content_type_id}&cat3={cat3}&serviceKey={service_key}"

            # 데이터 요청
            response = requests.get(url)
            
            # 상태 코드 확인
            if response.status_code == 200:
                contents = response.json()  # JSON으로 변환
                items = contents.get('response', {}).get('body', {}).get('items', {}).get('item', [])
                return items
            else:
                return {"error": f"Request failed with status code {response.status_code}"}

        # 데이터 가져오기
        items = fetch_data(keyword, page_no, num_of_rows, service_key, content_type_id, cat3)

        # 데이터프레임으로 변환
        if isinstance(items, list):
            df = pd.DataFrame(items)
            df = df[df['firstimage'].str.strip() != '']
        else:
            print("No items found or error occurred.")
        return df
    

# 파라미터 설정
def sea():
    category_dict = {'A01011200': '해수욕장', 'A02020800': '유람선'}
    for cat3,keyword in category_dict.items():
        page_no = 1  # 페이지 번호
        num_of_rows = 500  # 한 페이지에 표시할 데이터 수
        service_key = 'YjJ6%2Fr8ksXQJXkOYslKdlA2GgmKG%2FuSY2VyRC8uer9e89lIY0uY6dmwxB8VYEhMGZMnPVnHfjSqey3BYG41SwQ%3D%3D'  # 서비스 키
        content_type_id = 12  # 콘텐츠 타입 ID

        def fetch_data(keyword, page_no, num_of_rows, service_key, content_type_id, cat3):
            # URL 생성
            url = f"http://apis.data.go.kr/B551011/KorService1/searchKeyword1?numOfRows={num_of_rows}&pageNo={page_no}&MobileOS=ETC&MobileApp=Test&_type=JSON&keyword={keyword}&contentTypeId={content_type_id}&cat3={cat3}&serviceKey={service_key}"

            # 데이터 요청
            response = requests.get(url)
            
            # 상태 코드 확인
            if response.status_code == 200:
                contents = response.json()  # JSON으로 변환
                items = contents.get('response', {}).get('body', {}).get('items', {}).get('item', [])
                return items
            else:
                return {"error": f"Request failed with status code {response.status_code}"}

        # 데이터 가져오기
        items = fetch_data(keyword, page_no, num_of_rows, service_key, content_type_id, cat3)

        # 데이터프레임으로 변환
        if isinstance(items, list):
            df = pd.DataFrame(items)
            df = df[df['firstimage'].str.strip() != '']
        else:
            print("No items found or error occurred.")
        return df
    

# 파라미터 설정
def night_view():
    category_dict = {'A02050100': '대교', 'A02020800': '유람선'}
    for cat3,keyword in category_dict.items():
        page_no = 1  # 페이지 번호
        num_of_rows = 500  # 한 페이지에 표시할 데이터 수
        service_key = 'YjJ6%2Fr8ksXQJXkOYslKdlA2GgmKG%2FuSY2VyRC8uer9e89lIY0uY6dmwxB8VYEhMGZMnPVnHfjSqey3BYG41SwQ%3D%3D'  # 서비스 키
        content_type_id = 12  # 콘텐츠 타입 ID

        def fetch_data(keyword, page_no, num_of_rows, service_key, content_type_id, cat3):
            # URL 생성
            url = f"http://apis.data.go.kr/B551011/KorService1/searchKeyword1?numOfRows={num_of_rows}&pageNo={page_no}&MobileOS=ETC&MobileApp=Test&_type=JSON&keyword={keyword}&contentTypeId={content_type_id}&cat3={cat3}&serviceKey={service_key}"

            # 데이터 요청
            response = requests.get(url)
            
            # 상태 코드 확인
            if response.status_code == 200:
                contents = response.json()  # JSON으로 변환
                items = contents.get('response', {}).get('body', {}).get('items', {}).get('item', [])
                return items
            else:
                return {"error": f"Request failed with status code {response.status_code}"}

        # 데이터 가져오기
        items = fetch_data(keyword, page_no, num_of_rows, service_key, content_type_id, cat3)

        # 데이터프레임으로 변환
        if isinstance(items, list):
            df = pd.DataFrame(items)
            df = df[df['firstimage'].str.strip() != '']
        else:
            print("No items found or error occurred.")
        return df
    
# 파라미터 설정
def temple():
    category_dict = {'A02010100': '궁', 'A02010200': '성', 'A02010300':'문', 'A02010800':'절'}
    for cat3,keyword in category_dict.items():
        page_no = 1  # 페이지 번호
        num_of_rows = 500  # 한 페이지에 표시할 데이터 수
        service_key = 'YjJ6%2Fr8ksXQJXkOYslKdlA2GgmKG%2FuSY2VyRC8uer9e89lIY0uY6dmwxB8VYEhMGZMnPVnHfjSqey3BYG41SwQ%3D%3D'  # 서비스 키
        content_type_id = 12  # 콘텐츠 타입 ID

        def fetch_data(keyword, page_no, num_of_rows, service_key, content_type_id, cat3):
            # URL 생성
            url = f"http://apis.data.go.kr/B551011/KorService1/searchKeyword1?numOfRows={num_of_rows}&pageNo={page_no}&MobileOS=ETC&MobileApp=Test&_type=JSON&keyword={keyword}&contentTypeId={content_type_id}&cat3={cat3}&serviceKey={service_key}"

            # 데이터 요청
            response = requests.get(url)
            
            # 상태 코드 확인
            if response.status_code == 200:
                contents = response.json()  # JSON으로 변환
                items = contents.get('response', {}).get('body', {}).get('items', {}).get('item', [])
                return items
            else:
                return {"error": f"Request failed with status code {response.status_code}"}

        # 데이터 가져오기
        items = fetch_data(keyword, page_no, num_of_rows, service_key, content_type_id, cat3)

        # 데이터프레임으로 변환
        if isinstance(items, list):
            df = pd.DataFrame(items)
            df = df[df['firstimage'].str.strip() != '']
        else:
            print("No items found or error occurred.")
        return df

# 파라미터 설정
def theme_park():
    keyword = '공원'  # 검색할 키워드
    page_no = 1  # 페이지 번호
    num_of_rows = 1000  # 한 페이지에 표시할 데이터 수
    service_key = 'YjJ6%2Fr8ksXQJXkOYslKdlA2GgmKG%2FuSY2VyRC8uer9e89lIY0uY6dmwxB8VYEhMGZMnPVnHfjSqey3BYG41SwQ%3D%3D'  # 서비스 키
    content_type_id = 12  # 콘텐츠 타입 ID
    cat3 = 'A02020600'  # 카테고리 3

    def fetch_data(keyword, page_no, num_of_rows, service_key, content_type_id, cat3):
        # URL 생성
        url = f"http://apis.data.go.kr/B551011/KorService1/searchKeyword1?numOfRows={num_of_rows}&pageNo={page_no}&MobileOS=ETC&MobileApp=Test&_type=JSON&keyword={keyword}&contentTypeId={content_type_id}&cat3={cat3}&serviceKey={service_key}"

        # 데이터 요청
        response = requests.get(url)
        
        # 상태 코드 확인
        if response.status_code == 200:
            contents = response.json()  # JSON으로 변환
            items = contents.get('response', {}).get('body', {}).get('items', {}).get('item', [])
            return items
        else:
            return {"error": f"Request failed with status code {response.status_code}"}

    # 데이터 가져오기
    items = fetch_data(keyword, page_no, num_of_rows, service_key, content_type_id, cat3)

    # 데이터프레임으로 변환
    if isinstance(items, list):
        df = pd.DataFrame(items)
        df = df[df['firstimage'].str.strip() != '']
    else:
        print("No items found or error occurred.")
    return df
