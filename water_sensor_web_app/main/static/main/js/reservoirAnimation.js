var resOb    = null;
var renderer = null;
var scene    = null;
var camera   = null;


var animate = function () {
}

var run = () => {
  requestAnimationFrame(run);
  renderer.render(scene, camera);
  animate();
}

var main = () => {
  var canvas = document.getElementById('reservoir-animation');
  var sceneWidth = canvas.offsetWidth;
  var sceneHeigth = canvas.offsetHeight;
  // create a renderer to draw on the canvas
  renderer   = new THREE.WebGLRenderer({canvas: canvas, antialias: true});
  renderer.setSize(sceneWidth, sceneHeigth);
  renderer.setClearColor(0xffffff, 1);

  // create a scene where the reservoir object
  // will be present
  scene = new THREE.Scene();
  // the scene's camera
  camera = new THREE.PerspectiveCamera(45, sceneWidth/sceneHeigth, 1, 4000);
  scene.add(camera);

  // lighting for the scene
  var light = new THREE.DirectionalLight(0xffffff, 1.5);
  light.position.set(1, 1, 1);
  scene.add(light);

  // create the reservoir object
  var resMat  = new THREE.MeshPhongMaterial({
    map  : THREE.ImageUtils.loadTexture(RESERVOIR_WALL),
    color: 0xffffff
  });
  var resGeom = new THREE.BoxGeometry(reservoir.width, reservoir.heigth, reservoir.length);
  resOb         = new THREE.Mesh(resGeom, resMat);
  resOb.position.x = 0;
  resOb.rotation.y = Math.PI/2;
  resOb.position.z = -9;

  scene.add(resOb);

  run();
}

$(document).ready(main);