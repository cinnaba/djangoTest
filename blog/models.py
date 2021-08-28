from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=30)

    content = models.TextField()
    #hook_text는 요약문
    hook_text = models.CharField(max_length=40, blank=True)

    head_image = models.ImageField(upload_to='blog/images/%y/%m/%d/', blank='True')
    file_upload = models.FileField(upload_to='blog/files/%y/%m/%d/', blank='True')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.pk}]{self.title}'


    def get_absolute_url(self):
        return f'/blog/{self.pk}/'
