from django.db import models
from accounts.models import Users
from django.utils import timezone

def path(instance,filename):
    return 'posts/{0}/{1}'.format(instance.photographer.id,filename)

class Posts(models.Model):
    image = models.ImageField(upload_to = path)
    photographer = models.ForeignKey(Users,on_delete=models.CASCADE)
    date = models.DateTimeField(default = timezone.now)
    caption = models.TextField(max_length=10000)
    likes = models.ManyToManyField(Users,related_name='likes',null=True,blank=True)
    class Meta:
        verbose_name_plural = 'Posts'

    def __str__(self):
        return 'Post id : '+str(self.id)
    
    def total_likes(self):
        return self.likes.count()
    
class TextPost(models.Model):
    photographer = models.ForeignKey(Users,on_delete=models.CASCADE)
    date = models.DateTimeField(default = timezone.now)
    caption = models.CharField(max_length=10000)
    likes = models.ManyToManyField(Users,related_name='text_post_likes',null=True,blank=True)
    time = models.DateTimeField(default = timezone.now)
    class Meta:
        verbose_name_plural = 'TextPost'

    def __str__(self):
        return 'Text Post id : '+str(self.id)
    
    def total_likes(self):
        return self.likes.count()
    
class Ratings(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE,null=True)
    comment = models.TextField(null=True,blank=True)
    rating = models.IntegerField()
    time = models.DateTimeField(default = timezone.now)
    class Meta:
        verbose_name_plural = 'Ratings'
        
    def __str__(self):
        return 'Ratings of ( '+str(self.post)+' ) by '+str(self.user)

class Shares(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE,null=True)
    caption = models.TextField()
    time = models.DateTimeField(default = timezone.now)

    class Meta:
        verbose_name_plural = 'Shares'
    
    def __str__(self):
        return 'Sharing '+self.post+'by '+self.user