# Hướng dẫn cài đặt
## Clone repo này về
    git clone https://github.com/vdqhuy0912/online-electronic-store.git
## Di chuyển đến thư mục dự án
    cd OnlineShop
## Chạy docker container
    docker-compose up
## Tạo cơ sở dữ liệu
    docker-compose run shop-app python manage.py makemigrations
    docker-compose run shop-app python manage.py migrate
## Tạo superuser
    docker-compose run shop-app python manage.py createsuperuser