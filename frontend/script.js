document.addEventListener("DOMContentLoaded", () => {
    // Theme Toggle
    const themeToggleBtn = document.getElementById("themeToggleBtn");
    const body = document.body;
    
    // Check saved theme
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) {
        body.setAttribute("data-theme", savedTheme);
        updateThemeIcon(savedTheme);
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        body.setAttribute("data-theme", "dark");
        updateThemeIcon("dark");
    }
    
    themeToggleBtn.addEventListener("click", () => {
        const currentTheme = body.getAttribute("data-theme");
        const newTheme = currentTheme === "dark" ? "light" : "dark";
        body.setAttribute("data-theme", newTheme);
        localStorage.setItem("theme", newTheme);
        updateThemeIcon(newTheme);
    });
    
    function updateThemeIcon(theme) {
        const icon = themeToggleBtn.querySelector("i");
        if (theme === "dark") {
            icon.className = "fas fa-sun";
        } else {
            icon.className = "fas fa-moon";
        }
    }

    // Chatbot Toggle
    const floatingBtn = document.getElementById("floatingBtn");
    const chatbotWidget = document.getElementById("chatbotWidget");
    const closeChatBtn = document.getElementById("closeChatBtn");
    
    floatingBtn.addEventListener("click", () => {
        chatbotWidget.classList.add("active");
        floatingBtn.style.display = "none";
        
        // Auto greet if no history
        if (chatHistory.length === 0) {
            setTimeout(() => {
                addMessage("Hello 👋 Welcome to TechNova Solutions. How can I help you?", "bot");
            }, 500);
        }
    });
    
    closeChatBtn.addEventListener("click", () => {
        chatbotWidget.classList.remove("active");
        setTimeout(() => {
            floatingBtn.style.display = "flex";
        }, 300);
    });

    // Chat Logic
    const chatBody = document.getElementById("chatBody");
    const chatInput = document.getElementById("chatInput");
    const sendBtn = document.getElementById("sendBtn");
    const clearBtn = document.getElementById("clearBtn");
    const suggestions = document.querySelectorAll(".suggestion");
    const voiceBtn = document.getElementById("voiceBtn");
    
    let chatHistory = JSON.parse(localStorage.getItem("chatHistory")) || [];
    
    // Load History
    function loadHistory() {
        chatBody.innerHTML = "";
        if (chatHistory.length > 0) {
            chatHistory.forEach(msg => {
                renderMessage(msg.text, msg.sender, false);
            });
        }
    }
    loadHistory();
    
    function saveHistory() {
        localStorage.setItem("chatHistory", JSON.stringify(chatHistory));
    }

    function getTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function renderMessage(text, sender, animate = true) {
        const msgDiv = document.createElement("div");
        msgDiv.className = `chat-bubble ${sender}-msg`;
        
        // Convert text to HTML paragraphs safely
        const htmlText = text.replace(/\n/g, '<br>');
        let innerHTML = `<p>${htmlText}</p>`;
        
        innerHTML += `<span class="timestamp">${getTime()}</span>`;
        
        if (sender === "bot") {
            innerHTML += `<button class="copy-btn" title="Copy to clipboard"><i class="fas fa-copy"></i></button>`;
        }
        
        msgDiv.innerHTML = innerHTML;
        
        chatBody.appendChild(msgDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
        
        if (sender === "bot") {
            const copyBtn = msgDiv.querySelector(".copy-btn");
            if (copyBtn) {
                copyBtn.addEventListener("click", () => {
                    navigator.clipboard.writeText(text);
                    const icon = copyBtn.querySelector("i");
                    icon.className = "fas fa-check";
                    setTimeout(() => {
                        icon.className = "fas fa-copy";
                    }, 2000);
                });
            }
        }
    }

    function showTyping(agentName = "AI Assistant") {
        let typingIndicator = document.getElementById("typingIndicator");
        if (!typingIndicator) {
            typingIndicator = document.createElement("div");
            typingIndicator.className = "typing-indicator-container";
            typingIndicator.id = "typingIndicator";
            chatBody.appendChild(typingIndicator);
        }
        
        typingIndicator.innerHTML = `
            <span class="agent-tag">${agentName} is thinking...</span>
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    function hideTyping() {
        const typingDiv = document.getElementById("typingIndicator");
        if (typingDiv) {
            typingDiv.remove();
        }
    }

    function addMessage(text, sender) {
        renderMessage(text, sender, true);
        chatHistory.push({ text, sender, timestamp: getTime() });
        saveHistory();
    }

    async function sendMessage(text) {
        if (!text.trim()) return;
        
        addMessage(text, "user");
        chatInput.value = "";
        
        showTyping("Orchestrator");
        
        // Simulate multi-agent steps for UI polish
        setTimeout(() => showTyping("Retriever"), 1500);
        setTimeout(() => showTyping("Specialized Agent"), 3000);
        setTimeout(() => showTyping("Validator"), 4500);

        try {
            const API_URL = "http://localhost:8000/chat";
            
            const response = await fetch(API_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: text })
            });
            
            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }
            
            const data = await response.json();
            hideTyping();
            addMessage(data.answer, "bot");
            
        } catch (error) {
            console.error("Chat error:", error);
            hideTyping();
            addMessage("Sorry, I'm having trouble connecting to the server. Please try again later.", "bot");
        }
    }

    sendBtn.addEventListener("click", () => {
        sendMessage(chatInput.value);
    });

    chatInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            sendMessage(chatInput.value);
        }
    });

    suggestions.forEach(sug => {
        sug.addEventListener("click", () => {
            sendMessage(sug.innerText);
        });
    });

    clearBtn.addEventListener("click", () => {
        chatHistory = [];
        saveHistory();
        chatBody.innerHTML = "";
        addMessage("Chat cleared. How can I help you?", "bot");
    });
    
    // Voice Input via Web Speech API
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        recognition.continuous = false;
        recognition.interimResults = false;
        
        recognition.onstart = function() {
            voiceBtn.style.color = "red";
        };
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            chatInput.value = transcript;
            voiceBtn.style.color = "var(--text-color)";
        };
        
        recognition.onerror = function(event) {
            console.error("Speech recognition error", event.error);
            voiceBtn.style.color = "var(--text-color)";
        };
        
        recognition.onend = function() {
            voiceBtn.style.color = "var(--text-color)";
        };
        
        voiceBtn.addEventListener('click', () => {
            recognition.start();
        });
    } else {
        voiceBtn.style.display = "none";
    }
});
