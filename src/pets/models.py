from django.db import models

# Create your models here.


from django.db import models

# Create your models here.

class Pet(models.model):
    class PetType(models.TextChoices):
        DOG = 'DOG', 'Dog'
        CAT = 'CAT', 'Cat'
        BIRD = 'BIRD', 'Bird'
        RABBIT = 'RABBIT', 'Rabbit'
        FISH = 'FISH', 'Fish'
        REPTILE = 'REPTILE', 'Reptile'
        OTHER = 'OTHER', 'Other'
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=6, choices=PetType.choices, default=PetType.OTHER)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='pets', blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    breed = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='pets/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_in_shelter = models.BooleanField(default=False)
    is_adopted = models.BooleanField(default=False)
    is_rescue = models.BooleanField(default=False)
    is_looking_for_owner = models.BooleanField(default=False)
    is_looking_for_shelter = models.BooleanField(default=False)
    location = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return self.name
    
    
class Shelter(models.model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField()
    image = models.ImageField(upload_to='shelters/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pets = models.ManyToManyField(Pet, related_name='shelters')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_verified = models.BooleanField(default=False)
    is_open = models.BooleanField(default=False)
    schelude_open = models.TimeField()
    schelude_close = models.TimeField()
    is_emergency = models.BooleanField(default=False)
    have_vet = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    
class Adoption(models.model):
    class AdoptionStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        CANCELLED = 'CANCELLED', 'Cancelled'
        
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE)
    adopter = models.ForeignKey('users.User', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=AdoptionStatus.choices, default=AdoptionStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # TODO: create a function to generate a pdf with the information of the adoption
    def __str__(self):
        return f'{self.adopter} - {self.pet}'
    

class Event(models.model):
    class EventType(models.TextChoices):
        ADOPTION = 'ADOPTION', 'Adoption'
        FUNDRAISING = 'FUNDRAISING', 'Fundraising'
        MEETING = 'MEETING', 'Meeting'
        OTHER = 'OTHER', 'Other'
        
    name = models.CharField(max_length=100)
    description = models.TextField()
    from_date = models.DateField()
    from_time = models.TimeField()
    to_date = models.DateField()
    to_time = models.TimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=11, choices=EventType.choices, default=EventType.OTHER)
    is_payment_required = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # TODO: Create a function to develop a image with the information of event