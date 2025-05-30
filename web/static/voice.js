// web/static/voice.js
// Enhanced Web Speech API for voice input and output
let recognition = null;
let synthesis = window.speechSynthesis;

function initVoiceRecognition() {
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            console.log('Voice recognition started');
            const voiceBtn = document.querySelector('.voice-input-btn');
            if (voiceBtn) {
                voiceBtn.style.background = 'linear-gradient(135deg, #dc3545, #c82333)';
                voiceBtn.innerHTML = '🔴 Listening...';
            }
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            const messageInput = document.querySelector('#message-input textarea');
            if (messageInput) {
                messageInput.value = transcript;
                messageInput.dispatchEvent(new Event('input', { bubbles: true }));
                document.querySelector('#send-button').click();
            }
        };

        recognition.onend = () => {
            const voiceBtn = document.querySelector('.voice-input-btn');
            if (voiceBtn) {
                voiceBtn.style.background = 'linear-gradient(135deg, #17a2b8, #138496)';
                voiceBtn.innerHTML = '🎤 Voice';
            }
        };

        recognition.onerror = (event) => {
            console.error('Voice recognition error:', event.error);
            const voiceBtn = document.querySelector('.voice-input-btn');
            if (voiceBtn) {
                voiceBtn.style.background = 'linear-gradient(135deg, #17a2b8, #138496)';
                voiceBtn.innerHTML = '🎤 Voice';
                alert(`Voice recognition error: ${event.error}`);
            }
        };
    } else {
        console.warn('SpeechRecognition not supported');
        alert('Voice recognition is not supported in this browser');
    }
}

function startVoiceInput() {
    if (recognition) {
        recognition.start();
    } else {
        alert('Voice recognition not supported in this browser');
    }
}

function speakText(text) {
    if (synthesis) {
        synthesis.cancel(); // Cancel ongoing speech
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.pitch = 1;
        utterance.volume = 0.8;
        synthesis.speak(utterance);
    } else {
        alert('Text-to-speech not supported in this browser');
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initVoiceRecognition();
});

// Re-initialize after Gradio updates
setInterval(() => {
    if (!recognition) {
        initVoiceRecognition();
    }
}, 1000);

