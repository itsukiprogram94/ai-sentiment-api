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
  const [error, setError] = useState<string | null>(null);
  //Analyzeボタンが押されたときに実行される関数
  //asyncこの関数の中で非同期処理をすることを宣言
  const handlePredict = async () => {
    setLoading(true);
    setResult(null);
    setError(null);
    try {
      //fetch はブラウザ標準のHTTP通信機能
      const response = await fetch("/api/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });
      //response.ok は、HTTPステータスコードが 200〜299 のとき trueを返すプロパティ
      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
      }
      const data: PredictResponse = await response.json();
      setResult(data);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Unknown error occurred");
      }
    //絶対に実行されるコードをfinallyブロックに書く
    } finally {
      setLoading(false);
    }
  };
  const getLabelClassName = (label: string) => {
    if (label === "positive") return "label label-positive";
    if (label === "negative") return "label label-negative";
    return "label label-neutral";
  };

  return (
    <main className="page">
      <section className="card">
        <div className="header">
          <p className="eyebrow">FastAPI × React × TypeScript</p>
          <h1>AI Sentiment Web App</h1>
          <p className="description">
          英文を入力して、その文が肯定的、否定的、中立的かどうかを分析します。
          </p>
        </div>

        <div className="form-area">
          <label htmlFor="text-input">テキストを入力してください</label>
          <textarea
            id="text-input"
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={6}
            placeholder="Type a sentence..."
          />

          <button onClick={handlePredict} disabled={loading || text.trim() === ""}>
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </div>

        {error && (
          <section className="message error-box">
            <h2>Error</h2>
            <p>{error}</p>
          </section>
        )}

        {result && (
          <section className="message result-box">
            <h2>Result</h2>

            <div className="result-row">
              <span className="result-label">Label</span>
              <span className={getLabelClassName(result.label)}>
                {result.label}
              </span>
            </div>

            <div className="result-row">
              <span className="result-label">Score</span>
              <span>{result.score}</span>
            </div>

            <div className="analyzed-text">
              <span className="result-label">Analyzed text</span>
              <p>{result.text}</p>
            </div>
          </section>
        )}
      </section>
    </main>
  );
}

export default App;