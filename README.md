# Firouzeh Digital – Django Survey Project

این پروژه یک سرویس نظرسنجی مبتنی بر Django است که امکان ساخت پرسشنامه، ثبت پاسخ کاربران، و مشاهده نتایج را فراهم می‌کند.

---

## شروع سریع

### 1. کلون کردن ریپازیتوری

ابتدا ریپازیتوری را از GitHub کلون کنید:

```bash
git clone https://github.com/mohammad2goodarzi/firouzeh-digital.git
cd firouzeh-digital
```

### 2. ساخت و فعال‌سازی محیط مجازی

برای جلوگیری از تداخل پکیج‌ها، یک محیط مجازی بسازید:

```bash
python -m venv venv
source venv/bin/activate  # در ویندوز: venv\Scripts\activate
```

### 3. نصب وابستگی‌ها

پکیج‌های مورد نیاز پروژه را نصب کنید:

```bash
pip install -r requirements.txt
```

### 4. ساخت دیتابیس

تنظیمات دیتابیس را در فایل settings.py بررسی کرده و سپس دستورات زیر را اجرا کنید:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. اجرای تست‌ها

برای اجرای تست‌های پروژه:

```bash
pytest
```

### 6. اجرای سرور توسعه

برای اجرای سرور محلی:

```bash
python manage.py runserver
```

سپس مرورگر را باز کرده و وارد آدرس زیر شوید:

```code
http://127.0.0.1:8000/
```
