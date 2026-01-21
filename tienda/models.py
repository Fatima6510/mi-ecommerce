from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    icono = models.CharField(max_length=50) 
    imagen = models.ImageField(upload_to='categorias/', null=True, blank=True)
    slug = models.SlugField(unique=True)
    orden = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class Subcategoria(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='subcategorias')
    orden = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.categoria.nombre} > {self.nombre}"

class Marca(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='marcas/', null=True, blank=True) 
    orden = models.IntegerField(default=0) 

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    STOCK_CHOICES = [
        ('disponible', 'Disponible'),
        ('agotado', 'Agotado'),
        ('consulta', 'Bajo Consulta'),
    ]

    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=100, decimal_places=3) 
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    tag = models.CharField(max_length=50, blank=True, help_text="Ej: NUEVO")
    destacado = models.BooleanField(default=False)
    stock = models.CharField(max_length=20, choices=STOCK_CHOICES, default='disponible')
    orden = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/galeria/')
    orden = models.IntegerField(default=0)

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"

class Banner(models.Model):
    texto_blanco = models.CharField("Texto en Blanco", max_length=100)
    texto_rojo = models.CharField("Texto en Rojo", max_length=100)
    imagen = models.ImageField("Imagen de fondo", upload_to='banners/')
    link_url = models.CharField("Enlace (URL)", max_length=200, help_text="Ej: /productos/categoria/gaming/", default="/productos/")
    orden = models.IntegerField("Posición", default=0)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.texto_blanco} {self.texto_rojo}"