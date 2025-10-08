import os
import socket
import psycopg2
from urllib.parse import urlparse, parse_qs

# تحميل .env محلياً فقط
if os.getenv("RENDER") != "true":
    from dotenv import load_dotenv
    load_dotenv()

def _clean_env(key, default=""):
    return (os.getenv(key) or default).replace("\r", "").replace("\n", "").strip()

# قيم افتراضية مأخوذة من واجهة Pooler (الصورة)
DEFAULT_HOST = "aws-1-us-east-2.pooler.supabase.com"
DEFAULT_PORT = "6543"
DEFAULT_USER = "postgres.tqumkcobsergeybnxlb"
DEFAULT_DBNAME = "postgres"

# قراءة المتغيرات من البيئة أو استخدام الافتراضيات
host = _clean_env("DB_HOST", DEFAULT_HOST)
port = _clean_env("DB_PORT", DEFAULT_PORT)
user = _clean_env("DB_USER", DEFAULT_USER)
password = _clean_env("DB_PASS")
dbname = _clean_env("DB_NAME", DEFAULT_DBNAME)

print("DB_HOST repr:", repr(host))
print("DB_PORT repr:", repr(port))
print("DB_USER repr:", repr(user))
print("DB_NAME repr:", repr(dbname))
print("DB_PASS set:", bool(password))

# DATABASE_URL يأخذ الأولوية إن وُجد
database_url = (_clean_env("DATABASE_URL") or _clean_env("DATABASE_URI") or "").strip()
if database_url:
    print("Using DATABASE_URL repr:", repr(database_url))

# محاولة حل IPv4 للعقدة وإرجاع أول IPv4 إن وُجد
def resolve_first_ipv4(hostname):
    try:
        infos = socket.getaddrinfo(hostname, None)
        for family, _, _, _, sockaddr in infos:
            if family == socket.AF_INET:
                return sockaddr[0]
    except Exception as e:
        print("resolve_first_ipv4 error:", e)
    return None

# إن وُجد DATABASE_URL نجرّب استخدامه لكن نبحث عن ipv4 لإجبار hostaddr إن لزم
try:
    ipv4 = resolve_first_ipv4(host)
    print("Resolved IPv4 for host:", ipv4)

    if database_url:
        # نستخدم hostaddr عبر خيار options لإجبار سلوك IPv4 دون كسر الـ DSN
        if ipv4:
            conn = psycopg2.connect(
                database_url,
                options=f"-c hostaddr={ipv4}",
                sslmode="require",
                connect_timeout=5
            )
        else:
            # لا IPv4 متاح، نجرب الاتصال بالـ DATABASE_URL مباشرة (قد يجرب IPv6)
            conn = psycopg2.connect(
                database_url,
                sslmode="require",
                connect_timeout=5
            )
    else:
        # لا DATABASE_URL -> بناء اتصال مفصل. نفضل استخدام ipv4 كـ host إن وُجد
        connect_host = ipv4 if ipv4 else host
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=connect_host,
            port=port or "6543",
            sslmode="require",
            connect_timeout=5
        )

    print("Postgres connection established")
except Exception as e:
    # طباعة واضحة في اللوجات لمساعدة التشخيص
    print("Postgres connection failed:", repr(e))
    raise