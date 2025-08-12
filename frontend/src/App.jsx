
import React, {useState} from 'react';

export default function App(){
  const [q,setQ] = useState('');
  const [resp,setResp] = useState('');

  async function ask(){
    setResp('Thinking...');
    const r = await fetch('/api/ask', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ text: q })
    });
    const j = await r.json();
    setResp(JSON.stringify(j, null, 2));
  }

  return (
    <div style={{padding:20, fontFamily:'Arial, sans-serif'}}>
      <h1>Medical Multi-Tool AI</h1>
      <textarea value={q} onChange={e=>setQ(e.target.value)} rows={4} cols={80} placeholder="Ask a data question (e.g., 'average age heart disease') or medical question (e.g., 'symptoms of diabetes')"></textarea>
      <br/>
      <button onClick={ask} style={{marginTop:10}}>Ask</button>
      <pre style={{whiteSpace:'pre-wrap', marginTop:10}}>{resp}</pre>
    </div>
  );
}
