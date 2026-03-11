document.addEventListener('DOMContentLoaded', () => {
    // Only run on history page
    const historyContainer = document.getElementById('historyContainer');

    if (historyContainer) {
        const loadingDiv = document.getElementById('loadingHistory');
        const emptyDiv = document.getElementById('emptyHistory');
        const filterBtns = document.querySelectorAll('.filter-btn');

        let allHistoryData = [];

        // Fetch History
        async function fetchHistory() {
            try {
                loadingDiv.style.display = 'block';
                historyContainer.style.display = 'none';
                emptyDiv.style.display = 'none';

                const response = await fetch('http://localhost:8000/api/history', {
                    headers: {
                        'Authorization': `Bearer ${Auth.getToken()}`
                    }
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    allHistoryData = processAndSortCombinedHistory(data.data);
                    renderHistory(allHistoryData);

                    // Update Dashboard Stats if we are on dashboard (this script is on history though usually)
                    // We'll update stats locally on history page just in case we add them here.
                } else {
                    throw new Error(data.error?.message || 'Failed to load history');
                }
            } catch (error) {
                console.error('Error fetching history:', error);
                loadingDiv.style.display = 'none';
                emptyDiv.style.display = 'block';
                emptyDiv.querySelector('p').textContent = `Error: ${error.message}`;
            } finally {
                loadingDiv.style.display = 'none';
            }
        }

        // Process endpoints from backend which returns { chats, crops, diseases }
        // We need to combine them into one timeline
        function processAndSortCombinedHistory(data) {
            let combined = [];

            // Add crops
            if (data.crops && data.crops.length > 0) {
                data.crops.forEach(item => {
                    combined.push({
                        type: 'crop',
                        timestamp: new Date(item.timestamp),
                        title: 'Crop Recommendation',
                        details: `Input NPK levels: ${item.input.nitrogen}, ${item.input.phosphorus}, ${item.input.potassium}. Recommended: ${item.recommended_crop}`,
                        highlight: item.recommended_crop
                    });
                });
            }

            // Add diseases
            if (data.diseases && data.diseases.length > 0) {
                data.diseases.forEach(item => {
                    combined.push({
                        type: 'disease',
                        timestamp: new Date(item.timestamp),
                        title: 'Disease Analysis',
                        details: `Confidence: ${item.confidence}%`,
                        highlight: item.disease
                    });
                });
            }

            // Add chats
            if (data.chats && data.chats.length > 0) {
                data.chats.forEach(item => {
                    combined.push({
                        type: 'chat',
                        timestamp: new Date(item.timestamp),
                        title: 'AI Chat',
                        details: `You: "${item.message.substring(0, 50)}${item.message.length > 50 ? '...' : ''}"`,
                        highlight: 'Interaction'
                    });
                });
            }

            // Sort by descending date
            return combined.sort((a, b) => b.timestamp - a.timestamp);
        }

        function renderHistory(items) {
            historyContainer.innerHTML = '';

            if (items.length === 0) {
                historyContainer.style.display = 'none';
                emptyDiv.style.display = 'block';
                return;
            }

            emptyDiv.style.display = 'none';
            historyContainer.style.display = 'block';

            items.forEach((item, index) => {
                const dateStr = item.timestamp.toLocaleDateString();
                const timeStr = item.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

                let iconClass = '';
                let iconHtml = '';

                switch (item.type) {
                    case 'crop':
                        iconClass = 'icon-crop';
                        iconHtml = '<i class="fa-solid fa-seedling"></i>';
                        break;
                    case 'disease':
                        iconClass = 'icon-disease';
                        iconHtml = '<i class="fa-solid fa-bug"></i>';
                        break;
                    case 'chat':
                        iconClass = 'icon-chat';
                        iconHtml = '<i class="fa-solid fa-comment-dots"></i>';
                        break;
                }

                const delay = index < 10 ? index * 0.05 : 0;

                const cardHtml = `
                    <div class="history-card animate-fade-in" style="animation-delay: ${delay}s">
                        <div class="history-icon ${iconClass}">
                            ${iconHtml}
                        </div>
                        <div class="history-content">
                            <h4 class="history-title">
                                ${item.title} <span style="font-weight: 800; color: var(--primary);">| ${item.highlight}</span>
                            </h4>
                            <p class="history-details">${item.details}</p>
                        </div>
                        <div class="history-time">
                            ${dateStr} ${timeStr}
                        </div>
                    </div>
                `;

                historyContainer.insertAdjacentHTML('beforeend', cardHtml);
            });
        }

        // Handle Filters
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Update active class
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const filter = btn.getAttribute('data-filter');

                if (filter === 'all') {
                    renderHistory(allHistoryData);
                } else {
                    const filtered = allHistoryData.filter(item => item.type === filter);
                    renderHistory(filtered);
                }
            });
        });

        // Init
        fetchHistory();
    }
});
