from django.db import models
from django.utils.timezone import now


# Create your models here.

# 1. <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    Name = models.CharField(blank=False, max_length=50)
    Description = models.CharField(blank=False, max_length=50)  
    myCampo = models.CharField(blank=True, max_length=60)
    
    # Create a toString method for object string representation
    def __str__(self):
        return self.Name + ": " + self.Description  




# 2. <HINT> Create a Car Model model `class CarModel(models.Model):`:

class CarModel(models.Model):
# - Many-To-Many relationship to CarMake model/class (One CarMake has many Car Models).
# clarification:
# "Many-to-Many" entre CarMake y CarModel cumple con el requerimiento "One Car Make has many Car Models". 
# Cada instancia de CarMake puede estar asociada a múltiples instancias de CarModel, lo que significa que una marca de automóvil puede
# tener muchos modelos de automóviles. Esto satisface el requerimiento de que una marca de automóvil tenga varios modelos de automóviles:
        # makes = models.ManyToManyField(CarMake)

# Durante la creación de marcas, que incluyen modelos por defecto, fue necesario cambiar la relación 
# a Many-to-one utilizando el método 'ForeignKey'
        Makes = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)

# NOTA: Si se desea obtener una lista de modelos de automóviles asociados a una marca de vehículo específica, se podría de la siguiente manera:
#         car_make = CarMake.objects.get(id=1)  # Reemplazar 1 con el ID de la marca de vehículo que se desea consultar.
#         car_models = car_make.models.all()

# Note: En Python, la sangría es fundamental, ya que define los bloques de código. En tu modelo CarModel, parece que estás intentando definir las opciones de TYPE_CHOICES con sangría incorrecta. Debe estar al mismo nivel de sangría que el resto del código en la clase.
    
# - Name / Speciific car name # ASK CLARIFICATION ABOUT WHAT DOES MEAN THIS "name".  
        Name = models.CharField(blank=False, max_length=100)

# - Dealer_id, used to refer a dealer created in cloudant database
        Dealer_id = models.CharField(blank=False, max_length=50) 

# - Car_type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
   
    # Create the variables with the options:
        SEDAN = 'sedan'
        SUV = 'suv'
        WAGON = 'wagon'
        COUPE = 'coupe'
        MINIVAN = 'minivan'
        SPORTCAR = 'sportcar'
        CROSSOVER = 'crossover'

    # Create the options with variables:
        TYPE_CHOICES = [
            (SEDAN, 'Sedan'),
            (SUV, 'Suv'),
            (WAGON, 'Wagon'),
            (COUPE, 'Coupe'),
            (MINIVAN, 'Minivan'),
            (SPORTCAR, 'Sportcar'),
            (CROSSOVER, 'Crossover') 
        ]

    # types Char field with defined enumeration choices
        type = models.CharField(
            null=False,
            max_length=20,
            choices=TYPE_CHOICES,
            default=SEDAN
        )

# - Year (DateField) 
        year = models.DateField(null=True)
   

# Create a toString method for object string representation
        def __str__(self):
            return "Name: " + self.Name + ", " + \
                   "Dealer_id: " + self.Dealer_id + ", " + \
                   "Car_type: " + self.type + ", " + \
                   "Year: " + self.year.strftime("%Y")


 

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
