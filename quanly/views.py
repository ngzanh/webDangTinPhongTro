from django.shortcuts import render , redirect # dung cho form đang ky va dang nhap 
from .models import PhongTro
from django.db.models import Q# dung cho form đang ky va dang nhap , tìm kiếm

#Phân đăng tin 
from django.contrib.auth.decorators import login_required
from .forms import PhongTroForm, TaoTaiKhoanForm

# CÁC THƯ VIỆN NÀY ĐỂ LÀM TÀI KHOẢN
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm

#chỉnh sủa tin đăng 
from django.shortcuts import render, redirect, get_object_or_404

#Khách hàng liên hệ 
from .models import KhachLienHe
from .models import HinhAnhPhong

from django.http import HttpResponseRedirect
from django.urls import reverse


# def trang_chu(request):
#     # Lấy tất cả phòng trọ từ database, sắp xếp bài mới nhất lên đầu
#     danh_sach_phong = PhongTro.objects.all().order_by('-ngay_dang')
    
#     # Gửi danh sách này sang file giao diện HTML
#     return render(request, 'quanly/trang_chu.html', {'danh_sach_phong': danh_sach_phong})
def trang_chu(request): # hàm chỉnh sửa để tìm kiếm
    # 1. Lấy toàn bộ danh sách phòng trọ ban đầu
    danh_sach_phong = PhongTro.objects.all().order_by('-id')

    # 2. Hứng các thông số từ thanh tìm kiếm (chính là thuộc tính 'name' trong các thẻ <select>)
    khu_vuc = request.GET.get('khu_vuc')
    gia = request.GET.get('gia')
    dien_tich = request.GET.get('dien_tich')

    # 3. Bắt đầu LỌC (Filter)
    
    # Lọc theo Khu vực: Nếu có chọn khu vực, sẽ tìm những phòng mà "dia_chi" có chứa chữ đó
    if khu_vuc:
        danh_sach_phong = danh_sach_phong.filter(khu_vuc=khu_vuc)

    # Lọc theo Giá
    if gia == 'duoi_3':
        danh_sach_phong = danh_sach_phong.filter(gia_thue__lt=3000000) # Nhỏ hơn 3tr
    elif gia == '3_den_5':
        danh_sach_phong = danh_sach_phong.filter(gia_thue__gte=3000000, gia_thue__lte=5000000) # Từ 3 đến 5tr
    elif gia == 'tren_5':
        danh_sach_phong = danh_sach_phong.filter(gia_thue__gt=5000000) # Lớn hơn 5tr

    # Lọc theo Diện tích
    if dien_tich == 'duoi_20':
        danh_sach_phong = danh_sach_phong.filter(dien_tich__lt=20)
    elif dien_tich == '20_den_30':
        danh_sach_phong = danh_sach_phong.filter(dien_tich__gte=20, dien_tich__lte=30)
    elif dien_tich == 'tren_30':
        danh_sach_phong = danh_sach_phong.filter(dien_tich__gt=30)

    # 4. Gói dữ liệu ĐÃ LỌC để gửi ra giao diện
    context = {
        'danh_sach_phong': danh_sach_phong,
    }
    return render(request, 'quanly/trang_chu.html', context)
# 1. HÀM ĐĂNG KÝ
def dang_ky(request):
    if request.method == 'POST':
        form = TaoTaiKhoanForm(request.POST) # Thay UserCreationForm bằng TaoTaiKhoanForm
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('trang_chu') 
    else:
        form = TaoTaiKhoanForm() # Thay UserCreationForm bằng TaoTaiKhoanForm
    return render(request, 'quanly/dang_ky.html', {'form': form})

