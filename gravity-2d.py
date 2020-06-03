import math, numpy
import matplotlib.pyplot as plt
from scipy.constants import G

class Vector2D:
	def __init__(self, x, y):
		self.vector = numpy.array([x, y])

	def mult_vector(self, position):
		return Vector2D(self.vector[0]*position.vector[0], self.vector[1]*position.vector[1])

	def dev_vector(self, position):
		return Vector2D(self.vector[0]/position.vector[0], self.vector[1]/position.vector[1])

	def add_vector(self, position):
		return Vector2D(self.vector[0]+position.vector[0], self.vector[1]+position.vector[1])

	def subtract_vector(self, position):
		return Vector2D(self.vector[0]-position.vector[0], self.vector[1]-position.vector[1])

	def get_length(self):
		return math.sqrt(self.vector[0]**2+self.vector[1]**2)

	def get_normalized_vector(self):
		if self.get_length() == 0:
			return Vector2D(0.0, 0.0)
		return Vector2D(self.vector[0]/self.get_length(), self.vector[1]/self.get_length())

	def print(self):
		print("x: ", self.vector[0], " y: ", self.vector[1])

class Body:
	def __init__(self, position_vector, velocity_vector, mass, radius):
		self.position_vector = position_vector
		self.velocity_vector = velocity_vector
		self.mass = mass
		self.radius = radius

	def get_velocity(self):
		return self.velocity_vector.get_length()

	def calculate_force(self, other):
		return -(G*self.mass*other.mass)/self.position_vector.subtract_vector(other.position_vector).get_length()**2

	def update_velocity_vector(self, other):
		force = self.calculate_force(other)
		self.velocity_vector = self.velocity_vector.add_vector(
			Vector2D(force, force).mult_vector(self.position_vector.subtract_vector(other.position_vector).get_normalized_vector().dev_vector(Vector2D(self.mass, self.mass)))
			)

	def update_position_vector(self):
		self.position_vector = self.position_vector.add_vector(self.velocity_vector)


class System:
	def __init__(self, bodies):
		self.bodies = bodies

	def update(self):
		updated_system = System([])
		for primary_body in self.bodies:
			for secondary_body in self.bodies:
				if primary_body is not secondary_body:
					primary_body.update_velocity_vector(secondary_body)
					primary_body.update_position_vector()

	def plot(self, cycles):
		cycle_values = []
		for i in range(cycles):
			cycle_values.append([])
			for body in self.bodies:
				cycle_values[-1].append(body.position_vector)
			system.update()
		for i, body in enumerate(self.bodies):
			plt.plot([i.vector[0] for i in [cycle[i] for cycle in cycle_values]], [i.vector[1] for i in [cycle[i] for cycle in cycle_values]])
		plt.ylabel('y-axis')
		plt.xlabel('x-axis')
		plt.show()


configurations = [
	[
	Body(Vector2D(0.0, 0.0), Vector2D(0, 0), 10**13, 0),
	Body(Vector2D(100.0, 0.0), Vector2D(-.4, 2.4), 10**11, 0),
	Body(Vector2D(-100.0, 0.0), Vector2D(.4, -2.4), 10**2, 0),
	],
	[
	Body(Vector2D(0.0, 0.0), Vector2D(0, 0), 10**13, 0),
	Body(Vector2D(100.0, 0.0), Vector2D(-.4, 2.4), 10**5, 0),
	Body(Vector2D(-100.0, 0.0), Vector2D(.4, -2.4), 10**2, 0),
	],
	[
	Body(Vector2D(0.0, 0.0), Vector2D(0, 0), 10**13, 0),
	Body(Vector2D(100.0, 0.0), Vector2D(-.4, 2.4), 10**5, 0),
	Body(Vector2D(-200.0, 0.0), Vector2D(1.0, -.5), 10**5, 0),
	]
]

system = System(configurations[2])
system.plot(10000)
