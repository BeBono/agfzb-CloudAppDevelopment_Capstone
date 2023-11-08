from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    Name = models.CharField(blank=False, max_length=100)
    Description = models.CharField(blank=False, max_length=50)   

    # Create a toString method for object string representation
    def __str__(self):
        return self.Name + ": " + self.Description  




# <HINT> Create a Car Model model `class CarModel(models.Model):`:

class CarModel(models.Model):
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# Note: En Python, la sangría es fundamental, ya que define los bloques de código. En tu modelo CarModel, parece que estás intentando definir las opciones de TYPE_CHOICES con sangría incorrecta. Debe estar al mismo nivel de sangría que el resto del código en la clase.
    
# - Name  
        Name = models.CharField(blank=False, max_length=100)

# - Dealer id, used to refer a dealer created in cloudant database
        Dealer_id = models.CharField(blank=False, max_length=50) 

# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
   
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
        types = models.CharField(
            null=False,
            max_length=20,
            choices=TYPE_CHOICES,
            default=SEDAN
        )

    # - Year (DateField) 
        Year = models.DateField(null=True)
   

    # Create a toString method for object string representation
    # def __str__(self):
        # return "Name: " + self.first_name + ", " + \
        #        "Dealer_id: " + self.last_name + ", " + \
        #        "Car types: " + self.types + ", " + \
        #        "Total Learners: " + str(self.total_learners)


 



# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
