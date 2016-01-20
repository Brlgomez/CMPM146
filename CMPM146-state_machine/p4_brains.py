
import random

# EXAMPLE STATE MACHINE
class MantisBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.target = None

  def handle_event(self, message, details):

    if self.state is 'idle':

      if message == 'timer':
        # go to a random point, wake up sometime in the next 10 seconds
        world = self.body.world
        x, y = random.random()*world.width, random.random()*world.height
        self.body.go_to((x,y))
        self.body.set_alarm(random.random()*10)

      elif message == 'collide' and details['what'] == 'Slug':
        # a slug bumped into us; get curious
        self.state = 'curious'
        self.body.set_alarm(1) # think about this for a sec
        self.body.stop()
        self.target = details['who']

    elif self.state == 'curious':

      if message == 'timer':
        # chase down that slug who bumped into us
        if self.target:
          if random.random() < 0.5:
            self.body.stop()
            self.state = 'idle'
          else:
            self.body.follow(self.target)
          self.body.set_alarm(1)
      elif message == 'collide' and details['what'] == 'Slug':
        # we meet again!
        slug = details['who']
        slug.amount -= 0.01 # take a tiny little bite
    
class SlugBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.target = None
    self.have_resource = False

  def handle_event(self, message, details):

    self.target = None
    if message == 'order':
      try:
        x, y = details
        self.body.go_to(details)
        pass
      except ValueError:
        if details == 'i':
          self.state = 'idle'
          self.body.stop()
          pass
        elif details == 'a':
          self.state = 'attack'
          pass
        elif details == 'h':
          self.state = 'harvest'
          pass
        elif details == 'b':
          self.state = 'build'
          pass
        elif details == 'd':
          self.body.amount = .4
          pass
     


    if self.state == 'attack':
      try:
        self.target = self.body.find_nearest("Mantis")
        self.body.follow(self.target)
        if message == 'collide' and details['who'] == self.target:
          self.target.amount -= .05
          self.body.set_alarm(2)
      except ValueError:
        self.body.stop()
        self.state = 'idle'



    if self.state == 'build':
      self.target = self.body.find_nearest("Nest")
      self.body.go_to(self.target)
      if message == 'collide' and details['who'] == self.target and self.target.amount < 1:
        self.target.amount += .01
      if self.target.amount == 1:
        self.body.stop()
        self.state = 'idle'
      self.body.set_alarm(2)



    if self.state == 'harvest':
      if self.have_resource == False:
        try:
          self.target = self.body.find_nearest("Resource")
          self.body.go_to(self.target)
          if message == 'collide' and details['who'] == self.target:
            self.target.amount -= .25
            self.have_resource = True
        except ValueError:
          self.body.stop()
          self.state = 'idle'
      else:
        self.target = self.body.find_nearest("Nest")
        self.body.go_to(self.target)
        if message == 'collide' and details['who'] == self.target:
          self.have_resource = False
      self.body.set_alarm(2)



    if self.body.amount < .5:
      self.state = 'Flee'
      
    if self.state == 'Flee':
      self.target = self.body.find_nearest("Nest")
      self.body.go_to(self.target)
      if message == 'collide' and details['who'] == self.target and self.target.amount < 1:
        self.body.amount = 1
        self.target = None
        self.body.stop()
        self.state = 'idle'
      self.body.set_alarm(2)

    pass    

world_specification = {
 # 'worldgen_seed': 13, # comment-out to randomize
  'nests': 2,
  'obstacles': 25,
  'resources': 5,
  'slugs': 5,
  'mantises': 5,
}

brain_classes = {
  'mantis': MantisBrain,
  'slug': SlugBrain,
}
