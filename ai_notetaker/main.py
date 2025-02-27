from meeting_recorder import MeetingRecorder
from pynput import keyboard
import os

def main():
    # Get Google API key from environment variable
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        api_key = input("Please enter your Google API key: ")
    
    # Set up Google Cloud credentials
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not credentials_path:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        print("Please set it to the path of your Google Cloud service account key file.")
        return
    
    recorder = MeetingRecorder(api_key)
    
    def on_press(key):
        try:
            # Press 'r' to start recording
            if key.char == 'r':
                recorder.start_recording()
            # Press 's' to stop recording
            elif key.char == 's':
                recorder.stop_recording()
            # Press 'q' to quit
            elif key.char == 'q':
                return False
        except AttributeError:
            pass

    print("AI Note Taker")
    print("Controls:")
    print("Press 'r' to start recording")
    print("Press 's' to stop recording")
    print("Press 'q' to quit")

    # Listen for keypress
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
