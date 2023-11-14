import React, { useState, useEffect } from "react";
import logo from './logo.svg';
import './App.css';

function App() {
  const [currentDate, setCurrentDate] = useState("");

  useEffect(() => {
    fetch("/date")
      .then(response => response.json())
      .then(dateData => setCurrentDate(dateData.date))
      .catch(error => console.error(error));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>The current date is {currentDate}.</p>
      </header>
    </div>
  );
}

export default App;
