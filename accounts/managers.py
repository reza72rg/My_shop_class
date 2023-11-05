from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
	def create_user(self, phone_number, email, full_name, password):
		if not email:
			raise ValueError('user must have email')
		user = self.model( email=self.normalize_email(email))
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password):
		user = self.create_user( email, password)
		user.is_admin = True
		user.is_superuser = True
		user.save(using=self._db)
		return user
