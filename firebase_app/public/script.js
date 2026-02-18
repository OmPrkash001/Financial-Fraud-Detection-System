document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('fraudForm');
    const submitBtn = document.getElementById('submitBtn');
    const resultCard = document.getElementById('result');
    
    // UI Elements
    const resultIcon = document.getElementById('resultIcon');
    const resultTitle = document.getElementById('resultTitle');
    const resultDesc = document.getElementById('resultDesc');
    const probFill = document.getElementById('probFill');
    const probValue = document.getElementById('probValue');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Show loading state
        submitBtn.classList.add('btn-loading');
        submitBtn.disabled = true;
        resultCard.classList.add('hidden');
        resultCard.style.display = 'none';

        // Collect data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        // Convert numbers
        data.amt = parseFloat(data.amt);
        data.age = parseInt(data.age);
        data.hour = parseInt(data.hour);

        try {
            // Call API (Relative path now since we are serving from the same origin)
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (result.status === 'success') {
                showResult(result);
            } else {
                alert('Analysis failed: ' + (result.error || 'Unknown error'));
            }

        } catch (error) {
            console.error('Error:', error);
            alert('Connection failed. Ensure the backend server is running.');
        } finally {
            submitBtn.classList.remove('btn-loading');
            submitBtn.disabled = false;
        }
    });

    function showResult(data) {
        resultCard.style.display = 'block';
        // Trigger reflow for animation
        void resultCard.offsetWidth;
        resultCard.classList.remove('hidden');

        const isFraud = data.prediction === 1;
        const probability = (data.probability * 100).toFixed(1);

        if (isFraud) {
            resultIcon.textContent = '🚨';
            resultTitle.textContent = 'High Risk Detected';
            resultTitle.style.color = 'var(--danger)';
            resultDesc.textContent = 'This transaction shows patterns consistent with fraudulent activity.';
            probFill.style.backgroundColor = 'var(--danger)';
        } else {
            resultIcon.textContent = '🛡️';
            resultTitle.textContent = 'Safe Transaction';
            resultTitle.style.color = 'var(--success)';
            resultDesc.textContent = 'No suspicious patterns detected.';
            probFill.style.backgroundColor = 'var(--success)';
        }

        // Animate bar
        setTimeout(() => {
            probFill.style.width = `${probability}%`;
        }, 100);
        
        probValue.textContent = `${probability}%`;
    }
});
