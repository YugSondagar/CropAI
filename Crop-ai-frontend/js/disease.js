document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const previewContainer = document.getElementById('previewContainer');
    const imagePreview = document.getElementById('imagePreview');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resetBtn = document.getElementById('resetBtn');
    const resultCard = document.getElementById('resultCard');
    const errorDiv = document.getElementById('diseaseError');
    const analyzeLoader = document.getElementById('analyzeLoader');
    const analyzeText = document.querySelector('#analyzeBtn span');

    let currentFile = null;

    // Handle Drag and Drop
    if (dropZone) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.remove('dragover');
            }, false);
        });

        dropZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            handleFiles(files);
        }, false);

        fileInput.addEventListener('change', function () {
            handleFiles(this.files);
        });

        function handleFiles(files) {
            if (files.length > 0) {
                const file = files[0];
                if (file.type.startsWith('image/')) {
                    currentFile = file;

                    // Show preview
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        imagePreview.src = e.target.result;
                        dropZone.style.display = 'none';
                        previewContainer.style.display = 'block';
                        resultCard.style.display = 'none';
                        errorDiv.style.display = 'none';
                    };
                    reader.readAsDataURL(file);
                } else {
                    errorDiv.textContent = 'Please upload a valid image file.';
                    errorDiv.style.display = 'block';
                }
            }
        }
    }

    // Handle Reset
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            currentFile = null;
            fileInput.value = '';
            imagePreview.src = '';
            dropZone.style.display = 'block';
            previewContainer.style.display = 'none';
            resultCard.style.display = 'none';
            errorDiv.style.display = 'none';
        });
    }

    // Handle Analysis
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', async () => {
            if (!currentFile) return;

            analyzeText.style.display = 'none';
            analyzeLoader.style.display = 'block';
            errorDiv.style.display = 'none';
            resultCard.style.display = 'none';
            analyzeBtn.disabled = true;

            const formData = new FormData();
            formData.append('file', currentFile);

            try {
                const response = await fetch('http://localhost:8000/api/disease/predict', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${Auth.getToken()}`
                    },
                    body: formData
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    const { disease, confidence } = data.data;

                    // Update UI
                    const diseaseEl = document.getElementById('predictedDisease');
                    const confTextEl = document.getElementById('confidenceText');
                    const confBarEl = document.getElementById('confidenceBar');

                    diseaseEl.textContent = disease;
                    confTextEl.textContent = `${confidence.toFixed(1)}%`;

                    // Reset bar for animation
                    confBarEl.style.width = '0%';

                    // Style based on results (basic example: healthy vs sick)
                    if (disease.toLowerCase().includes('healthy')) {
                        diseaseEl.classList.add('healthy');
                        confBarEl.style.backgroundColor = 'var(--primary)';
                    } else {
                        diseaseEl.classList.remove('healthy');
                        confBarEl.style.backgroundColor = '#ef4444'; // Red for disease
                    }

                    resultCard.style.display = 'block';

                    // Trigger animation
                    setTimeout(() => {
                        confBarEl.style.width = `${confidence}%`;
                    }, 100);

                    resultCard.scrollIntoView({ behavior: 'smooth' });
                } else {
                    throw new Error(data.error?.message || 'Failed to analyze image');
                }
            } catch (error) {
                errorDiv.textContent = error.message;
                errorDiv.style.display = 'block';
            } finally {
                analyzeText.style.display = 'block';
                analyzeLoader.style.display = 'none';
                analyzeBtn.disabled = false;
            }
        });
    }
});
