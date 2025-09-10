import { useState } from 'react';
import nlp from 'compromise';

async function translateText(text, targetLang = "zh") {
  const response = await fetch("http://127.0.0.1:8000/translate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      text: text,          // Text to translate
      target: targetLang, // Target language code (e.g., "es" for Spanish)
    })
  });
  const data = await response.json();
  console.log("Translated text:", data.translatedText);
  return data.translatedText;
}

function TextAnalyzer() {
  const [text, setText] = useState("");
  const [displayedText, setDisplayedText] = useState("");
  const [nouns, setNouns] = useState([]);

  return (
    <div className="card">
      <textarea
        placeholder="Input text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={8}
        cols={50}
      />
      <button
        onClick={async () => {
          const t = nlp(text);
          setNouns(t.nouns().out('array'));
          const translation = await translateText(text, "zh");
          setDisplayedText(translation);
        }}
      >
        Translate
      </button>
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
    </div>
  );
}

export default TextAnalyzer;
