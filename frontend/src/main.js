import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';

//create scene
const scene = new THREE.Scene();

//light source creation
const ambientLight = new THREE.AmbientLight(0xffffff, 0.3);
scene.add(ambientLight)

const sunLight = new THREE.DirectionalLight(0xffffff, 1)
sunLight.position.set(5,3,5);
scene.add(sunLight);

//Google's CDN for the Draco decoder
const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');

//model loader
// const gtlfLoader = new GLTFLoader();
// gtlfLoader.setDRACOLoader(dracoLoader);
// let issModel;

// gtlfLoader.load('/models/iss.glb', (gltf) => {
//     issModel = gltf.scene;
//     issModel.scale.set(0.003, 0.003, 0.003);
//     scene.add(issModel);
// });

//marker instead, better performance
let issMarker;
const issGeometry = new THREE.SphereGeometry(0.02, 8, 8);
const issMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 });
issMarker = new THREE.Mesh(issGeometry, issMaterial);
scene.add(issMarker);

function latLonToXYZ(lat, lon, alt){
    const EARTH_RADIUS = 1;
    const EARTH_RADIUS_KM = 6371;
    const r = EARTH_RADIUS + (alt / EARTH_RADIUS_KM);

    const phi = (90 - lat) * (Math.PI / 180);
    const theta = (lon + 180) * (Math.PI / 180);

    return{
        x: -r * Math.sin(phi) * Math.cos(theta),
        y: r * Math.cos(phi),
        z: r * Math.sin(phi) * Math.sin(theta)
    };
}

//get iss current position and next position
let currentPos = new THREE.Vector3();
let targetPos = new THREE.Vector3();

async function updateISS() {
    const res = await fetch('http://localhost:8000/iss');
    const data = await res.json();
    const { x, y, z } = latLonToXYZ(data.latitude, data.longitude, data.altitude_km);
    targetPos.set(x, y, z);
    issMarker.userData.feed = data.feed;
}

updateISS();
setInterval(updateISS, 2000);

//load sphere and apply earth texture
const textureLoader = new THREE.TextureLoader()
const earthTexture = textureLoader.load('/textures/earth.jpg')

const geometry = new THREE.SphereGeometry(1, 64, 64);
const material = new THREE.MeshPhongMaterial({ map: earthTexture });
const earth = new THREE.Mesh(geometry, material);
scene.add(earth);


//window size
const sizes = {
    width: window.innerWidth,
    height: window.innerHeight
};

//camera creation
const camera = new THREE.PerspectiveCamera(75, sizes.width / sizes.height, 0.1, 100);
camera.position.z = 3;
scene.add(camera);

// rendering
const canvas = document.querySelector('canvas.webgl');
const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    antialias: true
});
renderer.setSize(sizes.width, sizes.height);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

// Handle Window Resize
window.addEventListener('resize', () => {
    // Update sizes
    sizes.width = window.innerWidth;
    sizes.height = window.innerHeight;

    // Update camera aspect ratio
    camera.aspect = sizes.width / sizes.height;
    camera.updateProjectionMatrix();

    // Update renderer
    renderer.setSize(sizes.width, sizes.height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
});

// animation loop
const clock = new THREE.Clock();

//orbital controls
const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;

//mouse input, raycast
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

window.addEventListener('click', (e) => {
    mouse.x = (e.clientX / sizes.width) * 2 - 1;
    mouse.y = -(e.clientY / sizes.height) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObject(issMarker);

    if (intersects.length > 0) {
        openFeed(issMarker.userData.feed);
    }
});

function openFeed(url) {
    const overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed; bottom: 20px; right: 20px;
        width: 400px; height: 225px; z-index: 999; background: black;
        border-radius: 8px; overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    `;
    overlay.innerHTML = `
        <iframe width="100%" height="100%" src="${url}" frameborder="0" allowfullscreen></iframe>
        <button onclick="this.parentElement.remove()" style="position:absolute; top:8px; right:8px; background: rgba(0,0,0,0.6); color: white; border: none; cursor: pointer; padding: 4px 8px; border-radius: 4px;">✕</button>
    `;
    document.body.appendChild(overlay);
}

const tick = () => {
    const elapsedTime = clock.getElapsedTime();

    // smoothly move current toward target each frame
    currentPos.lerp(targetPos, 0.08);
    if (issMarker) issMarker.position.copy(currentPos);

    controls.update();
    // Render
    renderer.render(scene, camera);
    // Call tick again on the next frame
    window.requestAnimationFrame(tick);
};

tick();