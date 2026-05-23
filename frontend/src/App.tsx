import { useState } from "react";
import "./App.css";

type PredictResponse = {
  text: string;
  label: string;
  score: number;
};

function App() {
  const [text, setText] = useState("This product is excellent");
  const [result, setResult] = useState<PredictResponse | null>(null);
  const [loading, setLoading] = useState(false);
  //Analyzeボタンが押されたときに実行される関数
  //asyncこの関数の中で非同期処理をすることを宣言
  const handlePredict = async () => {
    setLoading(true);
    setResult(null);
    //fetch はブラウザ標準のHTTP通信機能
    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    });
    
    const data: PredictResponse = await response.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <main>
      <h1>AI Sentiment API</h1>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={5}
        cols={50}
      />

      <br />

      <button onClick={handlePredict} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {result && (
        <section>
          <h2>Result</h2>
          <p>Text: {result.text}</p>
          <p>Label: {result.label}</p>
          <p>Score: {result.score}</p>
        </section>
      )}
    </main>
  );
}

export default App;
