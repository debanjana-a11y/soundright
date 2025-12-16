import { useState, useRef } from 'react';
import './App.css';

function App() {
  const [recordingStatus, setRecordingStatus] = useState('idle');
  const [spokenWord, setSpokenWord] = useState('');
  const [statusMessage, setStatusMessage] = useState('Use Chrome browser. Press Speak to begin.');

  // Corrected TypeScript syntax for accessing the experimental Web Speech API on the window object
  const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
  
  // Corrected TypeScript syntax for useRef: define that it can hold a SpeechRecognition object or null
  const recognitionRef = useRef<any | null>(null); // Using 'any' for simplicity if not using a full TS setup

  const startRecording = () => {
    if (!SpeechRecognition) {
        setStatusMessage('Browser does not support the Web Speech API. Use Google Chrome.');
        return;
    }

    setSpokenWord('');
    setRecordingStatus('recording');
    setStatusMessage('🔴 Listening... Speak now!');

    recognitionRef.current = new SpeechRecognition();
    recognitionRef.current.continuous = false; // Stop after one phrase
    recognitionRef.current.interimResults = false;
    recognitionRef.current.lang = 'en-US';

    recognitionRef.current.onresult = (event: any) => {
      // Get the actual transcribed text result
      const transcribedText = event.results[0][0].transcript;
      setSpokenWord(transcribedText);
      setStatusMessage(`Transcription successful:`);
      setRecordingStatus('idle');
    };

    recognitionRef.current.onerror = (event: any) => {
      console.error('Speech recognition error:', event.error);
      setStatusMessage(`Error recognizing speech: ${event.error}`);
      setRecordingStatus('idle');
    };
    
    recognitionRef.current.onend = () => {
        // Handle cases where recording stops without a result (e.g., user silence)
        if (recordingStatus !== 'idle') {
            setRecordingStatus('idle');
        }
    };

    recognitionRef.current.start();
  };

  const stopRecording = () => {
    if (recognitionRef.current && recordingStatus === 'recording') {
      recognitionRef.current.stop();
      // Status change is handled by the onend callback
    }
  };


  return (
    <div className="App">
      <header>
        <h1>PronounceRight</h1>
      </header>

      <div className="card">
        <button 
          onClick={recordingStatus === 'recording' ? stopRecording : startRecording}
          className={recordingStatus === 'recording' ? 'recording-active' : ''}
          disabled={recordingStatus === 'processing'} 
        >
          {recordingStatus === 'recording' ? 'Stop Speaking' : 'Speak a Word'}
        </button>
        
        <p className="status-message">{statusMessage}</p>

        {spokenWord && (
          <div className="result-box">
            <h2>You said:</h2>
            <p className="word-display">"{spokenWord}"</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
