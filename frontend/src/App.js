import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [email, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [tokens, setTokens] = useState('');


  const handleSubmit = async e => {
    e.preventDefault();

    const user = { email, password };
    const response = await axios.post('/auth/login', user);

    // get
    setTokens(response.data);
  };

  if (tokens) {
    return <div>User is logged in.</div>;
  }


  return (
    <div className="App">
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="username">Email: </label>
          <input type="email" value={email} placeholder="enter an email" onChange={({ target }) => setUsername(target.value)} />
        </div>
        <div>
          <label htmlFor="username">Password: </label>
          <input type="password" value={password} placeholder="enter a password" onChange={({ target }) => setPassword(target.value)} />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default App;
