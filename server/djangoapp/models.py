from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=100) # Name of the car maker
    description = models.TextField(blank=True) # Description of the car maker
    founder = models.CharField(max_length=100) # Name of the car maker founder
    date_founded = models.DateField() # Year the car maker was founded

    def __str__(self):
        return f'Name: {self.name}\nDescription:{self.description}\nFounder:{self.founder}\nDate Founded:{self.date_founded}'

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dealer_id = models.IntegerField()

    type_choice = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('VAN', 'Van')
    ]
    car_type = models.CharField(max_length=10, choices=type_choice)
    year = models.DateField()

    def __str__(self):
        return f'Name: {self.name}\nCar Make: {self.car_make}\nType: {self.car_type}\nYear: {self.year}'

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
