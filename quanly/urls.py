from django.urls import path
from . import views

urlpatterns = [
    path('', views.trang_chu, name='trang_chu'), # Đường dẫn rỗng '' tức là trang chủ
    path('dang-ky/', views.dang_ky, name='dang_ky'),       # 
    path('dang-nhap/', views.dang_nhap, name='dang_nhap'), # 
    path('dang-xuat/', views.dang_xuat, name='dang_xuat'),
    path('dang-tin/', views.dang_tin, name='dang_tin'), 
    # chinh sua thong tin phong trọ , xoa sua
    path('chinh-sua/<int:id>/', views.chinh_sua_tin, name='chinh_sua_tin'),
    path('xoa/<int:id>/', views.xoa_tin, name='xoa_tin'),

    path('quan-ly-tin/', views.quan_ly_tin, name='quan_ly_tin'),
    path('phong/<int:phong_id>/', views.chi_tiet_phong, name='chi_tiet_phong'),
    #Đường dẫn này có <int:phong_id> để Django biết bạn đang muốn xem chi tiết của phòng số mấy
    #phòng trọ đã thích
    path('thich-phong/<int:id>/', views.thich_phong, name='thich_phong'),
    path('danh-sach-yeu-thich/', views.danh_sach_yeu_thich, name='danh_sach_yeu_thich'),


    #de chur xem duco khach gui 
    path('khach-lien-he/', views.khach_lien_he, name='khach_lien_he'),
]