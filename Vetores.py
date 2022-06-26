
#define GLM_FORCE_SWIZZLE
import glm


def Constructors():

	print()
	Point1 = glm.vec3(10.0, 0.0, 0.0)
	Point2 = glm.vec3(10.0, 0.0, 0.0)
	Point3 = glm.vec3(10.0, 0.0, 0.0)

	print(f"Point1: {Point1}")
	print(f"Point2: {Point2}")
	print(f"Point3: {Point3}")


def Components():

	print()
	Point1 = glm.vec3(10.0, 10.0, 0.0)
	print(f"X: {Point1.x} Y: {Point1.y} Z: {Point1.z}")
	print(f"R: {Point1.r} G: {Point1.g} B: {Point1.b}")
	print(f"S: {Point1.s} T: {Point1.t} P: {Point1.p}")
	print(f"0: {Point1[0]} Y: {Point1[1]} 2: {Point1[2]}")


def Swizzles():
	# Precisa definir GLM_SWIZZLE

	print()
	Point1 = glm.vec3(10.0, 10.0, 0.0)
	Point2 = Point1.xxx
	Point3 = Point1.bgr
	Point4 = Point1.bbbb
	print(f"Point1: {Point1}")
	print(f"Point2: {Point2}")
	print(f"Point3: {Point3}")
	print(f"Point4: {Point4}")


def Operations():
	Point1 = glm.vec3(10.0, 10.0, 0.0)
	Point2 = glm.vec3(10.0, 10.0, 10.0)

	# Soma
	Point3 = Point1 + Point2
	Point4 = Point1 - Point2

	# Scala
	Point5 = Point1 * 10.0
	Point6 = Point1 / 10.0

	# Comprimento
	L = glm.length(Point1)
	# Nao confundir com a funcao membro length
	C = Point1.length()

	# Norma
	Norm = glm.normalize(Point1)

	# Dot product
	Dot = glm.dot(Point1, Point2)

	# Cross product
	Cross = glm.cross(Point1, Point2)

	# Distance
	Distance = glm.distance(Point1, Point2)

	# Refract
	Refract = glm.refract(Point1, Norm, 1.0)

	# Reflect
	Reflect = glm.reflect(Point1, Norm)


def main():
	Constructors()
	Components()
	Swizzles()
	Operations()