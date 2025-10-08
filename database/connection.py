import os
import psycopg2

# تحميل ملفات .env فقط محلياً
if os.getenv("RENDER") != "true":
    from dotenv import load_dotenv
    load_dotenv()

# اقرأ المتغيرات ونظفها من أحرف السطر الجديد والمسافات
def _clean_env(key):
    return (os.getenv(key) or "").replace("\r", "").replace("\n", "").strip()

host = _clean_env("DB_HOST")
user = _clean_env("DB_USER")
password = _clean_env("DB_PASS")
dbname = _clean_env("DB_NAME")
port = _clean_env("DB_PORT")

# طباعة للتصحيح في اللوجات
print("DB_HOST repr:", repr(host))
print("DB_USER repr:", repr(user))
print("DB_NAME repr:", repr(dbname))
print("DB_PORT repr:", repr(port))

# إن كان لديك DATABASE_URL (Connection URI) استخدمها كخيار بديل
database_url = (os.getenv("DATABASE_URL") or os.getenv("DATABASE_URI") or "").strip()
if database_url:
    database_url = database_url.replace("\r", "").replace("\n", "").strip()
    print("Using DATABASE_URL repr:", repr(database_url))
    conn = psycopg2.connect(database_url, sslmode="require")
else:
    # تأكد من وجود قيم أساسية وإلا سيعطي psycopg2 خطأ واضح
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        dbname=dbname,
        port=port or "5432",
        sslmode="require"
    )