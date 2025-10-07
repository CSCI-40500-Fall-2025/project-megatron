import { useState } from 'react';
import nlp from 'compromise';

const API = import.meta.env.VITE_API_URL;

async function translateText(text,  targetLang = "zh", nouns, verbs) {
  const response = await fetch(`${API}translate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      text: text,          // Text to translate
      target: targetLang, // Target language code (e.g., "es" for Spanish)
      nouns: nouns, // Translated nouns
      verbs: verbs, // Translated verbs
    })
  });
  const data = await response.json();
  console.log("Translated text:", data.translatedText);
  console.log("Translated nouns:", data.translatedNouns);
  console.log("Translated verbs:", data.translatedVerbs);
  return data;
}

function replaceWordsInText(text, map) {
  let modifiedText = text;
  for (const [original, translated] of Object.entries(map)) {
    const regex = new RegExp(`\\b${original}\\b`, 'g'); // using regex with word boundary and global flag to match all instances of whole words only
    modifiedText = modifiedText.replace(regex, translated);
  }
  return modifiedText;
}

function TextAnalyzer() {
  const [text, setText] = useState("");
  const [displayedText, setDisplayedText] = useState("");
  const [nouns, setNouns] = useState([]);
  const [verbs, setVerbs] = useState([]);
  const [replace, setReplace] = useState("noun"); // keeps track of what part of speech is getting replaced - for ex: "noun" or "verb"
  //const [nounMap, setNounMap] = useState({}); // Map of original to translated nouns

  return (
    <div className="card">
      <p>I'm looking to learn:</p>
      <select value={replace} onChange={(e) => setReplace(e.target.value)}>
        <option value="noun">Nouns</option>
        <option value="verb">Verbs</option>
      </select>
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
          const extractedVerbs = t.verbs().out('array');
          const data = await translateText(text, "zh", extractedNouns, extractedVerbs);

          //setDisplayedText(data.translatedText);
          setNouns(data.translatedNouns);
          setVerbs(data.translatedVerbs);

          const nounMap = {};
          data.translatedNouns.forEach(({ original, translated }) => {
            nounMap[original] = translated;
          });
          const verbMap = {};
          data.translatedVerbs.forEach(({ original, translated }) => {
            verbMap[original] = translated;
          });
          const modifiedText = replace === "noun" ? replaceWordsInText(text, nounMap) : replaceWordsInText(text, verbMap);
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
          <h3>Verbs:</h3>
          <ul>
            {verbs.map((verb, index) => (
              <li key={index}>
                Original Language: {verb.original} → Translated Language: {verb.translated}
                </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default TextAnalyzer;
