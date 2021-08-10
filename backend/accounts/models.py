from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.
class AccountsManager(BaseUserManager):
    def create_user(self, email, password = None, **extra_fields):
        if(not email):
            raise ValueError("Please Enter Email Address")
        user = self.model(
                email = self.normalize_email(email),
                **extra_fields
            )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password, **extra_fields):
        if(not email):
            raise ValueError("Please Enter Email Address")
        user = self.create_user(
                email = self.normalize_email(email),
                password = password,
                **extra_fields,
            )
        
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    first_name = models.CharField(max_length=200)    
    last_name = models.CharField(max_length=200)    
    email = models.EmailField(max_length = 100,unique = True)

    
    date_joined = models.DateTimeField(auto_now_add = True)
    last_login = models.DateTimeField(auto_now = True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default = True)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = AccountsManager()

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True
    
    class Meta:
        verbose_name_plural = 'Users'

from PIL import Image

def profile_pic_path(instance,filename):
    return 'profile_pics/{0}/{1}'.format(instance.user.id,filename)

class Profile(models.Model):
    user = models.OneToOneField(Users,on_delete = models.CASCADE)
    gender = models.CharField(max_length=50,default='NA')
    experience = models.CharField(max_length=50,default='NA')
    city = models.CharField(max_length=50,default='NA')
    state = models.CharField(max_length=50,default='NA')
    country = models.CharField(max_length=50,default='NA')
    phone = models.CharField(max_length=20,default='NA')
    bio = models.TextField(default='NA')
    image = models.ImageField(default='profile_pics/default.png',upload_to=profile_pic_path)
    following = models.ManyToManyField(Users,related_name='following',null=True,blank=True)
    followers = models.ManyToManyField(Users,related_name='followers',null=True,blank=True)
    
    def __str__(self):
        return f'id : {self.user.id} Profile'

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.image.path)

        if(img.height > 300 or img.width > 300):
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
            
    def num_followers(self):
        return self.followers.count()
    
    def num_following(self):
        return self.following.count()