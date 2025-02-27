# AI Meeting Note Taker

This application automatically records, transcribes, and summarizes your meetings. It creates comprehensive documents containing both the full transcript and a concise summary of key points.

## Features

- Audio recording from system audio and microphone
- High-quality speech-to-text transcription using Google Cloud Speech-to-Text
- AI-powered meeting summarization using Google Gemini
- Automatic document generation in multiple formats:
  - Word document (.docx) with formatted transcript and summary
  - JSON file with structured data
- Simple keyboard controls

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Google Cloud:
   - Create a Google Cloud project
   - Enable the Speech-to-Text API
   - Create a service account and download the JSON key file
   - Set the environment variable: `GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json`

3. Set up your Google API key:
   - Either set it as an environment variable: `GOOGLE_API_KEY=your_api_key`
   - Or enter it when prompted by the application

## Usage

1. Run the application:
```bash
python main.py
```

2. Use the following keyboard controls:
   - Press 'r' to start recording
   - Press 's' to stop recording and generate notes
   - Press 'q' to quit the application

3. The application will generate:
   - A WAV file of the recording: `meeting_recording_YYYYMMDD_HHMMSS.wav`
   - A Word document with formatted content: `meeting_notes_YYYYMMDD_HHMMSS.docx`
   - A JSON file with structured data: `meeting_notes_YYYYMMDD_HHMMSS.json`

## Output Files

### Word Document (.docx)
Contains a formatted version of:
- Meeting timestamp
- AI-generated concise summary
- Full transcript

### JSON File
Contains structured data with:
- timestamp
- summary
- transcript

## Requirements

- Python 3.7+
- Google API key for Gemini
- Google Cloud service account with Speech-to-Text API enabled
- Microphone access
- System audio access
