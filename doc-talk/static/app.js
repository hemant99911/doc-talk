document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('upload-form');
    const fileInput = document.getElementById('file-input');
    const uploadStatus = document.getElementById('upload-status');
    const questionForm = document.getElementById('question-form');
    const questionInput = document.getElementById('question-input');
    const chatBox = document.getElementById('chat-box');

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        uploadStatus.textContent = 'Uploading...';

        try {
            const response = await fetch('/uploadfile/', {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();

            if (response.ok) {
                uploadStatus.textContent = result.info;
            } else {
                uploadStatus.textContent = `Error: ${result.error}`;
            }
        } catch (error) {
            uploadStatus.textContent = 'An error occurred during upload.';
            console.error('Upload error:', error);
        }
    });

    questionForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = questionInput.value;
        if (!question) return;

        appendMessage(question, 'user');
        questionInput.value = '';

        try {
            const response = await fetch('/ask/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question }),
            });

            const result = await response.json();
            const answer = result.answer || result.error || 'Sorry, I could not get an answer.';
            appendMessage(answer, 'bot');

        } catch (error) {
            appendMessage('An error occurred while asking.', 'bot');
            console.error('Ask error:', error);
        }
    });

    function appendMessage(text, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        messageElement.textContent = text;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
