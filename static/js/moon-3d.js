let scene, camera, renderer, moon, moonGlow;
let isMouseDown = false;
let prevMouseX = 0;
let prevMouseY = 0;
const rotationSpeed = 0.003;

function createProceduralMoonSurface(geometry) {
  const positions = geometry.attributes.position;
  const normals = geometry.attributes.normal;
  const uvs = geometry.attributes.uv;

  for (let i = 0; i < positions.count; i++) {
    const vertex = new THREE.Vector3();
    vertex.fromBufferAttribute(positions, i);

    // Add base crater formations using multiple noise layers
    let displacement = 0;
    displacement +=
      simplex.noise3D(vertex.x * 0.5, vertex.y * 0.5, vertex.z * 0.5) * 0.15;
    displacement +=
      simplex.noise3D(vertex.x * 2, vertex.y * 2, vertex.z * 2) * 0.05;

    // Add procedural craters
    for (let c = 0; c < 15; c++) {
      const craterCenter = new THREE.Vector3(
        Math.random() * 2 - 1,
        Math.random() * 2 - 1,
        Math.random() * 2 - 1
      ).normalize();

      const distance = vertex.normalize().distanceTo(craterCenter);
      const craterSize = Math.random() * 0.5 + 0.5;
      const craterDepth = Math.random() * 0.1;

      if (distance < craterSize) {
        const craterShape = Math.cos((Math.PI * distance) / craterSize);
        displacement -= craterDepth * craterShape;
      }
    }

    // Apply displacement along normal
    const normal = new THREE.Vector3();
    normal.fromBufferAttribute(normals, i);
    vertex.add(normal.multiplyScalar(displacement));
    positions.setXYZ(i, vertex.x, vertex.y, vertex.z);
  }

  geometry.computeVertexNormals();
  return geometry;
}

function init() {
  scene = new THREE.Scene();

  // Enhanced renderer setup
  renderer = new THREE.WebGLRenderer({
    antialias: true,
    alpha: true,
  });
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  // Camera setup with better initial position
  const container = document.getElementById("moon-container");
  const aspect = container.clientWidth / container.clientHeight;
  camera = new THREE.PerspectiveCamera(60, aspect, 0.1, 1000);
  camera.position.set(0, 0, 10);

  // Add stars background with better quality
  const starGeometry = new THREE.SphereGeometry(50, 96, 96);
  const starMaterial = new THREE.MeshBasicMaterial({
    map: new THREE.TextureLoader().load("/static/images/stars.jpg"),
    side: THREE.BackSide,
  });
  scene.add(new THREE.Mesh(starGeometry, starMaterial));

  // Create procedural moon
  const moonGeometry = new THREE.SphereGeometry(3, 256, 256);
  createProceduralMoonSurface(moonGeometry);

  const moonMaterial = new THREE.MeshPhysicalMaterial({
    color: 0xcccccc,
    metalness: 0.1,
    roughness: 0.8,
    reflectivity: 0.2,
    clearcoat: 0.1,
    clearcoatRoughness: 0.4,
  });

  moon = new THREE.Mesh(moonGeometry, moonMaterial);
  moon.castShadow = true;
  moon.receiveShadow = true;
  scene.add(moon);

  // Add moon glow effect
  const glowGeometry = new THREE.SphereGeometry(3.2, 32, 32);
  const glowMaterial = new THREE.MeshPhongMaterial({
    color: 0x6699ff,
    transparent: true,
    opacity: 0.15,
    side: THREE.BackSide,
  });
  moonGlow = new THREE.Mesh(glowGeometry, glowMaterial);
  scene.add(moonGlow);

  // Enhanced physically-based lighting
  const ambientLight = new THREE.AmbientLight(0x404040, 0.2);
  scene.add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0xfffae6, 3);
  updateMoonIllumination();
  scene.add(directionalLight);

  const backLight = new THREE.DirectionalLight(0x404040, 0.5);
  backLight.position.set(-5, 0, -5);
  scene.add(backLight);

  // Add earthshine effect
  const earthshine = new THREE.HemisphereLight(0x0044ff, 0x000000, 0.2);
  scene.add(earthshine);

  // Initialize scene
  updateRendererSize();
  container.appendChild(renderer.domElement);
  setupEventListeners();
  animate();
}

function setupEventListeners() {
  const container = document.getElementById("moon-container");

  container.addEventListener("mousedown", (event) => {
    isMouseDown = true;
    prevMouseX = event.clientX;
    prevMouseY = event.clientY;
  });

  document.addEventListener("mouseup", () => (isMouseDown = false));

  container.addEventListener("mousemove", (event) => {
    if (!isMouseDown) return;

    const deltaX = (event.clientX - prevMouseX) * rotationSpeed;
    const deltaY = (event.clientY - prevMouseY) * rotationSpeed;

    moon.rotation.y += deltaX;
    moonGlow.rotation.y += deltaX;
    moon.rotation.x += deltaY;
    moonGlow.rotation.x += deltaY;

    prevMouseX = event.clientX;
    prevMouseY = event.clientY;

    updateMoonDetails();
  });

  container.addEventListener("wheel", (event) => {
    event.preventDefault();
    const zoomSpeed = 0.1;
    camera.position.z = Math.max(
      6,
      Math.min(15, camera.position.z + event.deltaY * zoomSpeed)
    );
  });

  window.addEventListener("resize", updateRendererSize);
}

function updateRendererSize() {
  const container = document.getElementById("moon-container");
  const width = container.clientWidth;
  const height = container.clientHeight;
  renderer.setSize(width, height);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
}

// Update the calculateMoonPhase function to be more accurate
function calculateMoonPhase() {
  const synodic = 29.530588853; // Synodic month in days
  const date = new Date();
  const epoch = new Date(2000, 0, 6, 18, 14); // Known new moon
  const elapsed = (date - epoch) / (1000 * 60 * 60 * 24);
  return ((elapsed % synodic) / synodic) * 360;
}

function updateMoonIllumination() {
  const phase = calculateMoonPhase();
  const phaseRadians = (phase * Math.PI) / 180;
  const lightDirection = new THREE.Vector3(
    Math.cos(phaseRadians),
    0,
    Math.sin(phaseRadians)
  );

  directionalLight.position.copy(lightDirection.multiplyScalar(10));
}

function updateMoonDetails() {
  const phaseAngle = calculateMoonPhase();
  const longitude = ((moon.rotation.y * 180) / Math.PI) % 360;
  const latitude = ((moon.rotation.x * 180) / Math.PI) % 360;

  document.getElementById("phase-angle").textContent = phaseAngle.toFixed(1);
  document.getElementById("longitude").textContent = longitude.toFixed(1);
  document.getElementById("latitude").textContent = latitude.toFixed(1);
}

function animate() {
  requestAnimationFrame(animate);

  if (!isMouseDown) {
    moon.rotation.y += 0.001;
    moonGlow.rotation.y += 0.001;
    updateMoonDetails();
  }

  // Add subtle floating motion
  moon.position.y = Math.sin(Date.now() * 0.001) * 0.1;
  moonGlow.position.y = moon.position.y;

  renderer.render(scene, camera);
}

init();
