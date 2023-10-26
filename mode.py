import datetime
from django.db import models
from django_jalali.db import models as jmodels


class Product(models.Model):
    code = models.CharField(max_length=10)
    color = models.ColorField(default='#FF0000')
    name = models.CharField()
    group = models.CharField()
    price = models.IntegerField(min_value=0, max_value=100000000)

    def clean_code(self):
        code = unidecode(self.cleaned_data['code'])
        if not re.search(r'^\d{10}$', code):
            raise ValidationError("کد باید 10 رقمی باشد!")
        return code

    def clean_price(self, value):
        if value > 100000000:
            raise ValidationError("قیمت نمی تواند بیشتز از این مقدار باشد !")
        return value


class customer(models.Model):
    fullname = models.CharField(max_length=25, required=True)
    national_code = models.IntegerField(max_length=10, required=True)
    phone_number = models.IntegerField(max_length=10, error_messages={
        'required': ("فیلد موبایل  اجباری است!"), })
    tell = models.IntegerField();
    number_no = models.IntegerField(max_length=24)

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not re.match(r'(09|۰۹)\S{9}$', phone_number):
            raise ValidationError("شماره موبایل   صحت ندارد")
        if phone_number != '' and not phone_number.isdigit():
            raise ValidationError("شماره موبایل نمی تواند شامل حروف باشد.")
        return phone_number

    def clean_national_code(self):
        national_code = unidecode(self.cleaned_data['national_code'])
        if not re.search(r'^\d{10}$', national_code):
            raise ValidationError("کدملی باید 10 رقمی باشد!")

        if not national_code.isdigit():
            raise ValidationError("کدملی تنها میتواند شامل عدد باشد!")

        check = int(national_code[9])
        s = sum([int(national_code[x]) * (10 - x) for x in range(9)]) % 11
        p = (s < 2 and check == s) or (s >= 2 and check + s == 11)
        if not p:
            raise ValidationError("کدملی واردشده صحت ندارد!")

        elif len(national_code) != 10:
            raise ValidationError("کدملی باید 10 رقمی باشد!")
        return national_code

    def clean_number_no(self):
        number_no = self.cleaned_data['number_no']
        if not number_vo_validate(number_no):
            raise ValidationError("شماره شبا صحیح نمی باشد .")
        return number_no
