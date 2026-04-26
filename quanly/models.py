from django.db import models
from django.contrib.auth.models import User

class PhongTro(models.Model):
    # Người đăng bài (liên kết với tài khoản người dùng)
    chu_tro = models.ForeignKey(User, on_delete=models.CASCADE) 
    
    # Các thông tin cơ bản của phòng trọ
    tieu_de = models.CharField(max_length=200)       # Chữ ngắn
    mo_ta = models.TextField()                       # Chữ dài (nhiều dòng)
    gia_thue = models.IntegerField()                 # Số nguyên (Ví dụ: 3000000)

    @property
    
    def gia_thue_co_cham(self):
        # Format số bằng dấu phẩy, sau đó thay thế dấu phẩy thành dấu chấm
        if self.gia_thue:
            return "{:,}".format(self.gia_thue).replace(',', '.')
        return "0"

    dien_tich = models.FloatField()                  # Số thập phân (Ví dụ: 25.5 m2)

    DANH_SACH_KHU_VUC = [
        ('Hà Nội', 'Hà Nội'),
        ('TPHCM', 'TPHCM'),
        ('Đà Nẵng', 'Đà Nẵng'),
        ('Kiên Giang', 'Kiên Giang'),
        ('Thái Bình', 'Thái Bình'),
        ('Hải Phòng', 'Hải Phòng'),
    ]
    khu_vuc = models.CharField(max_length=50, choices=DANH_SACH_KHU_VUC, default='Hà Nội')

    dia_chi = models.CharField(max_length=255)       # Chữ ngắn
    so_dien_thoai = models.CharField(max_length=15)  # Số điện thoại
    hinh_anh = models.ImageField(upload_to='phongtro/', null=True, blank=True) #hinh anh
    
    # Tự động lấy ngày giờ lúc đăng bài
    ngay_dang = models.DateTimeField(auto_now_add=True)
    nguoi_thich = models.ManyToManyField(User, related_name='phong_yeu_thich', blank=True)
    # Hàm này giúp hiển thị tên phòng trọ thay vì các chữ Object khó hiểu
    def __str__(self):
        return self.tieu_de
    
#Khác hàng liên hệ 
class KhachLienHe(models.Model):
    phong = models.ForeignKey(PhongTro, on_delete=models.CASCADE) # Biết là nhắn cho phòng nào
    ten_khach = models.CharField(max_length=100)
    so_dien_thoai = models.CharField(max_length=15)
    noi_dung = models.TextField()
    ngay_gui = models.DateTimeField(auto_now_add=True) # Tự động lưu thời gian gửi

    def __str__(self):
        return f"{self.ten_khach} nhắn hỏi phòng: {self.phong.tieu_de}"

#List Hinh Anh
class HinhAnhPhong(models.Model):
    # Khóa ngoại liên kết với phòng trọ, related_name giúp ta gọi ngược từ phòng trọ ra các ảnh
    phong = models.ForeignKey(PhongTro, related_name='cac_hinh_anh', on_delete=models.CASCADE)
    anh = models.ImageField(upload_to='phongtro_chitiet/')

    def __str__(self):
        return f"Ảnh phụ của phòng: {self.phong.tieu_de}"