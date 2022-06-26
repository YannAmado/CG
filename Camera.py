import glm


class SimpleCamera:
	def __init__(self):
		self.bEnableMouseMovement = False
		self.PreviousCursor = glm.vec2(0.0)
		self.ForwardScale = 0.0
		self.RightScale = 0.0

		self.Location = glm.vec3(0.0, 0.0, 5.0)
		self.Direction = glm.vec3(0.0, 0.0, -1.0)
		self.Up = glm.vec3(0.0, 1.0, 0.0)

		self.FieldOfView = glm.radians(45.0)
		self.AspectRatio = 4.0/3.0
		self.Near = 0.01
		self.Far = 1000.0

	def MoveForward(self, Scale: float):
		self.ForwardScale = Scale

	def MoveRight(self, Scale: float):
		self.RightScale = Scale

	def MouseMove(self, X: float, Y: float):
		if self.bEnableMouseMovement:
			CurrentCursor = glm.vec2(X, Y)
			Delta = glm.vec2((CurrentCursor - self.PreviousCursor)/10.0)

			if Delta.sizeof() < 5.0:
				Right = glm.vec3(glm.cross(self.Direction, self.Up))

				RotationRight = glm.rotate(glm.identity <glm.mat4>(), glm.radians(-Delta.y), Right)
				RotationUp = glm.rotate(glm.identity <glm.mat4>(), glm.radians(-Delta.x), self.Up)
				Rotation = RotationRight * RotationUp

				self.Up = Rotation * glm.vec4(self.Up, 0)
				self.Direction = Rotation * glm.vec4(self.Direction, 0)

			self.PreviousCursor = CurrentCursor

	def Update(self, DeltaTime: float):
		Right = glm.vec3(glm.cross(self.Direction, self.Up))
		self.Location += self.Direction * self.ForwardScale * DeltaTime
		self.Location += Right * self.RightScale * DeltaTime

	def GetView(self) -> glm.vec4:
		return glm.lookAt(self.Location, self.Location + self.Direction, self.Up)

	def GetViewProjection(self) -> glm.mat4:
		View = self.GetView()
		Projection = glm.perspective(self.FieldOfView, self.AspectRatio, self.Near, self.Far)
		return Projection * View







