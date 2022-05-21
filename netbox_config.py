DEVELOPER = True
DEBUG = True

# Register your plugin here
PLUGINS = ['netbox_config_manager']

# Add any configuration for your plugin here
PLUGINS_CONFIG = {
    'netbox_config_manager': {
        'vault_url': 'http://vault:8200',
        'vault_token': 'hvs.wvgh3Hx8UYPiPrUPaWw3oshg'
    }
}

if DEBUG:
    # Allow docker
    import socket
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'level': 'DEBUG',
#         },
#         'netbox.*': {
#             'level': 'DEBUG',
#         },
#     },
# }
