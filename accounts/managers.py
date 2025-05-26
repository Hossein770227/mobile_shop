from django.utils.translation import gettext as _
from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, phone_number, full_name, password=None, **extra_fields):
        if not phone_number:
            raise ValueError(_('Users must have a phone number'))

        user = self.model(
            phone_number=phone_number,
            full_name=full_name,
            **extra_fields
        )

        if password:
            user.set_password(password)
        else:
            raise ValueError(_("Password can't be empty"))

        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)  # Use is_staff for superuser
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)  # You might not need this

        if not password:
            raise ValueError(_("Password can't be empty"))

        user = self.create_user(phone_number, full_name, password, **extra_fields)
        user.save(using=self._db)
        return user
