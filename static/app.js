/**
 * Jia Futuristic Robot Dashboard - Frontend Controller
 * Default Language: English (JennyNeural)
 * Boss: Zain Sultan
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const voiceMicBtn = document.getElementById('voiceMicBtn');
    const dockMicBtn = document.getElementById('dockMicBtn');
    const transcriptionText = document.getElementById('transcriptionText');
    const statusLabel = document.getElementById('statusLabel');
    const statusPill = document.getElementById('statusPill');
    const responseCard = document.getElementById('responseCard');
    const respBody = document.getElementById('respBody');
    const respTime = document.getElementById('respTime');
    const commandForm = document.getElementById('commandForm');
    const commandInput = document.getElementById('commandInput');
    const soundToggleBtn = document.getElementById('soundToggleBtn');
    const soundIcon = document.getElementById('soundIcon');
    const neuralAudioPlayer = document.getElementById('neuralAudioPlayer');
    const detailTitle = document.getElementById('detailTitle');
    const detailCategory = document.getElementById('detailCategory');
    const previewImg = document.getElementById('previewImg');
    const previewTitle = document.getElementById('previewTitle');

    let isListening = false;
    let isSpeaking = false;
    let isSoundMuted = false;
    let recognition = null;

    // =========================================================================
    // 1. Audio Visualizer Waveform Canvas
    // =========================================================================
    const canvas = document.getElementById('waveformCanvas');
    const ctx = canvas.getContext('2d');
    let animationPhase = 0;

    function drawWaveform() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const radius = 95;

        // Draw multiple glowing sinusoidal circular ripples
        const waveCount = isSpeaking ? 4 : (isListening ? 3 : 2);
        const amplitude = isSpeaking ? 16 : (isListening ? 22 : 6);
        const speed = isSpeaking ? 0.08 : (isListening ? 0.12 : 0.03);

        animationPhase += speed;

        for (let w = 0; w < waveCount; w++) {
            ctx.beginPath();
            const currentRadius = radius + (w * 10);
            
            for (let angle = 0; angle < Math.PI * 2; angle += 0.05) {
                const waveOffset = Math.sin(angle * (5 + w) + animationPhase + (w * 1.5)) * amplitude;
                const r = currentRadius + waveOffset;
                const x = centerX + Math.cos(angle) * r;
                const y = centerY + Math.sin(angle) * r;

                if (angle === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            }

            ctx.closePath();
            ctx.lineWidth = w === 0 ? 2.5 : 1.5;
            ctx.strokeStyle = w % 2 === 0 ? 'rgba(0, 242, 254, 0.7)' : 'rgba(157, 78, 221, 0.6)';
            ctx.shadowBlur = 12;
            ctx.shadowColor = w % 2 === 0 ? '#00f2fe' : '#9d4edd';
            ctx.stroke();
        }

        requestAnimationFrame(drawWaveform);
    }

    drawWaveform();

    // =========================================================================
    // 2. Speech Recognition (Web Speech API - English Default)
    // =========================================================================
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = 'en-US'; // English Recognition by Default

        recognition.onstart = () => {
            isListening = true;
            voiceMicBtn.classList.add('listening');
            dockMicBtn.classList.add('active');
            statusLabel.textContent = "Listening to Boss Zain...";
            transcriptionText.textContent = "Listening...";
        };

        recognition.onresult = (event) => {
            let interimTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    const finalTranscript = event.results[i][0].transcript;
                    transcriptionText.textContent = `"${finalTranscript}"`;
                    executeCommand(finalTranscript);
                } else {
                    interimTranscript += event.results[i][0].transcript;
                    transcriptionText.textContent = `"${interimTranscript}..."`;
                }
            }
        };

        recognition.onerror = (event) => {
            console.warn("Speech recognition notice:", event.error);
            stopListening();
            statusLabel.textContent = "Ready for Voice Command";
        };

        recognition.onend = () => {
            stopListening();
        };
    } else {
        console.log("Web Speech API not supported in this browser. You can type commands below.");
    }

    function startListening() {
        if (!recognition) {
            alert("Microphone voice recognition requires Google Chrome or Microsoft Edge. You can also type commands into the chat bar below!");
            return;
        }
        try {
            recognition.start();
        } catch (e) {
            console.error(e);
        }
    }

    function stopListening() {
        isListening = false;
        voiceMicBtn.classList.remove('listening');
        dockMicBtn.classList.remove('active');
        if (!isSpeaking) {
            statusLabel.textContent = "Ready for Voice Command";
        }
    }

    function toggleListening() {
        if (isListening) {
            if (recognition) recognition.stop();
            stopListening();
        } else {
            startListening();
        }
    }

    voiceMicBtn.addEventListener('click', toggleListening);
    dockMicBtn.addEventListener('click', toggleListening);

    // =========================================================================
    // 3. Command Execution & API Bridge
    // =========================================================================
    async function executeCommand(cmdText) {
        if (!cmdText || !cmdText.trim()) return;

        statusLabel.textContent = "Processing instruction...";
        transcriptionText.textContent = `"${cmdText}"`;
        commandInput.value = "";

        try {
            const resp = await fetch('/api/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: cmdText })
            });

            const data = await resp.json();
            handleServerResponse(data);
        } catch (err) {
            console.error("API error:", err);
            respBody.textContent = "Boss Zain, I encountered a connection issue while executing that command.";
            statusLabel.textContent = "Connection Error";
        }
    }

    function handleServerResponse(data) {
        // Update display text
        respBody.textContent = data.response;
        respTime.textContent = data.timestamp || "Just Now";
        detailTitle.textContent = data.query || "Direct Execution";
        detailCategory.textContent = data.category || "General";

        // Update Wallpaper preview if wallpaper changed
        if (data.action_type === "wallpaper_change" && data.action_data && data.action_data.path) {
            previewTitle.textContent = "Applied Wallpaper: " + (data.action_data.theme || "Cyber");
            // Cache bust image
            previewImg.src = "/api/wallpaper/preview?" + new Date().getTime();
        }

        // Play neural speech audio if available and unmuted
        if (data.audio_url && !isSoundMuted) {
            playNeuralAudio(data.audio_url);
        } else {
            statusLabel.textContent = "Task Completed for Boss Zain";
        }
    }

    function playNeuralAudio(audioUrl) {
        isSpeaking = true;
        statusLabel.textContent = "Jia Speaking...";
        neuralAudioPlayer.src = audioUrl;
        
        neuralAudioPlayer.play().catch(e => {
            console.log("Audio autoplay prevented by browser policy:", e);
        });

        neuralAudioPlayer.onended = () => {
            isSpeaking = false;
            statusLabel.textContent = "Ready for Voice Command";
        };
    }

    // =========================================================================
    // 4. Form & Click Event Listeners
    // =========================================================================
    commandForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const query = commandInput.value.trim();
        if (query) {
            executeCommand(query);
        }
    });

    // Module Card clicks
    document.querySelectorAll('.module-card').forEach(card => {
        card.addEventListener('click', () => {
            const cmd = card.getAttribute('data-cmd');
            if (cmd) executeCommand(cmd);
        });
    });

    // Action button clicks
    document.querySelectorAll('.action-tile-btn, .loyalty-box').forEach(btn => {
        btn.addEventListener('click', () => {
            const cmd = btn.getAttribute('data-cmd');
            if (cmd) executeCommand(cmd);
        });
    });

    // Sound toggle
    soundToggleBtn.addEventListener('click', () => {
        isSoundMuted = !isSoundMuted;
        soundIcon.textContent = isSoundMuted ? '🔇' : '🔊';
        if (isSoundMuted) {
            neuralAudioPlayer.pause();
            isSpeaking = false;
        }
    });

    // Initial greeting sound trigger (if user interacts)
    document.body.addEventListener('click', () => {
        // Unlocks web audio context
    }, { once: true });
});
