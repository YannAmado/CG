import glm

def PrintMatrix(M):
	for i in range(4):
		for j in range(4):
			print(M[i][j], end=" ")
		print()

def TranslationMatrix():
	print()
	print("==================")
	print("Translation Matrix")
	print("==================")
	

	Position = glm.vec4(10, 10, 10, 1 )
	Direction = glm.vec4(10, 10, 10, 0 )
	Translate = glm.vec3(10, 10, 10 )
	Translation = glm.translate(glm.identity<glm.mat4>(), Translate);

	PrintMatrix(Translation)

	print()
	Position = Translation * Position
	Direction = Translation * Direction
	print(glm.to_string(Position))
	print(glm.to_string(Direction))



def RotationMatrix():

	print()
	print("==================")
	print("Rotation Matrix")
	print("==================")

	Position = glm.vec4( 100, 0, 0, 1 )
	Direction = glm.vec4( 100, 0, 0, 0 )
	Axis = glm.vec3( 0, 0, 1 )
	Rotation = glm.rotate(glm.identity<glm.mat4>(), glm.radians(90.0), Axis)

	PrintMatrix(Rotation)

	print()
	Position = Rotation * Position
	Direction = Rotation * Direction
	print(glm.to_string(Position))
	print(glm.to_string(Direction))


def ScaleMatrix():
	print()
	print("==================")
	print("Scale Matrix")
	print("==================")


	Position = glm.vec4( 100, 0, 0, 1 )
	Direction = glm.vec4( 100, 100, 0, 0 )
	ScaleAmount = glm.vec3( 2, 2, 2 )
	Scale = glm.scale(glm.identity<glm.mat4>(), ScaleAmount)

	PrintMatrix(Scale)

	print()
	Position = Scale * Position
	Direction = Scale * Direction
	print(glm.to_string(Position))
	print(glm.to_string(Direction))


def ComposedMatrix():
	print()
	print("==================")
	print("Composed Matrix")
	print("==================")

	Position = glm.vec4( 1, 1, 0, 1 )
	Direction = glm.vec4( 1, 1, 0, 0)

	Translate = glm.vec3( 0, 10, 0 )
	Translation = glm.translate(glm.identity<glm.mat4>(), Translate)

	Axis = glm.vec3( 0, 0, 1 )
	Rotation = glm.rotate(glm.identity<glm.mat4>(), glm.radians(45.0), Axis)

	ScaleAmount = glm.vec3( 2, 2, 0 )
	Scale = glm.scale(glm.identity<glm.mat4>(), ScaleAmount)

	print("Translation")
	PrintMatrix(Translation)
	print()

	print("Rotation")
	PrintMatrix(Rotation)
	print()

	print("Scale")
	PrintMatrix(Scale)
	print()

	Transform = Translation * Rotation * Scale
	
	print("Transform")
	PrintMatrix(Transform)
	print()

	Position = Transform * Position
	Direction = Transform * Direction

	print()
	print(glm.to_string(Position))
	print(glm.to_string(Direction))



def ModelViewProjection():
	print()
	print("==================")
	print("Model, View and Projection")
	print("==================")


	# Model é a matriz formada pelas transformações de Escala, Rotação e Translação!
	Model = glm.identity<glm.mat4>()

	# View
	Eye = glm.vec3( 0.0, 0.0, 10.0 )
	Center = glm.vec3(0.0, 0.0, 0.0 )
	Up = glm.vec3( 0.0, 1.0, 0.0 )
	View = glm.lookAt(Eye, Center, Up)

	print("View")
	PrintMatrix(View)

	FoV = glm.radians(45.0)
	AspectRatio = 800.0 / 600.0
	Near = 0.001
	Far = 1000.0
	Projection = glm.perspective(FoV, AspectRatio, Near, Far)

	print("View")
	PrintMatrix(Projection)

	ModelViewProjection = Projection * View * Model

	print("ModelViewProjection")
	PrintMatrix(ModelViewProjection)


def main():
	TranslationMatrix()
	RotationMatrix()
	ScaleMatrix()
	ComposedMatrix()
	ModelViewProjection()
