import React, { useState, useEffect } from "react";
import logo from './logo.svg';
import './App.css';

// 1. Get data from backend (current date).
//      --> This happens in my JavaScript.
//                • 1.1. Use Fetch API to retrieve data from some endpoint.
//                      ---> We just have to fetch from OUR OWN BACKEND ROUTES!
//                • 1.2. Create a state (`useState`) to store our retrieved backend data.
// 2. Render date in returned JSX.
//      --> This happens in my JSX/HTML. 
//                • 2.1. Load state data for datetime into relevant component or HTML container.























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
        <h2>The current date is <i>{currentDate}</i>.</h2>
      </header>
    </div>
  );
}

export default App;
