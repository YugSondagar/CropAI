document.addEventListener('DOMContentLoaded', () => {
    const cropForm = document.getElementById('cropForm');

    if (cropForm) {
        cropForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const loader = document.getElementById('cropLoader');
            const errorDiv = document.getElementById('cropError');
            const btnText = document.querySelector('#cropForm button span');
            const resultCard = document.getElementById('resultCard');
            const predictedCropEl = document.getElementById('predictedCrop');

            // Gather input data
            const inputData = {
                nitrogen: parseFloat(document.getElementById('nitrogen').value),
                phosphorus: parseFloat(document.getElementById('phosphorus').value),
                potassium: parseFloat(document.getElementById('potassium').value),
                temperature: parseFloat(document.getElementById('temperature').value),
                humidity: parseFloat(document.getElementById('humidity').value),
                ph: parseFloat(document.getElementById('ph').value),
                rainfall: parseFloat(document.getElementById('rainfall').value)
            };

            btnText.style.display = 'none';
            loader.style.display = 'block';
            errorDiv.style.display = 'none';
            resultCard.style.display = 'none';

            try {
                const response = await fetch('http://localhost:8000/api/crop/recommend', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${Auth.getToken()}`
                    },
                    body: JSON.stringify(inputData)
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    predictedCropEl.textContent = data.data.recommended_crop;
                    resultCard.style.display = 'block';
                    // Scroll to result
                    resultCard.scrollIntoView({ behavior: 'smooth' });
                } else {
                    throw new Error(data.error?.message || 'Failed to get recommendation');
                }
            } catch (error) {
                errorDiv.textContent = error.message;
                errorDiv.style.display = 'block';
            } finally {
                btnText.style.display = 'block';
                loader.style.display = 'none';
            }
        });
    }
});
