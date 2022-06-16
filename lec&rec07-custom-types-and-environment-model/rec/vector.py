import operator 
import functools
import math
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):
	CANNOT_NORMALIZE_ZERO_VECTOR_MSG = "Cannot normalize the zero vector"
	#Initialize a vector with an array of coordinates
	def __init__(self, coordinates):
		try:
			if not coordinates:
				raise ValueError
			self.__coordinates = tuple([Decimal(x) for x in coordinates])
			self.__dimension = len(coordinates)

		except ValueError:
			raise ValueError('The coordinates must be non-empty')
		except TypeError:
			raise TypeError('The coordinates must be an iterable')

	@property
	def coordinates(self):
		return self.__coordinates

	@property
	def dimension(self):
		return self.__dimension

	def __str__(self):
		return 'Vector: {}'.format(self.coordinates)

	def __eq__(self, v):
		return self._coordinates == v.coordinates

	def __add__(self, v):
		if not v.dimension == self.__dimension:
			raise ValueError('Dimension of the vectors must be the same to perform an addition')
		return Vector(tuple(map(operator.add, self.__coordinates, v.coordinates)))

	# Vector subtraction. Subtract <v> from <self>
	def __sub__(self,v):	
		if not v.dimension == self.__dimension:
			raise ValueError('Dimension of the vectors must be the same to perform an addition')
		return Vector(tuple(map(operator.sub, self.__coordinates, v.coordinates)))


	def __getitem__(self, i):
		"""
		Get <i>-th entry of the current vector
		"""
		pass

	def __setitem__(self, i, x):
		"""
		Set <i>-th entry of the current vector to <x>
		"""
		pass


	# Entry-wise multiplication. Scale every entry by <scalar> 
	def multiply(self, scalar):
		return Vector(tuple(e * Decimal(scalar) for e in self.__coordinates))

	
	def m(self):
		"""
		Returns the magnitude of the vector
		"""
		return math.sqrt(sum( i*i for i in self.__coordinates))

	
	def normalize(self):
		"""
		Returns the direction vector/normalize bector
		"""
		try:
			m = self.m()
			return self.multiply(Decimal('1.0')/Decimal(m))

		except ZeroDivisionError:
			raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)

	def dot(self, v):
		c = [i for i in self.__coordinates]
		e = [j for j in v.__coordinates]
		return sum([a*b for a,b in zip(c,e)])

	def angle_with(self,v, in_degrees=False):
		try:
			u1 = self.normalize()
			u2 = v.normalize()
			angle_in_radians = math.acos(u1.dot(u2)) #arccosine of dot product

			if in_degrees:
				degrees_per_radian = 180./math.pi
				return angle_in_radians * degrees_per_radian
			else:
				return angle_in_radians

		except Exception as e:
			if(str(e))==self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
				raise Exception('Cannot compute an angle with the zero vector')
			else:
				raise e

	# Projection compenent of <self> onto vector <b>
	def proj(self, b):
		# magni(proj_b(v)) = dot(v, b_unit)
		scal = self.dot(b.normalize())
		return b.normalize().multiply(scal)

	# Component of <self> orthogonal to <b>
	def ortho(self, b):
		return self - self.proj(b)




