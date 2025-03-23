async function getLocationImage() {
    const location = document.getElementById('location').value;
    const preview = document.getElementById('preview');

    if (!location) {
        alert('Please enter a location.');
        return;
    }

    try {
        const response = await fetch(`http://localhost:3000/image/${location}`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch image');
        }

        const data = await response.json();

        if (data.imageUrl) {
            renderVR(data.imageUrl);
        } else {
            alert('No image found.');
        }
    } catch (error) {
        console.error('Error fetching image:', error);
        alert('Failed to fetch image');
    }
}

function renderVR(imageUrl) {
    const preview = document.getElementById('preview');
    preview.innerHTML = ''; // Clear previous preview

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, preview.clientWidth / preview.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer();

    renderer.setSize(preview.clientWidth, preview.clientHeight);
    preview.appendChild(renderer.domElement);

    const geometry = new THREE.SphereGeometry(500, 60, 40);
    geometry.scale(-1, 1, 1);

    const texture = new THREE.TextureLoader().load(imageUrl);
    const material = new THREE.MeshBasicMaterial({ map: texture });

    const sphere = new THREE.Mesh(geometry, material);
    scene.add(sphere);

    camera.position.set(0, 0, 0.1);

    function animate() {
        requestAnimationFrame(animate);
        sphere.rotation.y += 0.001;  // Slow, smooth rotation
        renderer.render(scene, camera);
    }

    animate();
}

// Fullscreen functionality
const preview = document.getElementById('preview');
const fullscreenBtn = document.getElementById('fullscreen-btn');

function toggleFullScreen() {
    if (!document.fullscreenElement) {
        preview.requestFullscreen().catch(err => {
            console.error(`Error attempting fullscreen: ${err.message}`);
        });
        fullscreenBtn.textContent = 'Exit Fullscreen';
    } else {
        document.exitFullscreen();
        fullscreenBtn.textContent = 'Toggle Fullscreen';
    }
}
