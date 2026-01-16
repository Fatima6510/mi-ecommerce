from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    icono = models.CharField(max_length=50) 
    imagen_url = models.URLField()
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
    imagen_url = models.URLField()
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
    imagen_url = models.URLField()
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
    imagen_url = models.URLField(help_text="URL de la imagen adicional")
    orden = models.IntegerField(default=0)

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"