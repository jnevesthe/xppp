from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Video(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    video = CloudinaryField('video', resource_type='video')  # <<< importante!
    capa = CloudinaryField('image')  # só imagem
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    destaque = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        # gera o slug antes de salvar
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo



class TrafficLog(models.Model):
    ip = models.GenericIPAddressField()
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=200)  # URL acessada
    user_agent = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f"{self.ip} - {self.path} - {self.date}"
