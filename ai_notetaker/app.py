import streamlit as st
import os
from meeting_recorder import MeetingRecorder
import time
from datetime import datetime
import base64

# Initialize session state variables
if 'recorder' not in st.session_state:
    st.session_state.recorder = None
if 'recording' not in st.session_state:
    st.session_state.recording = False
if 'latest_recording' not in st.session_state:
    st.session_state.latest_recording = None
if 'playing_audio' not in st.session_state:
    st.session_state.playing_audio = False

def get_audio_player_html(audio_path):
    """Generate HTML for audio player with custom styling"""
    audio_placeholder = st.empty()
    with open(audio_path, 'rb') as audio_file:
        audio_bytes = audio_file.read()
    audio_base64 = base64.b64encode(audio_bytes).decode()
    audio_player = f"""
        <audio id="audio-player" style="width: 100%;" controls>
            <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
            Your browser does not support the audio element.
        </audio>
    """
    return audio_player

def main():
    st.title("AI Meeting Note Taker")
    st.write("Record, transcribe, and summarize your meetings with ease!")

    # Check for Google Cloud credentials
    # if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
    #     st.error("Google Cloud credentials not found. Please set GOOGLE_APPLICATION_CREDENTIALS environment variable.")
    #     return

    # Get or prompt for API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        api_key = st.text_input("Enter your Google API key:", type="password")
        if not api_key:
            st.warning("Please enter your Google API key to continue.")
            return

    # Initialize recorder if not already done
    if st.session_state.recorder is None:
        st.session_state.recorder = MeetingRecorder(api_key)

    # Create columns for buttons
    col1, col2, col3, col4 = st.columns(4)

    # Record button
    with col1:
        if not st.session_state.recording:
            if st.button("🎙️ Start Recording"):
                st.session_state.recording = True
                st.session_state.recorder.start_recording()
                st.experimental_rerun()

    # Stop button
    with col2:
        if st.session_state.recording:
            if st.button("⏹️ Stop Recording"):
                st.session_state.recording = False
                st.session_state.recorder.stop_recording()
                st.session_state.latest_recording = st.session_state.recorder.latest_audio_file
                st.experimental_rerun()

    # Status indicator
    status_placeholder = st.empty()
    if st.session_state.recording:
        status_placeholder.warning("🔴 Recording in progress...")
    else:
        status_placeholder.info("⚪ Ready to record")

    # Display audio player and transcription results
    if st.session_state.latest_recording and os.path.exists(st.session_state.latest_recording):
        st.subheader("Latest Recording")
        st.markdown(get_audio_player_html(st.session_state.latest_recording), unsafe_allow_html=True)

        # Get the timestamp from the filename
        timestamp = st.session_state.latest_recording.split('_')[-1].replace('.wav', '')
        
        # Check for corresponding document and JSON files
        doc_file = f"meeting_notes_{timestamp}.docx"
        json_file = f"meeting_notes_{timestamp}.json"

        if os.path.exists(doc_file):
            st.download_button(
                label="📄 Download Word Document",
                data=open(doc_file, 'rb'),
                file_name=doc_file,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        if os.path.exists(json_file):
            st.download_button(
                label="📋 Download JSON",
                data=open(json_file, 'rb'),
                file_name=json_file,
                mime="application/json"
            )

if __name__ == "__main__":
    main()
