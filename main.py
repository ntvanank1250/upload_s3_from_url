import boto3
import requests
import mimetypes
import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env 
load_dotenv()
ENDPOINT_URL = os.getenv("ENDPOINT_URL")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Cấu hình S3
endpoint_url = ENDPOINT_URL
aws_access_key_id = AWS_ACCESS_KEY_ID
aws_secret_access_key = AWS_SECRET_ACCESS_KEY

# Tạo resource và client của S3
s3 = boto3.resource('s3', endpoint_url=endpoint_url,
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key)

s3client = boto3.client('s3', endpoint_url=endpoint_url,
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key)

def get_content_type_from_url(url):
    """
    Trả về kiểu nội dung (content type) tương ứng với đường dẫn URL.

    Args:
        url (str): Đường dẫn URL mà bạn muốn lấy kiểu nội dung tương ứng.

    Returns:
        str: Kiểu nội dung (content type) tương ứng với đường dẫn URL.
              Trả về None nếu không xác định được kiểu nội dung.

    """
    url=url.split('?')[0]
    file_extension = url.split('.')[-1]
    content_type, _ = mimetypes.guess_type('file.{}'.format(file_extension))
    print(content_type)
    return content_type


def upload_file_from_url(bucket_name, file_path, file_url, acl='public-read'):
    """
    Tải lên tệp tin từ URL và lưu trữ nó trong bucket trên Amazon S3.

    Args:
        bucket_name (str): Tên của bucket trên Amazon S3.
        file_path (str): Đường dẫn và tên tệp tin trong bucket để lưu trữ tệp tin.
        file_url (str): Đường dẫn URL của tệp tin mà bạn muốn tải lên và lưu trữ.
        acl (str, optional): Quyền truy cập cho tệp tin tải lên. Mặc định là 'public-read'.

    Returns:
        tuple: Một tuple chứa hai phần tử:
            - message (str): Thông báo kết quả của quá trình tải lên tệp tin.
            - status (bool): Trạng thái thành công hoặc thất bại của quá trình tải lên.

    """
    try:
        response = requests.get(file_url)
        content_type = get_content_type_from_url(file_url)
        if response.status_code == 200:
            s3client.put_object(Body=response.content, Bucket=bucket_name,
                                Key=file_path, ContentType=content_type, ACL=acl)
            message = "Up ảnh thành công"
            status = True
        else:
            message = "Không lấy được ảnh"
            status = False

    except:
        message = "Lỗi khi up ảnh"
        status = False

    finally:
        return message, status
if __name__ == '__main__':
  bucket_name=""
  file_path="/home/user/path/"
  for url in list_url:
    message, status = upload_file_from_url(bucket_name=bucket_name, file_path=path_file.lstrip("/"), file_url=file_url))
