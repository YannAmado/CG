import glm
from OpenGL.GL import *
import OpenGL.GLUT
import glfw
import glew
import sys

from OpenGL.raw.GL._types import GLuint
from PIL import Image
import numpy as np

from Camera import SimpleCamera

#define STB_IMAGE_IMPLEMENTATION

Width = 800
Height = 600

class Vertex:
	def __init__(self, pos: glm.vec3, nor: glm.vec3, col: glm.vec3, uv: glm.vec2):
		self.Position = pos
		self.Normal = nor
		self.Color = col
		self.UV = uv

class Triangle:
	def __init__(self, v0:GLuint, v1:GLuint, v2:GLuint):
		self.V0 = v0
		self.V1 = v1
		self.V2 = v2


class DirectionalLight:
	def __init__(self, direc:glm.vec3, intensity:GLfloat):
		self.Direction = direc
		self.Intensity = intensity


Camera = SimpleCamera()

def GenerateSphere(Resolution:GLuint, Vertices, Indices):
	Vertices.clear()
	Indices.clear()

	Pi = glm.pi()
	TwoPi = glm.two_pi()
	InvResolution = 1.0/float(Resolution - 1)


	for i in range(Resolution):
		UIndex = GLuint(i)
		U = UIndex * InvResolution
		Theta = glm.mix(0.0, TwoPi, float(U))

		for j in range(Resolution):
			VIndex = GLuint(j)
			V = VIndex * InvResolution
			Phi = glm.mix(0.0, Pi, float(V))

			VertexPosition = glm.vec3(
				glm.cos(Theta) * glm.sin(Phi),
				glm.sin(Theta) * glm.sin(Phi),
				glm.cos(Phi)
			)

			VertexNormal = glm.normalize(VertexPosition)

			Vertices.append(Vertex(
				VertexPosition,
				VertexNormal,
				glm.vec3( 1.0, 1.0, 1.0 ),
				glm.vec2( 1.0 - U, 1.0 - V )
			))



	for i in range(Resolution-1):
		U = GLuint(i)
		for j in range(Resolution-1):
			V = GLuint(j)
			P0 = U + V * Resolution
			P1 = U + 1 + V * Resolution
			P2 = U + (V + 1) * Resolution
			P3 = U + 1 + (V + 1) * Resolution
			Indices.append(Triangle( P3, P2, P0 ))
			Indices.append(Triangle( P1, P3, P0 ))




def ReadFile(FilePath) -> str:
	f = open(FilePath, "r")
	return f.read()

		#	std::string FileContents;
	#if (std::ifstream FileStream{ FilePath, std::ios::in }):
#		FileContents.assign((std.istreambuf_iterator<char>(FileStream)), std.istreambuf_iterator<char>())



def CheckShader(ShaderId: GLuint):

	# Verificar se o shader foi compilado
	Result = glGetShaderiv(ShaderId, GL_COMPILE_STATUS)


	if Result == GL_FALSE:

		# Erro ao compilar o shader, imprimir o log para saber o que est� errado
		InfoLogLength = glGetShaderiv(ShaderId, GL_INFO_LOG_LENGTH)

		ShaderInfoLog(InfoLogLength, '\0')
		glGetShaderInfoLog(ShaderId, InfoLogLength, nullptr, &ShaderInfoLog[0])

		if InfoLogLength > 0:
			print("Erro no Vertex Shader:")
			print(ShaderInfoLog)