# 2. HÀM ĐĂNG NHẬP
def dang_nhap(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('trang_chu')
    else:
        form = AuthenticationForm()
    return render(request, 'quanly/dang_nhap.html', {'form': form})

# 3. HÀM ĐĂNG XUẤT
def dang_xuat(request):
    logout(request)
    return redirect('trang_chu')

#Dang tin 
# Yêu cầu phải đăng nhập mới được vào trang này
@login_required(login_url='dang_nhap')
def dang_tin(request):
    if request.method == 'POST':
        form = PhongTroForm(request.POST, request.FILES) # Thêm request.FILES nếu có up ảnh
        if form.is_valid():
            # 1. Lưu tạm form vào biến phong_tro, khoan ghi vào Database (commit=False)
            phong_tro = form.save(commit=False)
            
            # 2. Gán người đang đăng nhập (request.user) làm chủ trọ
            phong_tro.chu_tro = request.user
            
            # 3. Bây giờ mới chính thức lưu vào Database nè!
            phong_tro.save()
            # --- ĐOẠN MỚI THÊM: Xử lý lưu nhiều ảnh phụ ---
            danh_sach_anh = request.FILES.getlist('hinh_anh_phu') # Lấy danh sách file
            for file_anh in danh_sach_anh:
                # Mỗi vòng lặp sẽ tạo ra 1 dòng trong database liên kết với phòng trọ này
                HinhAnhPhong.objects.create(phong=phong_tro, anh=file_anh)
            # -----------------------------------------------
            # 4. Lưu xong thì chuyển hướng về Trang chủ (hoặc trang danh sách phòng)
            
            return redirect('trang_chu')
    else:
        form = PhongTroForm()
        
    return render(request, 'quanly/dang_tin.html', {'form': form})

#Chỉnh sửa tin sau khi đăng xoa sủa
@login_required(login_url='dang_nhap')
def chinh_sua_tin(request, id):
    phong_tro = get_object_or_404(PhongTro, id=id)

    if phong_tro.chu_tro != request.user:
        return redirect('trang_chu')

    if request.method == 'POST':
        form = PhongTroForm(request.POST, request.FILES, instance=phong_tro)
        if form.is_valid():
            phong_tro = form.save()
            
            # Xử lý xóa các ảnh phụ được chọn theo ID
            ids_can_xoa = request.POST.getlist('xoa_anh_id')
            if ids_can_xoa:
                HinhAnhPhong.objects.filter(id__in=ids_can_xoa).delete()
            
            # Xử lý thêm ảnh phụ mới nếu có upload
            danh_sach_anh_moi = request.FILES.getlist('hinh_anh_phu')
            for file_anh in danh_sach_anh_moi:
                HinhAnhPhong.objects.create(phong=phong_tro, anh=file_anh)
                    
            return redirect('trang_chu')
    else:
        form = PhongTroForm(instance=phong_tro)
        
    return render(request, 'quanly/chinh_sua_tin.html', {'form': form, 'phong_tro': phong_tro})

@login_required(login_url='dang_nhap')
def xoa_tin(request, id):
    phong_tro = get_object_or_404(PhongTro, id=id)
    
    # CHỐT CHẶN BẢO MẬT: Phải đúng chủ mới được xóa
    if phong_tro.chu_tro == request.user:
        phong_tro.delete() # Lệnh xóa cái rụp!
        
    return redirect('trang_chu')

#lấy ra danh sách các phòng do người đang đăng nhập tạo
@login_required(login_url='dang_nhap')
def quan_ly_tin(request):
    # Chỉ lấy những tin của người đang đăng nhập (chu_tro = request.user)
    danh_sach_cua_toi = PhongTro.objects.filter(chu_tro=request.user).order_by('-id')
    return render(request, 'quanly/quan_ly_tin.html', {'danh_sach_cua_toi': danh_sach_cua_toi})

#chi tiết phòng 
def chi_tiet_phong(request, phong_id):
    # Lấy đúng phòng có id đó ra, nếu không tìm thấy sẽ báo lỗi 404
    phong = get_object_or_404(PhongTro, id=phong_id)

    # KHI KHÁCH HÀNG BẤM NÚT GỬI TIN NHẮN (Gửi phương thức POST)
    if request.method == 'POST':
        ten = request.POST.get('ten_khach')
        sdt = request.POST.get('so_dien_thoai')
        loi_nhan = request.POST.get('noi_dung')
        
        # Lưu vào Database
        KhachLienHe.objects.create(
            phong=phong,
            ten_khach=ten,
            so_dien_thoai=sdt,
            noi_dung=loi_nhan
        )
        # Gửi xong thì load lại đúng trang chi tiết đó
        return redirect('chi_tiet_phong', phong_id=phong.id)
    
    context = {
        'phong': phong
    }
    return render(request, 'quanly/chi_tiet.html', context)

#Hamf dde docj thogn tin khacsh guwir 
@login_required(login_url='dang_nhap') # Bắt buộc phải đăng nhập mới được xem
def khach_lien_he(request):
    # Tìm tất cả tin nhắn mà phòng đó có chu_tro chính là user đang đăng nhập
    danh_sach_tin = KhachLienHe.objects.filter(phong__chu_tro=request.user).order_by('-ngay_gui')
    
    context = {
        'danh_sach_tin': danh_sach_tin
    }
    return render(request, 'quanly/khach_lien_he.html', context)

# 1. HÀM XỬ LÝ KHI NGƯỜI DÙNG BẤM NÚT THẢ TIM
@login_required(login_url='dang_nhap')
def thich_phong(request, id):
    phong = get_object_or_404(PhongTro, id=id)
    
    # Kiểm tra xem user này đã nằm trong danh sách người thích của phòng chưa
    if request.user in phong.nguoi_thich.all():
        # Nếu có rồi thì xóa đi (Bỏ thích)
        phong.nguoi_thich.remove(request.user)
    else:
        # Nếu chưa có thì thêm vào (Thả tim)
        phong.nguoi_thich.add(request.user)
        
    # Xong việc thì load lại đúng cái trang mà người dùng vừa đứng
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# 2. HÀM HIỂN THỊ DANH SÁCH CÁC PHÒNG ĐÃ THÍCH
@login_required(login_url='dang_nhap')
def danh_sach_yeu_thich(request):
    # Lấy ra tất cả các phòng mà user đang đăng nhập đã thả tim
    danh_sach = request.user.phong_yeu_thich.all().order_by('-id')
    return render(request, 'quanly/phong_yeu_thich.html', {'danh_sach_phong': danh_sach})
