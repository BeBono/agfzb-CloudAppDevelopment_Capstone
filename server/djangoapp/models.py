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
    # myCampo = models.CharField(blank=True, max_length=60)
    
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


 

# <HINT> Create a plain Python class `CarDealer` and 'DealerReview' to hold dealer data.
# Note that this is a plain Python class instead of a subclass of Django model.
# Parece que la intención es tener una clase simple para almacenar temporalmente datos 
# extraídos de la base de datos (from Cloudant) y mostrarlos en la interfaz de usuario, 
# sin necesidad de persistir esos datos en la base de datos mediante migraciones de Django.

# Also the 'Class CarDealer' data (is like a template) are used in resapis.py to retrive this data from there.
# The CarDealer() in resapis.py is one instance of this class:

class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer myfull_name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
# Also the 'Class DealerReview' data are used in resapis.py to retrive this data from there

class DealerReview:

    # def __init__(self, id, name, dealership, review, purchase, purchase_date, car_make, car_model, car_year, sentiment):
    def __init__(self, id, name, dealership, review, purchase, purchase_date, car_make, car_model, car_year):
        # Dealer address
        self.id = id
        # Dealer city
        self.name = name
        # Dealer Full Name
        self.dealership = dealership
        # Dealer id
        self.review = review
        # Location lat
        self.purchase = purchase
        # Location long
        self.purchase_date = purchase_date
        # Dealer short name
        self.car_make = car_make
        # Dealer state
        self.car_model = car_model
        # Dealer zip
        self.car_year = car_year
        # Sentiment from NLU by IBM Cloud service (No implemented like atribute by instructions of Staff lab)
        # self.sentiment = sentiment

    def __str__(self):
        return "Dealer review: " + self.review
