import streamlit as st
import os
import google.generativeai as genai
from gtts import gTTS
import tempfile
from dotenv import load_dotenv
import streamlit.components.v1 as components

st.set_page_config(page_title="AI Call Center - Voice Call", layout="wide")
st.title("📞 AI-Powered Virtual Call Center (Real-Time Voice Call)")

FULL_CONTEXT_FILE = "ai_full_context.txt"

# Load environment and Gemini API
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load the context file
if os.path.exists(FULL_CONTEXT_FILE):
    with open(FULL_CONTEXT_FILE, "r", encoding='utf-8') as f:
        full_context = f.read()
else:
    st.error("❌ No AI context found. Please ask Admin to generate it.")
    st.stop()

def text_to_speech(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        tts.save(fp.name)
        return fp.name

# Initialize session state
if 'call_active' not in st.session_state:
    st.session_state.call_active = False
if 'user_query' not in st.session_state:
    st.session_state.user_query = ""
if 'ai_response' not in st.session_state:
    st.session_state.ai_response = None

# Call UI
col1, col2 = st.columns(2)
with col1:
    if st.button("📞 Start Call", disabled=st.session_state.call_active):
        st.session_state.call_active = True
        st.session_state.user_query = ""
        st.session_state.ai_response = None
        st.rerun()

with col2:
    if st.button("⛔ End Call", disabled=not st.session_state.call_active):
        st.session_state.call_active = False
        st.rerun()

# Speech Recognition Component
if st.session_state.call_active:
    components.html("""
    <div id="speech-container" style="background:#f5f5f5; padding:15px; border-radius:10px; margin-bottom:20px;">
        <div style="text-align:center;">
            <button id="start-btn" style="
                background: linear-gradient(90deg, #4CAF50, #8BC34A);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 25px;
                font-weight: 600;
                cursor: pointer;
                margin: 10px;
                font-size: 16px;
            ">🎙️ Start Speaking</button>
            <div id="status" style="margin:15px; padding:10px; background:#ffffff; border-radius:5px;">
                🔴 Ready to record
            </div>
        </div>
        
        <script>
        const startBtn = document.getElementById('start-btn');
        const statusDiv = document.getElementById('status');
        let recognition = null;
        let isRecording = false;
        
        function initSpeechRecognition() {
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                statusDiv.innerHTML = "❌ Speech recognition not supported";
                return;
            }
            
            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = 'en-US';

            recognition.onstart = () => {
                isRecording = true;
                startBtn.textContent = "⏹️ Stop Recording";
                startBtn.style.background = "#F44336";
                statusDiv.innerHTML = "🎤 Listening... Speak now!";
                console.log("Recognition started");
            };

            recognition.onresult = (event) => {
                let transcript = '';
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    if (event.results[i].isFinal) {
                        transcript += event.results[i][0].transcript + ' ';
                    }
                }
                
                if (transcript) {
                    window.parent.postMessage({
                        type: "speech_transcript",
                        transcript: transcript.trim()
                    }, "*");
                    console.log("Transcript sent:", transcript);
                }
            };

            recognition.onerror = (event) => {
                console.error("Recognition error:", event.error);
                statusDiv.innerHTML = "❌ Error: " + event.error;
                resetUI();
            };

            recognition.onend = () => {
                if (isRecording) {
                    recognition.start(); // Continue recording
                    console.log("Recognition continuing");
                } else {
                    statusDiv.innerHTML = "✅ Recording complete";
                    resetUI();
                    console.log("Recognition stopped");
                    // Send final empty message to force update
                    window.parent.postMessage({
                        type: "speech_transcript",
                        transcript: ""
                    }, "*");
                }
            };
        }

        function resetUI() {
            isRecording = false;
            startBtn.textContent = "🎙️ Start Speaking";
            startBtn.style.background = "linear-gradient(90deg, #4CAF50, #8BC34A)";
        }

        startBtn.addEventListener('click', () => {
            if (!isRecording) {
                if (!recognition) initSpeechRecognition();
                recognition.start();
            } else {
                isRecording = false;
                recognition.stop();
            }
        });

        // Initialize on load
        document.addEventListener('DOMContentLoaded', function() {
            console.log("Speech component initialized");
        });
        </script>
    </div>
    """, height=200)

    # Textarea update handler
    components.html("""
    <script>
    window.addEventListener("message", (event) => {
        console.log("Message received in parent:", event.data);
        if (event.data && event.data.type === "speech_transcript") {
            const textareas = parent.document.querySelectorAll('textarea[aria-label="Your Question"]');
            if (textareas.length > 0) {
                const textarea = textareas[0];
                if (event.data.transcript) {
                    textarea.value = event.data.transcript;
                }
                
                // Trigger all necessary events
                const events = ['input', 'change', 'keyup', 'blur'];
                events.forEach(eventType => {
                    const evt = new Event(eventType, { bubbles: true });
                    textarea.dispatchEvent(evt);
                });
                
                console.log("Textarea updated with:", event.data.transcript);
            }
        }
    });
    </script>
    """)

# Text input area
user_query = st.text_area(
    "Your Question",
    value=st.session_state.user_query,
    key="user_input",
    height=120,
    placeholder="Speak or type your question here...",
    help="The text will be automatically filled when you use voice input"
)

# Update session state when text changes
if user_query != st.session_state.user_query:
    st.session_state.user_query = user_query

# AI Response section
if st.session_state.call_active and st.button("🔍 Get AI Response"):
    with st.spinner("🤖 Generating response..."):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"""You are a helpful call center assistant. Here's the context:\n{full_context}\n\nQuestion: {st.session_state.user_query}\nAnswer politely and conversationally:"""
            response = model.generate_content(prompt)
            st.session_state.ai_response = response.text
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

if st.session_state.ai_response:
    st.markdown("---")
    st.markdown("### 🤖 AI Response")
    st.markdown(st.session_state.ai_response)
    audio_file = text_to_speech(st.session_state.ai_response)
    st.audio(audio_file)
