from flask import Flask, render_template_string, request, jsonify
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_ai_system import MainAISystem

app = Flask(__name__)

# Initialize AI system
ai_system = None

def initialize_ai():
    global ai_system
    try:
        ai_system = MainAISystem()
        success = ai_system.initialize_system()
        return success
    except Exception as e:
        print(f"AI initialization error: {e}")
        return False

@app.route('/')
def dashboard():
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>⚡ Power Plant AI Dashboard</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1000px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(10px);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
                color: white;
                padding: 30px;
                text-align: center;
                position: relative;
                overflow: hidden;
            }
            
            .header::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                animation: shimmer 3s ease-in-out infinite;
            }
            
            @keyframes shimmer {
                0%, 100% { transform: rotate(0deg); }
                50% { transform: rotate(180deg); }
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                position: relative;
                z-index: 1;
            }
            
            .header p {
                font-size: 1.2em;
                opacity: 0.9;
                position: relative;
                z-index: 1;
            }
            
            .chat-area {
                padding: 30px;
                display: flex;
                flex-direction: column;
                height: 600px;
            }
            
            .chat-container {
                flex: 1;
                border: none;
                background: #f8f9fa;
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 20px;
                overflow-y: auto;
                box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.05);
            }
            
            .chat-container::-webkit-scrollbar {
                width: 8px;
            }
            
            .chat-container::-webkit-scrollbar-track {
                background: #f1f1f1;
                border-radius: 10px;
            }
            
            .chat-container::-webkit-scrollbar-thumb {
                background: #c1c1c1;
                border-radius: 10px;
            }
            
            .chat-container::-webkit-scrollbar-thumb:hover {
                background: #a8a8a8;
            }
            
            .message {
                margin: 15px 0;
                padding: 15px 20px;
                border-radius: 15px;
                max-width: 80%;
                word-wrap: break-word;
                animation: slideIn 0.3s ease-out;
            }
            
            @keyframes slideIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .user-message {
                background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
                color: white;
                margin-left: auto;
                border-bottom-right-radius: 5px;
                box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
            }
            
            .ai-message {
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                color: white;
                margin-right: auto;
                border-bottom-left-radius: 5px;
                box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
                font-family: 'Courier New', monospace;
                white-space: pre-wrap;
                line-height: 1.4;
            }
            
            .input-container {
                display: flex;
                gap: 15px;
                align-items: center;
            }
            
            .input-wrapper {
                flex: 1;
                position: relative;
            }
            
            input[type="text"] {
                width: 100%;
                padding: 15px 20px;
                border: 2px solid #e9ecef;
                border-radius: 25px;
                font-size: 16px;
                outline: none;
                transition: all 0.3s ease;
                background: white;
            }
            
            input[type="text"]:focus {
                border-color: #007bff;
                box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
                transform: translateY(-2px);
            }
            
            .send-button {
                padding: 15px 30px;
                background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
                color: white;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-size: 16px;
                font-weight: 600;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
            }
            
            .send-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0, 123, 255, 0.4);
            }
            
            .send-button:active {
                transform: translateY(0);
            }
            
            .loading {
                background: linear-gradient(135deg, #ffc107 0%, #ff8f00 100%);
                animation: pulse 1.5s ease-in-out infinite;
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.7; }
            }
            
            .suggestions {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin-bottom: 20px;
            }
            
            .suggestion-chip {
                background: rgba(0, 123, 255, 0.1);
                color: #007bff;
                padding: 8px 16px;
                border-radius: 20px;
                cursor: pointer;
                font-size: 14px;
                transition: all 0.3s ease;
                border: 1px solid rgba(0, 123, 255, 0.2);
            }
            
            .suggestion-chip:hover {
                background: #007bff;
                color: white;
                transform: translateY(-1px);
            }
            
            .welcome-message {
                text-align: center;
                color: #6c757d;
                font-style: italic;
                margin: 20px 0;
            }
            
            @media (max-width: 768px) {
                .container {
                    margin: 10px;
                    border-radius: 15px;
                }
                
                .header h1 {
                    font-size: 2em;
                }
                
                .chat-area {
                    padding: 20px;
                    height: 500px;
                }
                
                .message {
                    max-width: 90%;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>⚡ Power Plant AI Dashboard</h1>
                <p>Intelligent Analytics for Your Energy Portfolio</p>
            </div>
            
            <div class="chat-area">
                <div id="chat-container" class="chat-container">
                    <div class="welcome-message">
                        🤖 Welcome! I'm your intelligent power plant assistant. Ask me anything about your energy portfolio!
                    </div>
                    
                    <div class="suggestions">
                        <div class="suggestion-chip" onclick="sendSuggestion('portfolio overview')">📊 Portfolio Overview</div>
                        <div class="suggestion-chip" onclick="sendSuggestion('best performing plant')">🏆 Top Performer</div>
                        <div class="suggestion-chip" onclick="sendSuggestion('compare CSPPL and AXPPL')">⚖️ Compare Plants</div>
                        <div class="suggestion-chip" onclick="sendSuggestion('energy generation yesterday')">📅 Yesterday's Report</div>
                    </div>
                </div>
                
                <div class="input-container">
                    <div class="input-wrapper">
                        <input type="text" id="user-input" placeholder="Ask about your plants (e.g., 'Tell me about CEPPL performance')" onkeypress="handleKeyPress(event)">
                    </div>
                    <button class="send-button" onclick="sendMessage()">Send ✈️</button>
                </div>
            </div>
        </div>
        
        <script>
            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }
            
            function sendSuggestion(message) {
                document.getElementById('user-input').value = message;
                sendMessage();
            }
            
            function sendMessage() {
                const input = document.getElementById('user-input');
                const message = input.value.trim();
                if (!message) return;
                
                const chatContainer = document.getElementById('chat-container');
                
                // Hide suggestions after first message
                const suggestions = document.querySelector('.suggestions');
                if (suggestions) {
                    suggestions.style.display = 'none';
                }
                
                // Add user message
                const userDiv = document.createElement('div');
                userDiv.className = 'message user-message';
                userDiv.textContent = message;
                chatContainer.appendChild(userDiv);
                
                // Clear input
                input.value = '';
                
                // Add loading message
                const loadingDiv = document.createElement('div');
                loadingDiv.className = 'message ai-message loading';
                loadingDiv.textContent = '🤖 Analyzing your request...';
                chatContainer.appendChild(loadingDiv);
                
                // Scroll to bottom
                chatContainer.scrollTop = chatContainer.scrollHeight;
                
                // Send to AI
                fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message})
                })
                .then(response => response.json())
                .then(data => {
                    loadingDiv.className = 'message ai-message';
                    loadingDiv.textContent = data.response;
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                })
                .catch(error => {
                    loadingDiv.className = 'message ai-message';
                    loadingDiv.textContent = '❌ Error: ' + error.message;
                });
            }
            
            // Auto-focus input
            document.getElementById('user-input').focus();
        </script>
    </body>
    </html>
    """
    return html_template

@app.route('/chat', methods=['POST'])
def chat():
    global ai_system
    
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not ai_system:
        return jsonify({'response': '❌ AI system not initialized. Please restart the server.'})
    
    try:
        response = ai_system.process_query(user_message)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': f'❌ Error processing query: {str(e)}'})

if __name__ == '__main__':
    import os
    
    # Get port from environment variable (Render sets this)
    port = int(os.environ.get('PORT', 5008))
    
    print("🚀 Starting Power Plant AI Dashboard for Render...")
    
    if initialize_ai():
        print("✅ AI system initialized successfully!")
        print(f"🌐 Dashboard starting on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        print("❌ Failed to initialize AI system!")