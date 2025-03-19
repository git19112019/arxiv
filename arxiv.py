import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

# Constants: URL cơ bản cho ArXiv API
API_URL = "http://export.arxiv.org/api/query?"


def fetch_arxiv_papers(keyword, num_results=5):
    """
    Tìm kiếm bài báo trên ArXiv sử dụng API với sắp xếp theo thời gian gần nhất.
    Args:
        keyword (str): Từ khóa tìm kiếm trên ArXiv
        num_results (int): Số lượng kết quả tối đa muốn nhận
    """
    # Xây dựng URL API với sắp xếp theo thời gian
    query_params = {
        'search_query': f"all:{keyword}",
        'start': 0,
        'max_results': num_results,
        'sortBy': 'submittedDate',  # Sắp xếp theo ngày tháng
        'sortOrder': 'descending'  # Mới nhất trước
    }
    query_url = API_URL + urllib.parse.urlencode(query_params)
    print(f"Querying ArXiv API with URL: {query_url}")

    try:
        # Gửi yêu cầu tới API
        response = urllib.request.urlopen(query_url)
        data = response.read().decode('utf-8')
        parse_arxiv_results(data)
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def parse_arxiv_results(data):
    """
    Phân tích dữ liệu XML trả về từ API của ArXiv và hiển thị kết quả.
    Args:
        data (str): Dữ liệu XML trả về từ ArXiv API
    """
    # Phân tích cú pháp XML
    root = ET.fromstring(data)
    namespace = {'atom': 'http://www.w3.org/2005/Atom'}

    # Tìm tất cả các bài báo (entry)
    entries = root.findall('atom:entry', namespace)
    if not entries:
        print("No results found.")
        return

    for entry in entries:
        try:
            # Trích xuất thông tin bài báo
            title = entry.find('atom:title', namespace).text.strip()
            authors = [author.find('atom:name', namespace).text for author in entry.findall('atom:author', namespace)]
            summary = entry.find('atom:summary', namespace).text.strip()
            pdf_link = entry.find('atom:id', namespace).text.strip()

            # Hiển thị thông tin bài báo
            print(f"Title: {title}")
            print(f"Authors: {', '.join(authors)}")
            print(f"Abstract (Preview): {summary[:300]}...")  # Giới hạn tóm tắt 300 ký tự
            print(f"PDF Link: {pdf_link}")
            print("=" * 50)
        except AttributeError:
            print("Error parsing a paper. Skipping...")
            continue


def main():
    """
    Điểm bắt đầu của chương trình. Nhận tham số dòng lệnh, thực hiện tìm kiếm, và hiển thị kết quả.
    """
    keyword = input("Enter the search keyword: ")  # Nhập từ khóa tìm kiếm
    num_results = int(input("Enter the number of results to display: "))  # Số lượng kết quả tối đa

    # Gửi yêu cầu và xử lý kết quả
    fetch_arxiv_papers(keyword, num_results)


if __name__ == '__main__':
    main()