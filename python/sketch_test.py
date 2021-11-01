import vsketch, math
import shapely
from shapely.geometry import *
from shapely.ops import *
from shapely import affinity
import random
from HersheyFonts import HersheyFonts
import trimesh
from trimesh import path
import numpy as np

def draw_mouth(vsk, w, h):
  smiliness = abs(np.random.normal(1/4, 0.125))
  wiggle = 1 + abs(np.random.normal(0, smiliness/24))
  num_wiggles = math.pow(2,(math.ceil(random.randint(0,2))))

  smile_curve = []
  for i in np.arange(-1.5, 1.5 + 1/num_wiggles, 1/num_wiggles):
    if 0 == (num_wiggles*abs(i))%2:
      smile_curve.append(Point(np.random.normal(0, wiggle) + i * w/11, np.random.normal(0, wiggle) + h - smiliness * (i ** 2) * h/11 - wiggle))
    else:
      smile_curve.append(Point(np.random.normal(0, wiggle) + i * w/11, np.random.normal(0, wiggle) + wiggle * h - smiliness * (i ** 2) * h/11 - wiggle))

  smile_curve = LineString(smile_curve)
  vsk.geometry(smile_curve)

def draw_eyebrows(vsk, w, h):
  curvature = abs(np.random.normal(1/8, 0.125))
  wiggle = 1 + abs(np.random.normal(0, curvature/24))
  num_wiggles = pow(2,(math.ceil(random.randint(1,4))))
  tilt = np.random.normal(11*math.pi/12, math.pi/16)
  brow_width = random.uniform(0.5, 1)

  vsk.pushMatrix()
  vsk.translate(w*1.25/11, h - 3.25*h/11)
  vsk.rotate(-tilt)
  eyebrow_curve = []
  for i in np.arange(-brow_width, brow_width, 1/num_wiggles):
    if 0 == (num_wiggles*abs(i))%2:
      eyebrow_curve.append(Point(np.random.normal(0, wiggle) + i * w/11, np.random.normal(0, wiggle)- curvature * (i ** 2) * h/11 - wiggle))
    else:
      eyebrow_curve.append(Point(np.random.normal(0, wiggle) + i * w/11, np.random.normal(0, wiggle) + wiggle - curvature * (i ** 2) * h/11 - wiggle))
  vsk.geometry(LineString(eyebrow_curve))
  vsk.popMatrix()

  vsk.pushMatrix()
  vsk.translate(-w*1.25/11, h - 3.25*h/11)
  vsk.rotate(tilt)
  eyebrow_curve = []
  for i in np.arange(-brow_width, brow_width, 1/num_wiggles):
    if 0 == (num_wiggles*abs(i))%2:
      eyebrow_curve.append(Point(np.random.normal(0, wiggle) + i * w/11, np.random.normal(0, wiggle)- curvature * (i ** 2) * h/11 - wiggle))
    else:
      eyebrow_curve.append(Point(np.random.normal(0, wiggle) + i * w/11, np.random.normal(0, wiggle) + wiggle - curvature * (i ** 2) * h/11 - wiggle))
  vsk.geometry(LineString(eyebrow_curve))
  vsk.popMatrix()

def draw_eyelashes(vsk, xEye1, xEye2, h, r):

    spacing = np.random.normal(math.pi/6, math.pi/12)
    num_lashes = math.ceil(random.randint(1,9))

    vsk.pushMatrix()
    vsk.translate(xEye1, h)
    for a in range(0, num_lashes):
        vsk.rotate(spacing)
        vsk.line(0,r,0,r+30)
    vsk.popMatrix()

    vsk.pushMatrix()
    vsk.translate(xEye2, h)
    for a in range(0, num_lashes):
        vsk.rotate(-spacing)
        vsk.line(0,r,0,r+30)
    vsk.popMatrix()

def draw_nose(vsk, yTop, yBottom):
    noise_val = (yTop - yBottom)/16
    nose_width = np.random.normal((yTop-yBottom)/4, abs(noise_val))

    nose_type = math.ceil(random.randint(0,2))
    if nose_type == 1: # triangle
        vsk.triangle(0, np.random.normal(yTop, abs(noise_val)), -nose_width, yBottom, nose_width, yBottom)
    elif nose_type == 2: # ^
        nose = []
        nose.append(Point(-nose_width, yBottom))
        nose.append(Point(0, yBottom+np.random.normal(nose_width, abs(noise_val))))
        nose.append(Point(nose_width, yBottom))
        vsk.geometry(LineString(nose))
    else: # button nose
        vsk.arc(0, yBottom, 2*nose_width, 2*nose_width, math.pi, 0)

