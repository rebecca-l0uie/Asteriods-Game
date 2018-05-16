import pygame, sys, random, math, time

class asteroid(object):
	def __init__(self):
		self.size=75
		self.rad=self.size/2
		self.size=(self.size,self.size)
		self.ast = pygame.image.load('meteor2.png')
		self.ast = pygame.transform.scale(self.ast, self.size)
		self.xpos = random.randint(1,width)
		self.ypos = random.randint(1,height/2)
		self.xvel = random.randint(-3,3)
		if self.xvel == 0:
			self.xvel = 1
		self.yvel = random.randint(-3,3)
		if self.yvel == 0:
			self.yvel = 1
		self.rotdir= random.randint(1,2)
		self.angle = 0
	def redraw(self):
		self.xpos=self.xpos+self.xvel
		self.ypos=self.ypos+self.yvel
   
		if self.xpos > width:
			self.xpos = 0
		if self.xpos < 0:
			self.xpos = width
		if self.ypos > height:
			self.ypos = 0
		if self.ypos < 0:
			self.ypos = height
	   
		if self.rotdir==1:
			self.angle = self.angle - 3.0
		else:
			self.angle = self.angle + 3.0
		   
		rotast = pygame.transform.rotate(self.ast, self.angle)
		rotrec = rotast.get_rect()
		rotrec.center = (self.xpos,self.ypos)
		screen.blit(rotast,rotrec)
	   
class shipclass(object):
	def __init__(self):   
		self.size = (150)
		self.rad = self.size/2
		self.size = (self.size,self.size)
		self.ship = pygame.image.load('ship.png')
		self.ship = pygame.transform.scale(self.ship, self.size)
		self.xpos = width/2
		self.ypos = height-height/4
		self.vel = 0
		self.angle = 0   
		self.anglevel = 0
		self.switch = False
		self.driftangle = 0
	   
	def redraw(self):
		if self.xpos > width:
			self.xpos = 0
		if self.xpos < 0:
			self.xpos = width
		if self.ypos > height:
			self.ypos = 0
		if self.ypos < 0:
			self.ypos = height
	   
		if self.switch == True:
			if self.vel <= 7:
				self.vel += 0.1
			self.r=self.angle*(math.pi/180.0)
			self.xpos+=self.vel*(math.sin(self.r))*-1
			self.ypos+=self.vel*(math.cos(self.r))*-1
	   
		if self.switch == False:
			self.vel = self.vel*0.95
			self.r=self.driftangle*(math.pi/180.0)
			self.xpos+=self.vel*(math.sin(self.r))*-1
			self.ypos+=self.vel*(math.cos(self.r))*-1
	   
		self.angle=self.angle+self.anglevel   
		rotship = pygame.transform.rotate(self.ship, self.angle)
		rotrec = rotship.get_rect()
		rotrec.center = (self.xpos,self.ypos)
		screen.blit(rotship,rotrec)
	   
class bullet(object):
	def __init__(self):
		self.alive = True
		self.size = 20
		self.rad = self.size/2
		self.size = (self.size,self.size)
		self.image = pygame.image.load('globe.png')
		self.image = pygame.transform.scale(self.image, self.size)
		self.imagerect = self.image.get_rect()
		self.xpos = ship.xpos
		self.initxpos = self.xpos
		self.ypos = ship.ypos
		self.initypos = self.ypos
		self.vel = 6
		self.angle = ship.angle
		self.remove=False
	   
	def redraw(self):
		if self.xpos-self.initxpos > 500 or self.xpos-self.initxpos < -500:
			self.remove=True
		if self.ypos-self.initypos > 500 or self.ypos-self.initypos < -500:
			self.remove=True
	   
		self.r=self.angle*(math.pi/180.0)
		self.xpos+=self.vel*(math.sin(self.r))*-1
		self.ypos+=self.vel*(math.cos(self.r))*-1
		screen.blit(self.image,(self.xpos,self.ypos))

pygame.init()

width,height = 1224,1000
size = [width,height]
screen = pygame.display.set_mode(size)
astlist=[]
for x in range(1):
	astlist.append(asteroid())
bullets=[]
ship=shipclass()
destroy=[]
#boom = pygame.mixer.Sound('explode.wav')
pygame.display.set_caption("Asteroids")
space = pygame.image.load('SKY2.jpeg')
space = pygame.transform.scale(space,(width,height))
done = False
bounce = pygame.mixer.Sound('BOUNCE.wav')
boom = pygame.mixer.Sound('BOOM.wav')
clock = pygame.time.Clock()
score = 0

#--------- Main Program Loop -----------
while done == False:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done=True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:               
				ship.anglevel = -5.0
			elif event.key == pygame.K_LEFT:
				ship.anglevel = 5.0
			elif event.key == pygame.K_UP:
				ship.switch=True
			elif event.key == pygame.K_DOWN:
				pass
			elif event.key == pygame.K_SPACE:
				bullets.append(bullet())
				bounce.play()
				bullets[-1].vel+=ship.vel/2
			   
		if event.type == pygame.KEYUP:   
			if event.key == pygame.K_RIGHT:
				ship.anglevel = 0
			elif event.key == pygame.K_LEFT:
				ship.anglevel = 0
			elif event.key == pygame.K_UP:
				ship.switch = False
				ship.driftangle=ship.angle
			elif event.key == pygame.K_DOWN:
				pass
			   
	screen.blit(space,(0,0))  
	for ast in astlist:
		D=math.sqrt((ast.xpos-ship.xpos)**2+(ast.ypos-ship.ypos)**2)
		if (ast.rad+ship.rad)>D:
			boom.play()
			destroy.append(ship)
	if ship in destroy:
		#time.sleep(1)
		break 
	for b in bullets:
		if b.remove:
			bullets.remove(b)
	for ast in astlist:
		for b in bullets:
			D=math.sqrt((ast.xpos-b.xpos)**2+(ast.ypos-b.ypos)**2)
			if (ast.rad+b.rad)>D:
				astlist.remove(ast)
				bullets.remove(b)
				score=+10
		ast.redraw()
	for b in bullets:
		if b.xpos <= 0 or b.xpos == width or b.ypos <= 0 or b.ypos == height:
			bullets.remove(b)
		b.redraw()	   
	ship.redraw()
	font = pygame.font.SysFont('Arial', 25, True, False)
	text= font.render("Score:",True,WHITE)
	scoretext= font.render(str(score),True,WHITE)
	screen.blit(scoretext, [65, 0]) 
	screen.blit(text, [0, 0]) 
	pygame.display.flip()
   
	clock.tick(30)