def LoadShaders(VertexShaderFile, FragmentShaderFile) ->GLuint:

	# Criar os identificadores de cada um dos shaders
	VertShaderId = glCreateShader(GL_VERTEX_SHADER)
	FragShaderId = glCreateShader(GL_FRAGMENT_SHADER)

	VertexShaderSource = ReadFile(VertexShaderFile)
	FragmentShaderSource = ReadFile(FragmentShaderFile)

	#assert(not VertexShaderSource.empty())
	#assert(not FragmentShaderSource.empty())


	print(f"Compilando {VertexShaderFile}")
	glShaderSource(VertShaderId, 1)
	glCompileShader(VertShaderId)
	CheckShader(VertShaderId)

	print(f"Compilando {FragmentShaderFile}")
	glShaderSource(FragShaderId)
	glCompileShader(FragShaderId)
	CheckShader(FragShaderId)

	print("Linkando Programa")
	ProgramId = glCreateProgram()
	glAttachShader(ProgramId, VertShaderId)
	glAttachShader(ProgramId, FragShaderId)
	glLinkProgram(ProgramId)

	# Verificar o programa
	Result = glGetProgramiv(ProgramId, GL_LINK_STATUS)
	
	if Result == GL_FALSE:
		InfoLogLength = glGetProgramiv(ProgramId, GL_INFO_LOG_LENGTH)

		if InfoLogLength > 0:

			ProgramInfoLog(InfoLogLength, '\0')
			glGetProgramInfoLog(ProgramId, InfoLogLength, nullptr, &ProgramInfoLog[0])

			print("Erro ao linkar o Programa")
			print(ProgramInfoLog)
			assert(False)



	glDetachShader(ProgramId, VertShaderId)
	glDetachShader(ProgramId, FragShaderId)

	glDeleteShader(VertShaderId)
	glDeleteShader(FragShaderId)

	return ProgramId


def LoadTexture(filename):
	img = Image.open(filename)
	img_data = np.array(list(img.getdata()), np.int8)
	texture_id = glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D, texture_id)

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
	glGenerateMipmap(GL_TEXTURE_2D)

	return texture_id


def MouseButtonCallback(Window, Button: int, Action: int, Modifiers: int):

	# std::cout << "Button: " << Button << " Action: " << Action << " Modifiers: " << Modifiers << std::endl;

	if Button == glfw.MOUSE_BUTTON_LEFT:

		if Action == glfw.PRESS:

			glfw.set_input_mode(Window, glfw.CURSOR, glfw.CURSOR_DISABLED)
			X, Y = glfw.get_cursor_pos(Window)
			Camera.PreviousCursor = glm.vec2(X,Y)
			Camera.bEnableMouseMovement = True

		elif Action == glfw.RELEASE:
			glfw.set_input_mode(Window, glfw.CURSOR, glfw.CURSOR_NORMAL)
			Camera.bEnableMouseMovement = False




def MouseMotionCallback(Window, X: float, Y: float):

	# std::cout << "X: " << X << " Y: " << Y << std::endl;
	Camera.MouseMove(X, Y)

def KeyCallback(Window, Key: int, ScanCode: int, Action: int, Modifers: int):
	# std::cout << "Key: " << Key << " ScanCode: " << ScanCode << " Action: " << Action << " Modifiers: " << Modifers << std::endl;

	if Action == glfw.PRESS:
		if Key == glfw.KEY_ESCAPE:
			glfw.set_window_should_close(Window, True)

		elif Key == glfw.KEY_W:
			Camera.MoveForward(1.0)

		elif Key == glfw.KEY_S:
			Camera.MoveForward(-1.0)

		elif Key == glfw.KEY_A:
			Camera.MoveRight(-1.0)

		elif Key == glfw.KEY_D:
			Camera.MoveRight(1.0)

	elif Action == glfw.RELEASE:
		if Key == glfw.KEY_ESCAPE:
			glfw.set_window_should_close(Window, True)

		elif Key == glfw.KEY_W:
			Camera.MoveForward(0.0)

		elif Key == glfw.KEY_S:
			Camera.MoveForward(0.0)

		elif Key == glfw.KEY_A:
			Camera.MoveRight(0.0)

		elif Key == glfw.KEY_D:
			Camera.MoveRight(0.0)




