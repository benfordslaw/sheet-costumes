var noiseVal = 0.125;
var defaultStroke = 2;
var showPaperSizeOutlines = true;

function setup() {
  createCanvas(816, 1056, SVG).position((windowWidth-width)/2, (windowHeight-height)/2);

  noSmooth();

  noFill();
  stroke(0);
  strokeWeight(defaultStroke);
  strokeJoin(ROUND);

  stroke(0);
  push();
  translate(width/2, height/2);

  //face
  //translate(width/2, height/2 - height*2/11);
  //rotate(PI/2);
  sc = 1/7;
  scale(sc);
  drawFace(sc);
  drawEarsHair(sc);
  drawHeart(sc);
  // save("plot.svg");
  pop();

}

function drawFace(sc) {
  var w = height;
  var h = height;

  strokeWeight(defaultStroke / sc);

  stroke(225);
  if(showPaperSizeOutlines){
    rect(-w*8.5/22,h*2/11,w*8.5/11,h);
  }
  stroke(0);

  circle(-w/11, h - h*2.5/11, w/16); //left eye
  circle(w/11, h - h*2.5/11, w/16); //right eye

  arc(0,0,w*12/11, w*12/11, PI/4, 3*PI/4); //forehead

  drawMouth(w, h);
  drawEyebrows(w, h);
  drawEyelashes(-w/11, w/11, h - h*2.5/11, w/32);
  drawNose(h - h*2.5/11, h - h/11);
  drawCheeks(w*1.5/11, h-1.5*h/11, h/11);

  strokeWeight(defaultStroke);
}

function drawRightSide(w, h) {
  stroke(225);
  if(showPaperSizeOutlines){
    rect(0,-h*8.5/22 + h*2/11,w,h*8.5/11);
  }
  stroke(0);

  push();
  rotate(-PI/4);
  line(0,w*6/11,0,w*7/11);
  pop();
  arc(0,0,w*14/11,w*14/11,0,PI/4);

  arc(w*8/11,w*3/11,w/12,h/12,PI,0);
}

function drawLeftSide(w, h) {
  stroke(225);
  if(showPaperSizeOutlines){
    rect(0,-h*8.5/22 + h*2/11,-w,h*8.5/11);
  }
  stroke(0);

  push();
  push();
  rotate(PI/4);
  line(0,w*6/11,0,w*7/11);
  pop();
  arc(0,0,w*14/11,w*14/11,3*PI/4,PI);

  arc(-w*8/11,w*3/11,w/12,h/12,PI,0);
}

function drawBack(w, h) {
  var hairLength = w*14/11;

  stroke(225);
  if(showPaperSizeOutlines){
    rect(0, -h + h*2/11, w*8.5/11, h);
    rect(0, -h + h*2/11, -w*8.5/11, h);
  }
  stroke(0);

  line(-w*7/11, 0, -hairLength/2, 0);
  line(w*7/11, 0, hairLength/2, 0);

  switch(ceil(random(3))){
    case 1:
      arc(0,0,hairLength, hairLength, PI, 0);
      break;
    case 2:
      var waves = 2*ceil(random(20))
      beginShape();
      vertex(hairLength/2,0);
      for(var i=0; i<=waves; i++){
        if(i%2==1){
          vertex(0.5*hairLength*0.875*cos(-i*PI/waves), 0.5*hairLength*0.875*sin(-i*PI/waves));
        } else {
          vertex(0.5*hairLength*cos(-i*PI/waves), 0.5*hairLength*sin(-i*PI/waves));
        }
      }
      vertex(-hairLength/2,0);
      endShape();
      break;
    default:
      var waves = 2*ceil(random(20))
      beginShape();
      vertex(hairLength/2,0);
      for(var i=0; i<=waves; i++){
        if(i%2==1){
          curveVertex(0.5*hairLength*0.875*cos(-i*PI/waves), 0.5*hairLength*0.875*sin(-i*PI/waves));
        } else {
          curveVertex(0.5*hairLength*cos(-i*PI/waves), 0.5*hairLength*sin(-i*PI/waves));
        }
      }
      vertex(-hairLength/2,0);
      endShape();
      break;
  }
}

function drawEarsHair(sc) {
  var w = height;
  var h = height; 

  strokeWeight(defaultStroke / sc);

  drawRightSide(w, h);
  drawLeftSide(w, h);
  drawBack(w, h);
  
  strokeWeight(defaultStroke);
}

function drawHeart(sc) {

  var w = width*2/11;
  var h = w;
  var x = 0;
  var y = height*22/11;
  var noiseVal = w/48;

  strokeWeight(defaultStroke / sc);

  stroke(225);
  if(showPaperSizeOutlines){
    rect(-width/2, height*16/11, width, height);
  }
  stroke(0);

  for (var sign = -1; sign <= 1; sign += 2) {
    beginShape();
    vertex(x, y - h / 3.5);
    curveVertex(x, y - h / 3.5);
    curveVertex(x + sign * (w / 3.5) + randomGaussian(0,noiseVal), y - h / 2 + randomGaussian(0,noiseVal));
    curveVertex(x + sign * (w / 2) + randomGaussian(0,noiseVal), y - h / 2.5 + randomGaussian(0,noiseVal));
    curveVertex(x + sign * (w / 2) + randomGaussian(0,noiseVal), y - h / 8 + randomGaussian(0,noiseVal));
    curveVertex(x + sign * (w / 8) + randomGaussian(0,noiseVal), y + h / 4 + randomGaussian(0,noiseVal));
    curveVertex(x, y + h / 2);
    vertex(x, y + h / 2);
    endShape();
  }

  strokeWeight(defaultStroke);
}

