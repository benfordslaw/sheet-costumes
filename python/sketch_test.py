import vsketch, math, shapely, random, trimesh
from shapely.geometry import *
from shapely.ops import *
from shapely import affinity
from trimesh import path
import numpy as np
from pynoise.noisemodule import *
from pynoise.noiseutil import *

particles = []

def concentric_fill(vsk, polygon):
    return_geom = polygon
    while return_geom.is_empty == False:
        vsk.geometry(return_geom)
        return_geom = return_geom.buffer(-10)

def radial_hair_fill(vsk, polygon):
    (ox, oy, px, py) = polygon.bounds

    scalp_off = 1
    hair_lines = []
    step_out = 25
    noise_scale = random.uniform(0,4)

    for a in np.arange(0, math.pi * 2, math.pi / 60):
        position = [scalp_off * math.cos(a), scalp_off * math.sin(a)]
        hair_line = []
        while position[0] >= ox and position[0] <= px and position[1] >= oy and position[1] <= py:
            n = Perlin().get_value(math.sin(a) * noise_scale, math.cos(a) * noise_scale, 0) * Point(position[0], position[1]).distance(polygon.centroid) / 200
            position[0] += math.cos(a) * step_out + n
            position[1] += math.sin(a) * step_out + n
            hair_line.append(Point(position[0], position[1]))
        hair_lines.append(LineString(hair_line))
    
    hair_lines = MultiLineString(hair_lines).buffer(2).intersection(polygon) # crops to hair
    bald_bound = Point(0, 0).buffer(75*scalp_off)
    concentric_fill(vsk, bald_bound)
    hair_lines = unary_union([hair_lines, Point(0, 0).buffer(30*scalp_off)]) # removes circle from geom
    
    vsk.geometry(hair_lines)

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
  num_wiggles = pow(2,(math.ceil(random.randint(2,5))))
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

def draw_eyelashes(vsk, x_eye_1, x_eye_2, h, r):

    spacing = np.random.normal(math.pi/6, math.pi/12)
    num_lashes = math.ceil(random.randint(1,9))

    vsk.pushMatrix()
    vsk.translate(x_eye_1, h)
    for a in range(0, num_lashes):
        vsk.rotate(spacing)
        vsk.line(0,r,0,r+30)
    vsk.popMatrix()

    vsk.pushMatrix()
    vsk.translate(x_eye_2, h)
    for a in range(0, num_lashes):
        vsk.rotate(-spacing)
        vsk.line(0,r,0,r+30)
    vsk.popMatrix()

def draw_nose(vsk, y_top, y_bottom):
    noise_val = (y_top - y_bottom)/16
    nose_width = np.random.normal((y_top-y_bottom)/4, abs(noise_val))

    nose_type = math.ceil(random.randint(0,2))
    if nose_type == 1: # triangle
        nose = []
        nose.append(Point(0, np.random.normal(y_top, abs(noise_val))))
        nose.append(Point(-nose_width, y_bottom))
        nose.append(Point(nose_width, y_bottom))
        nose = Polygon(nose)
        vsk.geometry(nose)
        concentric_fill(vsk, nose)
    elif nose_type == 2: # ^
        nose = []
        nose.append(Point(-nose_width, y_bottom))
        nose.append(Point(0, y_bottom+np.random.normal(nose_width, abs(noise_val))))
        nose.append(Point(nose_width, y_bottom))
        vsk.geometry(LineString(nose))
    else: # button nose
        vsk.arc(0, y_bottom, 2*nose_width, 2*nose_width, math.pi, 0)

def draw_cheeks(vsk, dist_from_middle, y, maxRad):

    rad = random.uniform(maxRad/2, maxRad)
    if math.ceil(random.randint(0,1)) == 1:
        vsk.line(-dist_from_middle - rad/2, y-rad/2, -dist_from_middle + rad/2, y+rad/2)
        vsk.line(-dist_from_middle - rad/2, y+rad/2, -dist_from_middle + rad/2, y-rad/2)
        vsk.line(dist_from_middle - rad/2, y-rad/2, dist_from_middle + rad/2, y+rad/2)
        vsk.line(dist_from_middle - rad/2, y+rad/2, dist_from_middle + rad/2, y-rad/2)

def draw_face(vsk: vsketch.Vsketch):
    w = vsk.height
    h = vsk.height

    vsk.circle(-w/11, h - h*2.5/11, w/16) # left eye
    vsk.circle(w/11, h - h*2.5/11, w/16) # right eye

    draw_mouth(vsk, w, h)
    draw_eyebrows(vsk, w, h)
    draw_eyelashes(vsk, -w/11, w/11, h - h*2.5/11, w/32)
    draw_nose(vsk, h - h*2.5/11, h - h/11)
    draw_cheeks(vsk, w*1.5/11, h-1.5*h/11, h/11)

def draw_ears_hair(vsk, sc):
    w = vsk.height
    h = vsk.height

    vsk.arc(-w*8/11,w*3/11,w/12,h/12,0,-math.pi) # ear
    vsk.arc(w*8/11,w*3/11,w/12,h/12,0,-math.pi) # ear

    hair = []

    r = w*14/22
    for a in np.arange(math.pi, 3*math.pi/4, -math.pi / 24):
        hair.append(Point(r*math.cos(a), r*math.sin(a)))

    r = w*12/22
    for a in np.arange(3*math.pi/4, math.pi/4, -math.pi / 24):
        hair.append(Point(r*math.cos(a), r*math.sin(a)))
        
    r = w*14/22
    for a in np.arange(math.pi/4, 0, -math.pi / 24):
        hair.append(Point(r*math.cos(a), r*math.sin(a)))
    
    hair_length = w*14/11
    hair_type = math.ceil(random.randint(0,1))

    if hair_type == 1:
        waves = 2*math.ceil(random.randint(1, 19))
        hair.append(Point(hair_length/2,0))
        for i in range(0, waves):
            if(i%2==1):
                hair.append(Point(0.5*hair_length*0.875*math.cos(-i*math.pi/waves), 0.5*hair_length*0.875*math.sin(-i*math.pi/waves)))
            else:
                hair.append(Point(0.5*hair_length*math.cos(-i*math.pi/waves), 0.5*hair_length*math.sin(-i*math.pi/waves)))
        hair.append(Point(-hair_length/2,0))
    else:
        waves = 2*math.ceil(random.randint(0, 19))
        hair.append(Point(hair_length/2,0))
        for i in range(0, waves):
            if i%2 == 1:
                hair.append(Point(0.5*hair_length*0.875*math.cos(-i*math.pi/waves), 0.5*hair_length*0.875*math.sin(-i*math.pi/waves)))
            else:
                hair.append(Point(0.5*hair_length*math.cos(-i*math.pi/waves), 0.5*hair_length*math.sin(-i*math.pi/waves)))
        hair.append(Point(-hair_length/2,0))
    
    vsk.geometry(Polygon(hair))
    radial_hair_fill(vsk, Polygon(hair))

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