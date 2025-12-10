import { useState } from 'react';
const API = import.meta.env.VITE_API_URL;

export default function Generate() {
    const [text, setText] = useState("");
    const [generatedText, setParagraph] = useState("");
    //generateText("dogs");
    async function generateText(){
    const res = await fetch((`${API}generate`), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
        text: text,
        })
    });
    const data = await res.json();
    console.log(data.text);
    setText(data.text)
    }

    return (
        <>  
        <textarea
            placeholder="Input text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={8}
            cols={50}
        />
        <button onClick={generateText}> Generate </button>
        {/* {generatedText && (
        <div className="mt-3 p-3 border rounded bg-gray-50">
          <strong>Text:</strong> {generatedText}
        </div>
      )} */}
        </>
    )
}
