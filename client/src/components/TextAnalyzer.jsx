import { useState } from 'react';
import nlp from 'compromise';

const API = import.meta.env.VITE_API_URL;

async function translateText(text,  targetLang = "zh", nouns) {
  const response = await fetch(`${API}translate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      text: text,          // Text to translate
      target: targetLang, // Target language code (e.g., "es" for Spanish)
      nouns: nouns, // Translated nouns
    })
  });
  const data = await response.json();
  console.log("Translated text:", data.translatedText);
  console.log("Translated nouns:", data.translatedNouns)
  return data;
}

function replaceNounsInText(text, nounMap) {
  let modifiedText = text;
  for (const [original, translated] of Object.entries(nounMap)) {
    const regex = new RegExp(`\\b${original}\\b`, 'g'); // using regex with word boundary and global flag to match all instances of whole words only
    modifiedText = modifiedText.replace(regex, translated);
  }
  return modifiedText;
}

function TextAnalyzer() {
  const [text, setText] = useState("");
  const [displayedText, setDisplayedText] = useState("");
  const [nouns, setNouns] = useState([]);
  //const [nounMap, setNounMap] = useState({}); // Map of original to translated nouns

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
          const extractedNouns = t.nouns().out('array');
          const data = await translateText(text, "zh", extractedNouns);

          //setDisplayedText(data.translatedText);
          setNouns(data.translatedNouns);

          const map = {};
          data.translatedNouns.forEach(({ original, translated }) => {
            map[original] = translated;
          });
          //setNounMap(map);
          const modifiedText = replaceNounsInText(text, map);
          setDisplayedText(modifiedText);
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
              <li key={index}>
                Original Language: {noun.original} → Translated Language: {noun.translated}
                </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default TextAnalyzer;
