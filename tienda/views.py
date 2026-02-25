from django.shortcuts import render, Http404, redirect, get_object_or_404
from .models import Producto, Categoria, Marca, Banner, PromoBanner
import urllib.parse
from django.contrib import messages

def home(request):
    banners_db = list(Banner.objects.all().order_by('orden'))
    if banners_db:
        banners_final = banners_db + [banners_db[0]]
    else:
        banners_final = []

    promos_query = PromoBanner.objects.filter(activo=True).order_by('orden')
    promos_list = list(promos_query)
    
    if promos_list:
        promos_final = promos_list + [promos_list[0]]
    else:
        promos_final = []

    return render(request, 'tienda/index.html', {
        'banners': banners_final, 
        'destacados': Producto.objects.filter(destacado=True).order_by('orden'),
        'todos_los_productos': Producto.objects.all().order_by('orden')[:15],
        'marcas': Marca.objects.all().order_by('orden'),
        'categorias': Categoria.objects.all().order_by('orden'),
        'menu_lateral': Categoria.objects.all().prefetch_related('subcategorias').order_by('orden'),
        'promos': promos_final, 
    })

def lista_productos(request, slug=None):
    query = request.GET.get('q')
    marcas_seleccionadas = request.GET.getlist('marca') 
    sub_filtro = request.GET.get('sub')
    
    productos = Producto.objects.all().order_by('orden')
    titulo = "Todos los Productos"

    if slug:
        cat = get_object_or_404(Categoria, slug=slug)
        productos = productos.filter(categoria=cat)
        titulo = cat.nombre
    elif sub_filtro:
        productos = productos.filter(subcategoria__nombre=sub_filtro)
        titulo = sub_filtro   

    # Marcas dinámicas basadas en los productos que estamos viendo
    marcas_ids = productos.values_list('marca_id', flat=True).distinct()
    marcas_disponibles = Marca.objects.filter(id__in=marcas_ids).order_by('nombre')

    if marcas_seleccionadas:
        productos = productos.filter(marca__nombre__in=marcas_seleccionadas)
        titulo = f"Filtro: {', '.join(marcas_seleccionadas)}"
    
    if query:
        productos = productos.filter(nombre__icontains=query)
        titulo = f"Resultados para: '{query}'"

    return render(request, 'tienda/lista_productos.html', {
        'productos': productos,
        'titulo': titulo,
        'marcas_filtro': marcas_disponibles,
        'marcas_active': marcas_seleccionadas, 
        'menu_lateral': Categoria.objects.all().prefetch_related('subcategorias').order_by('orden'),
    })

def detalle_producto(request, id):
    p = Producto.objects.prefetch_related('imagenes').filter(id=id).first()
    if not p: 
        raise Http404()
    
    # Productos de la misma categoría para la sección "También te puede interesar"
    relacionados = Producto.objects.filter(categoria=p.categoria).exclude(id=p.id).order_by('?')[:5]

    return render(request, 'tienda/detalle_producto.html', {
        'p': p,
        'relacionados': relacionados,
        'menu_lateral': Categoria.objects.all().prefetch_related('subcategorias').order_by('orden'),
    })

# --- VISTAS DEL CARRITO ---

def añadir_al_carrito(request, id):
    p = get_object_or_404(Producto, id=id)
    carrito = request.session.get('carrito', {})
    if not isinstance(carrito, dict): 
        carrito = {}
    
    id_s = str(id)
    carrito[id_s] = carrito.get(id_s, 0) + 1
    request.session['carrito'] = carrito
    
    messages.success(request, f"{p.nombre} añadido al carrito.")
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
    if str(id) in carrito: 
        del carrito[str(id)]
    request.session['carrito'] = carrito
    return redirect('ver_carrito')

def ver_carrito(request):
    carrito_dict = request.session.get('carrito', {})
    productos_carrito = []
    total = 0
    mensaje = "Hola TECH SHOP! Me gustaría realizar este pedido:\n\n"

    for p_id, cantidad in carrito_dict.items():
        p = Producto.objects.filter(id=p_id).first()
        if p:
            subtotal = p.precio * cantidad
            total += subtotal
            # Formato de mensaje para WhatsApp con puntos de miles
            mensaje += f"• {p.nombre} (x{cantidad}) - Gs {int(subtotal):,}\n".replace(',', '.')
            
            productos_carrito.append({
                'info': p,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
    
    mensaje += f"\n*TOTAL ESTIMADO: Gs {int(total):,}*".replace(',', '.')
    
    mensaje_url = urllib.parse.quote(mensaje)
    # Link dinámico con el número
    whatsapp_link = f"https://wa.me/595994324702?text={mensaje_url}"

    return render(request, 'tienda/carrito.html', {
        'carrito': productos_carrito,
        'total': total,
        'whatsapp_url': whatsapp_link,
        'menu_lateral': Categoria.objects.all().prefetch_related('subcategorias').order_by('orden')
    })

def vaciar_carrito(request):
    request.session['carrito'] = {}
    return redirect('ver_carrito')

def ver_promo(request, slug):
    promo = get_object_or_404(PromoBanner, slug=slug)
    productos = promo.productos.all()
    
    return render(request, 'tienda/lista_productos.html', {
        'productos': productos,
        'titulo': f"{promo.titulo_blanco} {promo.titulo_rojo}",
        'menu_lateral': Categoria.objects.all().prefetch_related('subcategorias').order_by('orden')
    })