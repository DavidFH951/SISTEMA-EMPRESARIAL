from django.db import models

# 1. Refleja tu pestaña "UBICACIONES"
class Ubicacion(models.Model):
    TIPO_CHOICES = (
        ('almacen', 'Almacén'),
        ('tienda', 'Tienda'),
        ('tecnico', 'Técnico'),
        ('proveedor', 'Proveedor'),
    )
    # Ej: ALM-OF, TDA, TEC-LEO
    id_ubicacion = models.CharField(max_length=20, unique=True, verbose_name="ID Ubicación")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    nombre = models.CharField(max_length=100) # Ej: Almacén Oficina, OXXO El Polo

    def __str__(self):
        return f"{self.id_ubicacion} - {self.nombre}"

# 2. Refleja tu pestaña "ACTIVOS"
class Activo(models.Model):
    ESTADO_CHOICES = (
        ('FUNCIONA', 'FUNCIONA'),
        ('NO FUNCIONA', 'NO FUNCIONA'),
    )
    # Ej: I-0001
    codigo_interno = models.CharField(max_length=20, unique=True)
    tipo_equipo = models.CharField(max_length=50) # Ej: Impresora, Modem
    marca = models.CharField(max_length=50) # Ej: EPSON
    n_serie = models.CharField(max_length=100, unique=True, verbose_name="N° de Serie")
    
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='FUNCIONA')
    observacion = models.TextField(blank=True, null=True)
    
    # Esto reemplaza a "FECHA_DE_ULTIMA_UBICACION" y "ULTIMA_UBICACION"
    ubicacion_actual = models.ForeignKey(Ubicacion, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_ultima_ubicacion = models.DateField(auto_now=True)
    
    disponibilidad = models.CharField(max_length=20, default='DISPONIBLE')

    def __str__(self):
        return f"{self.tipo_equipo} {self.marca} - SN: {self.n_serie}"

# 3. Refleja tu pestaña "MOVIMIENTOS" (Registro automático)
class Movimiento(models.Model):
    TIPO_MOV = (
        ('Ingreso', 'Ingreso'),
        ('Traslado', 'Traslado'),
        ('Recojo', 'Recojo'),
    )
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    
    desde = models.ForeignKey(Ubicacion, related_name='movimientos_salida', on_delete=models.SET_NULL, null=True)
    hacia = models.ForeignKey(Ubicacion, related_name='movimientos_entrada', on_delete=models.SET_NULL, null=True)
    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_MOV)
    
    ticket = models.CharField(max_length=20, blank=True, null=True) # Ej: 0-00001
    observacion = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        # LÓGICA AUTOMÁTICA: Al guardar un movimiento, el activo cambia de ubicación instantáneamente
        if self.hacia:
            self.activo.ubicacion_actual = self.hacia
            # Si va a una tienda (TDA), deja de estar disponible en almacén
            if self.hacia.tipo == 'tienda':
                self.activo.disponibilidad = 'NO DISPONIBLE'
            elif self.hacia.tipo == 'almacen':
                self.activo.disponibilidad = 'DISPONIBLE'
            self.activo.save()
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.activo.n_serie} hacia {self.hacia}"