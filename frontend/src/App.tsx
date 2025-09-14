import { useEffect, useState } from 'react'


function App() {
const [health, setHealth] = useState<any>(null)


useEffect(() => {
fetch(`${import.meta.env.VITE_API_BASE}/api/health`).then(r => r.json()).then(setHealth).catch(console.error)
}, [])


return (
<div style={{ padding: 24, fontFamily: 'ui-sans-serif' }}>
<h1>Invoice App — Hello World</h1>
<p>Backend health: {health ? JSON.stringify(health) : 'loading...'}</p>
</div>
)
}


export default App