def main():
	if glfw.NOT_INITIALIZED:
		print("Erro ao inicializar o GLFW")
		return 1

	glfw.window_hint(glfw.DEPTH_BITS, 32)
	Window = glfw.create_window(Width, Height, "Blue Marble")

	if not Window:

		print("Erro ao criara a Janela")
		glfw.terminate()
		return 1

	glfw.set_mouse_button_callback(Window, MouseButtonCallback)
	glfw.set_cursor_pos_callback(Window, MouseMotionCallback)
	glfw.set_key_callback(Window, KeyCallback)

	glfw.make_context_current(Window)
	glfw.swap_interval(1)

	if glew.glewInit() != glew.GLEW_OK:
		print("Erro ao inicializar o GLEW")
		glfw.terminate()
		return 1


	GLMajorVersion = glGetIntegerv(GL_MAJOR_VERSION)
	GLMinorVersion = glGetIntegerv(GL_MINOR_VERSION)
	print(f"OpenGL Version   : {GLMajorVersion}.{GLMinorVersion}")
	print(f"OpenGL Vendor    : {glGetString(GL_VENDOR)}")
	print(f"OpenGL Renderer  : {glGetString(GL_RENDERER)}")
	print(f"OpenGL Veersion  : {glGetString(GL_VERSION)}")
	print(f"GLSL Version     : {glGetString(GL_SHADING_LANGUAGE_VERSION)}")


	# Habilita o Buffer de Profundidade
	glEnable(GL_DEPTH_TEST)

	# Escolhe a funcao de teste de profundidade.
	glDepthFunc(GL_ALWAYS)

	glDisable(GL_CULL_FACE)
	glEnable(GL_CULL_FACE)

	# Compilar o vertex e o fragment shader
	ProgramId = LoadShaders("shaders/triangle_vert.glsl", "shaders/triangle_frag.glsl")

	# Gera a Geometria da esfera e copia os dados para a GPU (mem�ria da placa de v�deo)
	SphereVertices = [Vertex()]
	SphereIndices = [Triangle(0,0,0)]
	GenerateSphere(100, SphereVertices, SphereIndices)

	SphereVertexBuffer = glGenBuffers(1)
	SphereElementBuffer = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, SphereVertexBuffer)
	glBufferData(GL_ARRAY_BUFFER, len(SphereVertices) *  sys.getsizeof(Vertex), SphereVertices.data(), GL_STATIC_DRAW)
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, SphereElementBuffer)
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(SphereIndices) *  sys.getsizeof(Triangle), SphereIndices.data(), GL_STATIC_DRAW)

	# Criar uma fonte de luz direcional
	Light = DirectionalLight(glm.vec3(0.0, 0.0, -1.0), 1.0)

	# Model View Projection
	ModelMatrix = glm.rotate(glm.identity<glm.mat4>(), glm.radians(90.0), glm.vec3(1.0, 0.0, 0.0 ))

	# Carregar a Textura para a Mem�ria de V�deo
	EarthTextureId = LoadTexture("textures/earth_2k.jpg")
	CloudsTextureId = LoadTexture("textures/earth_clouds_2k.jpg")

	# Configura a cor de fundo
	glClearColor(0.0, 0.0, 0.0, 1.0)

	# Identificador do Vertex Array Object (VAO)
	# Gerar o identificador do VAO
	SphereVAO = glGenVertexArrays(1)

	# Habilitar o VAO
	glBindVertexArray(SphereVAO)

	# Habilita o atributo na posi��o 0, normalmente � o atributo de v�rtices
	# Esse vai ser o identificador que vamos usar no shader para ler a posi��o
	# de cada v�rtice, mas n�o se preocupe com isso agora. Vai ficar tudo mais
	# claro quando formos falar de shaders
	glEnableVertexAttribArray(0)
	glEnableVertexAttribArray(1)
	glEnableVertexAttribArray(2)
	glEnableVertexAttribArray(3)

	# Diz para o OpenGL que o VertexBuffer vai ficar associado ao atributo 0
	# glBindBuffer(GL_ARRAY_BUFFER, VertexBuffer);
	glBindBuffer(GL_ARRAY_BUFFER, SphereVertexBuffer)
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, SphereElementBuffer)

	# Informa ao OpenGL onde, dentro do VertexBuffer, os v�rtices est�o. No
	# nosso caso o array Triangles � tudo o que a gente precisa
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sys.getsizeof(Vertex))
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_TRUE, sys.getsizeof(Vertex), reinterpret_cast<void*>(offsetof(Vertex, Normal)))
	glVertexAttribPointer(2, 3, GL_FLOAT, GL_TRUE, sys.getsizeof(Vertex), reinterpret_cast<void*>(offsetof(Vertex, Color)))
	glVertexAttribPointer(3, 2, GL_FLOAT, GL_FALSE, sys.getsizeof(Vertex), reinterpret_cast<void*>(offsetof(Vertex, UV)))

	# Disabilitar o VAO
	glBindVertexArray(0)

	PreviousTime = glfw.get_time()

	while not glfw.window_should_close(Window):
		CurrentTime = glfw.get_time()
		DeltaTime = CurrentTime - PreviousTime
		if DeltaTime > 0.0:
			Camera.Update(DeltaTime)
			PreviousTime = CurrentTime

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		glUseProgram(ProgramId)
		
		ViewMatrix = Camera.GetView()
		NormalMatrix = glm.transpose(glm.inverse(ViewMatrix * ModelMatrix))
		ModelViewMatrix = ViewMatrix * ModelMatrix
		ModelViewProjectionMatrix = Camera.GetViewProjection() * ModelMatrix

		TimeLoc = glGetUniformLocation(ProgramId, "Time")
		glUniform1f(TimeLoc, CurrentTime)

		NormalMatrixLoc = glGetUniformLocation(ProgramId, "NormalMatrix")
		glUniformMatrix4fv(NormalMatrixLoc, 1, GL_FALSE, glm.value_ptr(NormalMatrix))

		ModelViewMatrixLoc = glGetUniformLocation(ProgramId, "ModelViewMatrix")
		glUniformMatrix4fv(ModelViewMatrixLoc, 1, GL_FALSE, glm.value_ptr(ModelViewMatrix))

		ModelViewProjectionLoc = glGetUniformLocation(ProgramId, "ModelViewProjection")
		glUniformMatrix4fv(ModelViewProjectionLoc, 1, GL_FALSE, glm.value_ptr(ModelViewProjectionMatrix))

		LightIntensityLoc = glGetUniformLocation(ProgramId, "LightIntensity")
		glUniform1f(LightIntensityLoc, Light.Intensity)

		LightDirectionViewSpace = ViewMatrix * glm.vec4( Light.Direction, 0.0)

		LightDirectionLoc = glGetUniformLocation(ProgramId, "LightDirection")
		glUniform3fv(LightDirectionLoc, 1, glm.value_ptr(LightDirectionViewSpace))

		glActiveTexture(GL_TEXTURE0)
		glBindTexture(GL_TEXTURE_2D, EarthTextureId)

		glActiveTexture(GL_TEXTURE1)
		glBindTexture(GL_TEXTURE_2D, CloudsTextureId)

		TextureSamplerLoc = glGetUniformLocation(ProgramId, "EarthTexture")
		glUniform1i(TextureSamplerLoc, 0)

		CloudsTextureSamplerLoc = glGetUniformLocation(ProgramId, "CloudsTexture")
		glUniform1i(CloudsTextureSamplerLoc, 1)

		glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
		glBindVertexArray(SphereVAO)
		glDrawElements(GL_TRIANGLES, len(SphereIndices) * 3, GL_UNSIGNED_INT)
		glBindVertexArray(0)

		glfw.poll_events()
		glfw.swap_buffers(Window)

	
	glDeleteBuffers(1, SphereElementBuffer)
	glDeleteBuffers(1, SphereVertexBuffer)
	glDeleteVertexArrays(1, SphereVAO)
	glDeleteProgram(ProgramId)
	glDeleteTextures(1, EarthTextureId)

	glfw.destroy_window(Window)
	glfw.terminate()