function drawCheeks(distFromMiddle, y, maxRad) {

  var rad = random(maxRad/2, maxRad);

  switch(ceil(random(3))){
    case 1: //x's
      line(-distFromMiddle - rad/2, y-rad/2, -distFromMiddle + rad/2, y+rad/2);
      line(-distFromMiddle - rad/2, y+rad/2, -distFromMiddle + rad/2, y-rad/2);
      line(distFromMiddle - rad/2, y-rad/2, distFromMiddle + rad/2, y+rad/2);
      line(distFromMiddle - rad/2, y+rad/2, distFromMiddle + rad/2, y-rad/2);
      break;
    default:
      break;
  }
}

function drawNose(yTop, yBottom) {
  var noiseVal = (yTop - yBottom)/16;
  var noseWidth = randomGaussian((yTop-yBottom)/4, noiseVal);

  switch(ceil(random(3))){
    case 1: //triangle
      triangle(0, randomGaussian(yTop, noiseVal), -noseWidth, yBottom, noseWidth, yBottom);
      break;
    case 2:
      beginShape();
      vertex(-noseWidth, yBottom)
      vertex(0, yBottom+randomGaussian(noseWidth, noiseVal));
      vertex(noseWidth, yBottom)
      endShape();
      break;
    default: //button nose
      arc(0, yBottom, 2*noseWidth, 2*noseWidth, PI, 0);
      break;
  }
}

function drawMouth(w, h) {
  var smiliness = abs(randomGaussian(1/4, 0.125));
  var wiggle = 1 + abs(randomGaussian(0, smiliness/24));
  var numWiggles = pow(2,(ceil(random(3))));

  beginShape();
  vertex(-w*2/11, h - h/11);
  for(i=-1.5; i<=1.5; i+=1/numWiggles){
    if(0 == (numWiggles*abs(i))%2){
      curveVertex(randomGaussian(0, wiggle) + i * w/11, randomGaussian(0, wiggle) + h - smiliness * sq(i) * h/11 - wiggle);
    } else {
      curveVertex(randomGaussian(0, wiggle) + i * w/11, randomGaussian(0, wiggle) + wiggle * h - smiliness * sq(i) * h/11 - wiggle);
    }
  }
  vertex(w*2/11, h - h/11);
  endShape();
}

function drawEyebrows(w, h) {
  var curvature = abs(randomGaussian(1/8, 0.125));
  var wiggle = 1 + abs(randomGaussian(0, curvature/24));
  var numWiggles = pow(2,(ceil(random(3))));
  var tilt= randomGaussian(11*PI/12, PI/16);
  var browWidth = random(0.5, 1);

  push();
  translate(w*1.25/11, h - 3.25*h/11);
  rotate(-tilt);
  beginShape();
  vertex(-w*2/11, -h/11);
  for(i=-browWidth; i<=browWidth; i+=1/numWiggles){
    if(0 == (numWiggles*abs(i))%2){
      curveVertex(randomGaussian(0, wiggle) + i * w/11, randomGaussian(0, wiggle)- curvature * sq(i) * h/11 - wiggle);
    } else {
      curveVertex(randomGaussian(0, wiggle) + i * w/11, randomGaussian(0, wiggle) + wiggle - curvature * sq(i) * h/11 - wiggle);
    }
  }
  vertex(w*2/11, -h/11);
  endShape();
  pop();

  push();
  translate(-w*1.25/11, h - 3.25*h/11);
  rotate(tilt);
  beginShape();
  vertex(-w*2/11, -h/11);
  for(i=-browWidth; i<=browWidth; i+=1/numWiggles){
    if(0 == (numWiggles*abs(i))%2){
      curveVertex(randomGaussian(0, wiggle) + i * w/11, randomGaussian(0, wiggle)- curvature * sq(i) * h/11 - wiggle);
    } else {
      curveVertex(randomGaussian(0, wiggle) + i * w/11, randomGaussian(0, wiggle) + wiggle - curvature * sq(i) * h/11 - wiggle);
    }
  }
  vertex(w*2/11, -h/11);
  endShape();
  pop();
}

function drawEyelashes(xEye1, xEye2, h, r) {

  var spacing = randomGaussian(PI/6, PI/12);
  var numLashes = ceil(random(10));

  push();
  translate(xEye1, h);
  for(var a=0; a<=numLashes; a++){
    rotate(spacing);
    line(0,r,0,r+10);
  }
  pop();

  push();
  translate(xEye2, h);
  for(var a=0; a<=numLashes; a++){
    rotate(-spacing);
    line(0,r,0,r+10);
  }
  pop();
}