def draw_cheeks(vsk, distFromMiddle, y, maxRad):

    rad = random.uniform(maxRad/2, maxRad)
    if math.ceil(random.randint(0,1)) == 1:
        vsk.line(-distFromMiddle - rad/2, y-rad/2, -distFromMiddle + rad/2, y+rad/2)
        vsk.line(-distFromMiddle - rad/2, y+rad/2, -distFromMiddle + rad/2, y-rad/2)
        vsk.line(distFromMiddle - rad/2, y-rad/2, distFromMiddle + rad/2, y+rad/2)
        vsk.line(distFromMiddle - rad/2, y+rad/2, distFromMiddle + rad/2, y-rad/2)

def draw_face(vsk: vsketch.Vsketch):
    w = vsk.height
    h = vsk.height

    vsk.circle(-w/11, h - h*2.5/11, w/16) # left eye
    vsk.circle(w/11, h - h*2.5/11, w/16) # right eye

    vsk.arc(0,0,w*12/11, w*12/11, -3*math.pi/4, -math.pi/4) # forehead

    draw_mouth(vsk, w, h)
    draw_eyebrows(vsk, w, h)
    draw_eyelashes(vsk, -w/11, w/11, h - h*2.5/11, w/32)
    draw_nose(vsk, h - h*2.5/11, h - h/11)
    draw_cheeks(vsk, w*1.5/11, h-1.5*h/11, h/11)

def draw_ears_hair(vsk, sc):
    w = vsk.height
    h = vsk.height

    vsk.pushMatrix()
    vsk.rotate(-math.pi/4)
    vsk.line(0,w*6/11,0,w*7/11)
    vsk.popMatrix()
    vsk.arc(0,0,w*14/11,w*14/11,-math.pi/4, 0)

    vsk.arc(w*8/11,w*3/11,w/12,h/12,0,-math.pi)

    vsk.pushMatrix()
    vsk.rotate(math.pi/4)
    vsk.line(0,w*6/11,0,w*7/11)
    vsk.popMatrix()
    vsk.arc(0,0,w*14/11,w*14/11,-math.pi, -3*math.pi/4)

    vsk.arc(-w*8/11,w*3/11,w/12,h/12,0,-math.pi)

    # hair_length = random.uniform(w*14/11, 3*w*14/11)
    hair_length = w*14/11

    vsk.line(-w*7/11, 0, -hair_length/2, 0)
    vsk.line(w*7/11, 0, hair_length/2, 0)

    hair_type = math.ceil(random.randint(0,2))

    if hair_type == 1:
        vsk.arc(0,0,hair_length, hair_length, 0, -math.pi)
    elif hair_type == 2:
        waves = 2*math.ceil(random.randint(1, 19))
        hair = []
        hair.append(Point(hair_length/2,0))
        for i in range(0, waves):
            if(i%2==1):
                hair.append(Point(0.5*hair_length*0.875*math.cos(-i*math.pi/waves), 0.5*hair_length*0.875*math.sin(-i*math.pi/waves)))
            else:
                hair.append(Point(0.5*hair_length*math.cos(-i*math.pi/waves), 0.5*hair_length*math.sin(-i*math.pi/waves)))
        hair.append(Point(-hair_length/2,0))
        vsk.geometry(LineString(hair))
    else:
        waves = 2*math.ceil(random.randint(0, 19))
        hair = []
        hair.append(Point(hair_length/2,0))
        for i in range(0, waves):
            if i%2 == 1:
                hair.append(Point(0.5*hair_length*0.875*math.cos(-i*math.pi/waves), 0.5*hair_length*0.875*math.sin(-i*math.pi/waves)))
            else:
                hair.append(Point(0.5*hair_length*math.cos(-i*math.pi/waves), 0.5*hair_length*math.sin(-i*math.pi/waves)))
        
        
        hair.append(Point(-hair_length/2,0))
        vsk.geometry(LineString(hair))

class TestSketch(vsketch.SketchClass):
                    
    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("50in", "30in", center=False)

        x = 500
        y = 450
        
        vsk.pushMatrix()
        vsk.translate(vsk.width/2, vsk.height/2)
        vsk.rotate(math.pi/2)

        sc = 1/1.75
        vsk.scale(sc)

        draw_face(vsk)
        draw_ears_hair(vsk, sc)

        vsk.popMatrix()

        
    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("reloop")

if __name__ == "<run_path>":
    TestSketch.display()