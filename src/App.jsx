import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [text, setText] = useState("");
  const [displayedText, setDisplayedText] = useState("");

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
    </>
  );
}

export default App
