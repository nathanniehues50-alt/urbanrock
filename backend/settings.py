from pathlib import Path

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'   # pasta onde o collectstatic junta tudo

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============================
# SEGURANÇA
# ============================

SECRET_KEY = 'Caralhoa4'
DEBUG = False
ALLOWED_HOSTS = [
    "urbanrock.com.br",
    "www.urbanrock.com.br",
    "104.131.73.32",
    "localhost",
    "127.0.0.1",
]



# ============================
# APPS INSTALADOS
# ============================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',''
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps do projeto
    'produtos',
    'usuarios.apps.UsuariosConfig',   # importante pros signals
]


# ============================
# MIDDLEWARE
# ============================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ============================
# URL PRINCIPAL
# ============================

ROOT_URLCONF = 'backend.urls'


# ============================
# TEMPLATES
# ============================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # templates globais (opcional)
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',   # necessário para request no template
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# ============================
# BANCO DE DADOS
# ============================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ============================
# VALIDAÇÃO DE SENHA
# ============================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ============================
# LÍNGUA / REGIÃO
# ============================

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# ============================
# STATIC FILES
# ============================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"


# ============================
# MEDIA (UPLOADS)
# ============================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ============================
# AUTENTICAÇÃO (MELHOR JEITO)
# ============================

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'


# ============================
# DEFAULT
# ============================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/entrar/'

DEBUG = True

CSRF_TRUSTED_ORIGINS = [
    "https://urbanrock.com.br",
    "https://www.urbanrock.com.br",
]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_SSL_REDIRECT = True

SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30   # 30 dias
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"
