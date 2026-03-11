document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatMessages = document.getElementById('chatMessages');
    const typingIndicator = document.getElementById('typingIndicator');

    if (chatForm) {

        // Auto scroll to bottom
        function scrollToBottom() {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        // Add message to UI
        function appendMessage(text, isUser) {
            const wrapperDiv = document.createElement('div');
            wrapperDiv.className = `message ${isUser ? 'user' : 'bot'}`;

            let iconHtml = '';
            if (!isUser) {
                iconHtml = `<div class="bot-avatar" style="width: 32px; height: 32px; font-size: 1rem;"><i class="fa-solid fa-robot"></i></div>`;
            }

            // Convert simple markdown-like elements (very basic)
            let formattedText = text.replace(/\n/g, '<br>');
            formattedText = formattedText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

            wrapperDiv.innerHTML = `
                ${iconHtml}
                <div class="message-content">${formattedText}</div>
            `;

            // Insert before typing indicator
            chatMessages.insertBefore(wrapperDiv, typingIndicator);
            scrollToBottom();
        }

        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const message = chatInput.value.trim();
            if (!message) return;

            // Clear input
            chatInput.value = '';

            // Add user message to UI
            appendMessage(message, true);

            // Show typing indicator
            typingIndicator.style.display = 'flex';
            scrollToBottom();

            try {
                const response = await fetch('http://localhost:8000/api/chatbot/message', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${Auth.getToken()}`
                    },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();

                // Hide typing
                typingIndicator.style.display = 'none';

                if (response.ok && data.success) {
                    appendMessage(data.data.reply, false);
                } else {
                    appendMessage(`Error: ${data.message || 'Could not get a response. Please try again.'}`, false);
                    console.error('Chat error:', data);
                }
            } catch (error) {
                typingIndicator.style.display = 'none';
                appendMessage('Network error. Could not reach the server.', false);
                console.error(error);
            }
        });
    }
});
