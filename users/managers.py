from django.contrib.auth.models import BaseUserManager

class UserAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)
        email = email.lower()
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user
