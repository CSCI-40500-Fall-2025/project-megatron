import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import nlp from 'compromise'

function App() {
  const [text, setText] = useState("");
  const [displayedText, setDisplayedText] = useState("");
  const [nouns, setNouns] = useState([]);

  return (
    <>
      <div className="card">
        <textarea
          placeholder="Input text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={8}   // number of visible lines
          cols={50}  // width of the box
        />
        <br />
        <button
          onClick={() => {
            const t = nlp(text);
            setNouns(t.nouns().out('array'));
            console.log(nouns); 
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
    </>
  );
}

export default App
