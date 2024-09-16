REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Medium API",
    "DESCRIPTION": "A Medium Clone API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # License information
    "LICENSE": {
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    # Contact information
    "CONTACT": {
        "name": "API Support Team",
        "email": "support@testapi.com",
        "url": "https://testapi.com/contact",
    },
}
