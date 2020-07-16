import React from 'react';
import Container from 'react-bootstrap/Container';
import SignInAndSignUpPage from './pages/authentication/auth.pages';

function App() {
  return (
    <Container>
      {/* Header */}
      <SignInAndSignUpPage />
      {/* Footer */}
    </Container>
  );

  // add router to handle navigation between logged in user and anonymous
}

export default App;
