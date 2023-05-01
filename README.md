Đây là project thực hiện lấy thông tin các thẻ ngân hàng hiện có. Nếu thấy có ích thì cho mình xin một sao ạ. Thanks
# **1 . Thiết lập môi trường và activate môi trường**
## **Window**
~~~
 py -m venv venv
 .\venv\Scripts\activate
~~~
## **Linux**
~~~
 python3 -m venv venv
 source .\venv\bin\activate
~~~
## **2 . Cài đặt thư viện**
~~~
    pip install -r requirements.txt
~~~
## **3 .Crawl dữ liệu**
## **Window**
~~~
 py crawler.py
~~~
## **Linux**
~~~
 python3 crawler.py
~~~
Sau khi chạy xong thì dữ liệu sẽ được lưu thành bank.xlsx, card_info.xlsx và card_type.xlsx cùng folder image để lưu ảnh. Chạy db_maker.py để thực hiện chuyển về dạng txt
## **Window**
~~~
 py db_maker.py
~~~
## **Linux**
~~~
 python3 db_maker.py
~~~
Dữ liệu sẽ được lưu ở folder data
## **4 .Cấu trúc dữ liệu**
Dữ liệu được lưu theo đúng thứ tự trình bày bên dưới và cách nhau bới dấu, đối với từng cột và mỗi dòng tương ứng với một dòng trong bảng
## **banks.txt**
| Tên cột | Header |
|:-------|:------:|
|  id    |  id của ngân hàng  |
|  bank_name  |  Tên của ngân hàng  |
## **card_type.txt**
| Tên cột | Header |
|:-------|:------:|
|  id    |  id của ngân hàng  |
|  card_name  |  Tên của loại thẻ  |
## **card_info.txt**
| Tên cột | Header |
|:-------|:------:|
|  id    |  id của ngân hàng  |
|  bank_name  |  ID của bank (khóa ngoại)  |
|  card_type  |  ID của card_type (khóa ngoại)  |
|  card_name  |  Tên loại thẻ  |
|  lower_limit  |  Hạn mức dưới  |
|  upper_limit  |  Hạn mức trên  |
|  img_url  |  Tên của ảnh thẻ trong image  |