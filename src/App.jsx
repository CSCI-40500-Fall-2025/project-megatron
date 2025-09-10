
import { useState } from 'react';
import './App.css';
import Header from './components/Header';
import MainContent from './components/MainContent';
import Footer from './components/Footer';

function App() {
  const [text, setText] = useState("");
  const [displayedText, setDisplayedText] = useState("");

  return (
    <div className="app-container">
      <Header />
      <main className="main-content">
        <MainContent />
        <div className="card">
          <textarea
            placeholder="Input text"
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <button
            onClick={() => {
              setDisplayedText(text);
            }}
          >
            Translate
          </button>
        </div>
        {displayedText && (
          <div className="displayed-text">
            <h2>Translation:</h2>
            <p>{displayedText}</p>
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
}

export default App;
