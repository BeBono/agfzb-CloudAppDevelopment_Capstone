from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here:
# Aquí se registran los modelos/tablas a las que se les cargarán los datos, desde la interfaz de adminitrador



# CarModelInline class:
# admin.StackedInline es una clase para listar repetidas veces un modelo/tabla. En este caso, se define
# la tabla llamada 'CarModel' que contiene modelos. Posteriormente se integraá como parte del modelo/tabla 
# CarMake (Marca de Carro). Es decir, al crear una nueva marca (modelo CarMake) se tendrá una lista de 
# modelos en "CarModel" que están previamente definidas en modeles.py.
class CarModel_Inline(admin.StackedInline):
    model = CarModel


# CarModelAdmin class:
# admin.ModelAdmin es una clase para customizar el modelo. En este caso, el modelo contiene 4 fields
# pero estamos seleccionando 3.
class CarModel_Admin(admin.ModelAdmin):
    fields = ['Name','Dealer_id','type','year']


# CarMakeAdmin class with CarModelInline:
# Aquí, además de seleccionar los campos para el modelo/tabla creación de marca, estamos integrando los modelos.
# Es decir, durante la creación de una nueva marca (modelo CarMake) se tendrá una lista de modelos 
# proveniente de "CarModel"  (que están previamente definidas en modeles.py). Esta se desplegará repetidas 
# veces, ya que una marca puede manejar varios modelos. 
class CarMake_Admin(admin.ModelAdmin):
     fields = ['Name','Description']
     inlines = [CarModel_Inline]


# Register models here:
# Requisito: Aquí se nombran tanto los modelos originales importados de models.py al comienzo de este archivo, como los modelos 
# personalizdos creados en este mismo archivo, de decir "arMake_Admin" y "arModel_Admin". 
admin.site.register(CarModel, CarModel_Admin)
admin.site.register(CarMake, CarMake_Admin)

# Notas adicoinales:

# * No se debería crear un modelo solo con el modelo/tabla CarModel (Sin definir la marca), pero igual funciona para cargar modelos de carros en la base de datos.

# * Cabe anotar que los datos ingresados se verán reflejados en la base de datos, en este caso la de PostgreSQL

# * Cualquier modificación en model.py, por ejemplo, en los campos, deberá ser migrada(reflejada) en la base de datos, 
# de lo contratio se perderá la coincidencia entre los nombres de los campos y arrojará error. 