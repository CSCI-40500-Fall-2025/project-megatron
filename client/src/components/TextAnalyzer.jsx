import { useState } from 'react';
import nlp from 'compromise';

const apiKey = "";
const url = `https://translation.googleapis.com/language/translate/v2?key=${apiKey}`;

async function translateText(text, targetLang = "zh") {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      q: text,          // Text to translate
      target: targetLang, // Target language code (e.g., "es" for Spanish)
      format: "text"
    })
  });
  const data = await response.json();
  console.log("Translated text:", data.data.translations[0].translatedText);
  return data.data.translations[0].translatedText;
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
        onClick={() => {
          const t = nlp(text);
          setNouns(t.nouns().out('array'));
          setDisplayedText(translateText(text));
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
