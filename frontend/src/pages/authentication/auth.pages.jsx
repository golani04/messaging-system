import React from "react";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";

import SignIn from "../../components/sign-in/sign-in.component";


const SignInAndSignUpPage = () => (
    <Row>
        <Col md={6} className="mb-5 mb-sm-0">
            <SignIn />
        </Col>
    </Row>
);

export default SignInAndSignUpPage;
