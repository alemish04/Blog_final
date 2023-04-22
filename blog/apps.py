from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        from . import signals

# from django.apps import AppConfig


# class UsersConfig(AppConfig):
#     name = 'users'

# add this function
# def ready(self):
#     from . import signals

# # users/__init__.py
# default_app_config = 'users.apps.UsersConfig'
