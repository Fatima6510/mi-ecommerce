from django.shortcuts import render, Http404, redirect
from .models import Producto, Categoria, Marca, Banner
import urllib.parse

def home(request):
    banners_query = Banner.objects.all().order_by('orden')
    banners_list = list(banners_query)

    if banners_list:
        banners_final = banners_list + [banners_list[0]]
    else:
        banners_final = []

    return render(request, 'tienda/index.html', {
        'banners': banners_final, 
        'destacados': Producto.objects.filter(destacado=True).order_by('orden'),
        'todos_los_productos': Producto.objects.all().order_by('orden')[:12],
        'marcas': Marca.objects.all().order_by('orden'),
        'categorias': Categoria.objects.all().order_by('orden'),
        'menu_lateral': Categoria.objects.all().prefetch_related('subcategorias').order_by('orden'),
    })

def lista_productos(request, slug=None):
    query = request.GET.get('q')
    marcas_seleccionadas = request.GET.getlist('marca') 
    sub_filtro = request.GET.get('sub')
    
    productos = Producto.objects.all().order_by('orden')
    titulo = "Todos los Productos"

    if slug:
        cat = Categoria.objects.get(slug=slug)
        productos = productos.filter(categoria=cat)
        titulo = cat.nombre
    elif sub_filtro:
        productos = productos.filter(subcategoria__nombre=sub_filtro)
        titulo = sub_filtro   
    marcas_ids = productos.values_list('marca_id', flat=True).distinct()
    marcas_disponibles = Marca.objects.filter(id__in=marcas_ids).order_by('nombre')

    if marcas_seleccionadas:
        productos = productos.filter(marca__nombre__in=marcas_seleccionadas)
        titulo = f"Filtro: {', '.join(marcas_seleccionadas)}"
    
    if query:
        productos = productos.filter(nombre__icontains=query)

    return render(request, 'tienda/lista_productos.html', {
        'productos': productos,
        'titulo': titulo,
        'marcas_filtro': marcas_disponibles,
        'marcas_active': marcas_seleccionadas, 
        'menu_lateral': Categoria.objects.all().prefetch_related('subcategorias'),
    })

def detalle_producto(request, id):
    p = Producto.objects.prefetch_related('imagenes').filter(id=id).first()
    if not p: raise Http404()
    return render(request, 'tienda/detalle_producto.html', {
        'p': p,
        'menu_lateral': Categoria.objects.all().prefetch_related('subcategorias').order_by('orden'),
    })

# --- CARRITO ---
def añadir_al_carrito(request, id):
    carrito = request.session.get('carrito', {})
    if not isinstance(carrito, dict): carrito = {}
    id_s = str(id)
    carrito[id_s] = carrito.get(id_s, 0) + 1
    request.session['carrito'] = carrito
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def restar_del_carrito(request, id):
    carrito = request.session.get('carrito', {})
    id_s = str(id)
    if id_s in carrito:
        carrito[id_s] -= 1
        if carrito[id_s] <= 0: del carrito[id_s]
    request.session['carrito'] = carrito
    return redirect('ver_carrito')

def eliminar_del_carrito(request, id):
    carrito = request.session.get('carrito', {})
    if str(id) in carrito: del carrito[str(id)]
    request.session['carrito'] = carrito
    return redirect('ver_carrito')

def ver_carrito(request):
    carrito_dict = request.session.get('carrito', {})
    productos_carrito = []
    total = 0
    mensaje = "Hola TECH SHOP! Me gustaría consultar sobre este pedido:\n\n"

    for p_id, cantidad in carrito_dict.items():
        p = Producto.objects.filter(id=p_id).first()
        if p:
            subtotal = p.precio * cantidad
            total += subtotal
            #se agrega el mensaje mas los productos
            mensaje += f"• {p.nombre} (x{cantidad}) - Gs {int(subtotal):,}\n".replace(',', '.')
            
            productos_carrito.append({
                'info': p,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
    
    mensaje += f"\n*TOTAL ESTIMADO: Gs {int(total):,}\n*".replace(',', '.')
    
    # Se convierte el texto a un formato que entienda el navegador
    mensaje_url = urllib.parse.quote(mensaje)
    whatsapp_link = f"https://wa.me/595994324702?text={mensaje_url}"

    return render(request, 'tienda/carrito.html', {
        'carrito': productos_carrito,
        'total': total,
        'whatsapp_url': whatsapp_link,
        'menu_lateral': Categoria.objects.all().prefetch_related('subcategorias')
    })

def vaciar_carrito(request):
    request.session['carrito'] = {}
    return redirect('ver_carrito')