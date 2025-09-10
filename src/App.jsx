
import { useState } from 'react';
import './App.css';
import Header from './components/Header';
import MainContent from './components/MainContent';
import Footer from './components/Footer';
import nlp from 'compromise';

function App() {
  const [text, setText] = useState("");
  const [displayedText, setDisplayedText] = useState("");
  const [nouns, setNouns] = useState([]);

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
            rows={8}
            cols={50}
          />
          <button
            onClick={() => {
              const t = nlp(text);
              setNouns(t.nouns().out('array'));
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
            <h3>Nouns:</h3>
            <ul>
              {nouns.map((noun, index) => (
                <li key={index}>{noun}</li>
              ))}
            </ul>
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
}

export default App;
