from django.core.exceptions import ValidationError

class VietHoaDoDaiMatKhau:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            # Ghi đè câu tiếng Anh thành câu tiếng Việt của bạn
            raise ValidationError(
                f"Mật khẩu quá ngắn. Vui lòng nhập ít nhất {self.min_length} ký tự.",
                code='password_too_short',
            )

    def get_help_text(self):
        return f"Mật khẩu phải chứa ít nhất {self.min_length} ký tự."