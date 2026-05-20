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

async function updateISS() {
    const res = await fetch('http://localhost:8000/iss');
    const data = await res.json();

    const { x, y, z } = latLonToXYZ(data.latitude, data.longitude, data.altitude_km);
    if (issMarker) {
        issMarker.position.set(x, y, z);
    }
}

updateISS();
setInterval(updateISS, 5000);

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

const tick = () => {
    const elapsedTime = clock.getElapsedTime();

    // Render
    renderer.render(scene, camera);


    controls.update();

    // Call tick again on the next frame
    window.requestAnimationFrame(tick);
};

tick();