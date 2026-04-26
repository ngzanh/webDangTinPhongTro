from django import forms
from .models import PhongTro
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User

class PhongTroForm(forms.ModelForm):
   
    class Meta:
        model = PhongTro
        # Liệt kê các cột trong bảng PhongTro mà bạn muốn người dùng nhập
        fields = ['tieu_de', 'mo_ta', 'gia_thue', 'dien_tich','khu_vuc','dia_chi' ,'so_dien_thoai','hinh_anh'] 
        
        # Tùy chỉnh chữ hiển thị cho đẹp
        labels = {
            'tieu_de': 'Tiêu đề bài đăng',
            'mo_ta' : 'Mô tả',
            'gia_thue': 'Giá thuê (VNĐ/tháng)',
            'dien_tich': 'Diện tích (m²)',
            'khu_vuc' : 'Thành Phố/Tỉnh',
            'dia_chi': 'Địa chỉ chi tiết',
            'so_dien_thoai' : 'Số điện thoại liên hệ',
            'hinh_anh': 'Hình ảnh phòng',
        }

        # class CSS của Tailwind vào ô chọn Khu vực cho đẹp mắt
        widgets = {
            'khu_vuc': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500'
            }),
            # Bạn có thể làm tương tự cho các ô khác nếu muốn
            'dia_chi': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500',
                'placeholder': 'VD: 120 An Liễng, Đống Đa'
            }),
        }

class TaoTaiKhoanForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']
        labels = {
            'username': 'Tên đăng nhập',
            'unique': 'Tên đăng nhập này đã có người sử dụng. Vui lòng chọn tên khác!',
            'invalid': 'Tên đăng nhập chỉ được chứa chữ cái, số và các ký tự @/./+/-/_'
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Vòng lặp này sẽ đi qua tất cả các ô nhập (username, password...) 
        # và xóa sạch dòng chữ hướng dẫn mặc định
        for field in self.fields.values():
            field.help_text = ''
        self.error_messages['password_mismatch'] = 'Hai mật khẩu bạn nhập không khớp nhau. Vui lòng kiểm tra lại!'