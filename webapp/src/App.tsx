import './App.css'

import WebApp from '@twa-dev/sdk'

function App() {
  return (
    <>
      <div className="card">
        <button onClick={() => WebApp.showAlert(`Hello World`)}>
          Show Alert
        </button>
      </div>
    </>
  )
}

export default App
