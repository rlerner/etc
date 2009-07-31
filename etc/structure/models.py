from django.db import models
from django.contrib.localflavor.us import models as lfus

# Defines university structure regarding people and places.

class College(models.Model):
	"""The highest-level container for personnel structure"""
	name = models.CharField(max_length=100)
	abbreviation = models.CharField(max_length=10)
	
	def __unicode__(self):
		return u"%s" % self.name
	
	# add uppercase conversion to save method
	def save(self, *args, **kwargs):
		self.abbreviation = self.abbreviation.upper()
		super(College, self).save(*args, **kwargs)
	
	class Meta:
		ordering = ('name',)
		db_table = 'structure_college'

class Department(models.Model):
	"""A level-two container for personnel structure"""
	name = models.CharField(max_length=100)
	college = models.ForeignKey(College)
	
	def __unicode__(self):
		return u"%s" % self.name
	
	class Meta:
		ordering = ('name', 'college',)
		db_table = 'structure_department'

class SubDepartment(models.Model):
	"""A level-three container for personnel structure"""
	name = models.CharField(max_length=100)
	department = models.ForeignKey(Department)
	
	def __unicode__(self):
		return u"%s" % self.name
	
	class Meta:
		ordering = ('department', 'name',)
		db_table = 'structure_subdepartment'

class Campus(models.Model):
	"""A top-level container for building structure"""
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	state = lfus.USStateField()
	zip_code = models.CharField(max_length=9)
	country = models.CharField(max_length=50, default='United States')
	phone = lfus.PhoneNumberField()
	
	def __unicode__(self):
		return u"%s" % self.name
	
	class Meta:
		ordering = ('name',)
		verbose_name_plural = "campuses"
		db_table = 'structure_campus'

class Building(models.Model):
	"""A level-two container for building structure"""
	name = models.CharField(max_length=100)
	abbreviation = models.CharField(max_length=20, blank=True, unique=True)
	campus = models.ForeignKey(Campus)
	
	class Meta:
		ordering = ('campus', 'name',)
		db_table = 'structure_building'
	
	def save(self, *args, **kwargs):
		if not self.abbreviation:
			self.abbreviation = self.name.split()[0]
		super(Building, self).save(*args, **kwargs)
	
	def __unicode__(self):
		return u"%s" % self.name