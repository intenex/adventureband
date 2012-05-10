from django.db import models
from django.contrib.auth.models import User

# Note - use South (south.aeracode.org) to reliably migrate your database changes. Strange that Django can't do this on its own
# Note - if you want to change the *type* of a column (e.g. from CharField to IntegerField) first create a migration that deletes the old column and then another migration to create the new column

class Character(models.Model):
    CHAR_CHOICES = (
        ('W', 'Warrior'),
        ('M', 'Mage'),
        ('R', 'Rogue'),
    )
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    RACE_CHOICES = (
        ('H', 'Human'),
        ('E', 'Elf'),
        ('D', 'Dwarf'),
    )

    user = models.ForeignKey(User)
    name = models.CharField(max_length=20, blank=False)
    name_lower = models.CharField(max_length=20, blank=False) # used for case-insensitive prevention of duplicate character names while preserving user-defined casing of the character name
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=False, default='M')
    race = models.CharField(max_length=1, choices=RACE_CHOICES, blank=False, default='E')
    char_class = models.CharField(max_length=1, choices=CHAR_CHOICES, verbose_name='class', blank=False, default='W')
    level = models.IntegerField()
    exp = models.IntegerField()
    strength = models.IntegerField()
    intelligence = models.IntegerField()
    wisdom = models.IntegerField()
    dexterity = models.IntegerField()
    constitution = models.IntegerField()
    charisma = models.IntegerField()
    current_hp = models.IntegerField()
    max_hp = models.IntegerField()
    gold = models.IntegerField()
    weapon = models.IntegerField(max_length=10,null=True) # don't use null=True on CharFields - use blank=True
    ranged = models.IntegerField(max_length=10,null=True) # changed these to be integers though - will map up each item id to an actual id
    body = models.IntegerField(max_length=10,null=True)
    left_finger = models.IntegerField(max_length=10,null=True)
    right_finger = models.IntegerField(max_length=10,null=True)
    shield = models.IntegerField(max_length=10,null=True)
    hands = models.IntegerField(max_length=10,null=True)
    head = models.IntegerField(max_length=10,null=True)
    feet = models.IntegerField(max_length=10,null=True)
    quiver = models.IntegerField(max_length=10,null=True)
    create_date = models.DateTimeField()
    first_time = models.BooleanField()
    dungeon = models.IntegerField()
    def __unicode__(self):
        return self.name # This specifies that if a 'Character' object is ever referenced, it will output the 'name' value of the object by default instead of a useless object instance id - hence given that 'character' is a QuerySet (tuple list) of 'Character' objects, printing 'character' or 'character.name' will output the same thing