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
