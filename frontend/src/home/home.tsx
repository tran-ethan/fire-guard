import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './home.svelte'; // Import the Svelte component

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/home" element={<div id="svelte-root"></div>} />
        {/* Add more routes here as needed */}
      </Routes>
    </Router>
  );
}

ReactDOM.render(<App />, document.getElementById('root'));


const app = new Home({
  target: document.getElementById('app')!,
})
