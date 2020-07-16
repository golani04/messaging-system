import React from "react";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";

import SignIn from "../../components/sign-in/sign-in.component";


const SignInAndSignUpPage = () => (
    <Row>
        <Col>
            <div className="sign-in-and-sign-up">
                <SignIn />
            </div>
        </Col>
        <Col>
            <div className="sign-in-and-sign-up">
                <SignIn />
            </div>
        </Col>
    </Row>
);

export default SignInAndSignUpPage;
