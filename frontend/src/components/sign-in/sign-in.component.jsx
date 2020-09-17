import React from "react";
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";
import CustomGroup from "../form-input/form-input.components";


class SignIn extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            email: '',
            password: ''
        }
    }

    handleSubmit = async (e) => {
        e.preventDefault();

        // check if example exists
        console.log(e);
    }

    handleChange = (e) => {
        console.log(e);
    }

    render() {
        return (
            <Card className="sign-in">
                <Card.Header>
                    <h2>I already have an account</h2>
                    <p><small>Sign in with email and password</small></p>
                </Card.Header>

                <Card.Body>
                    <Form onSubmit={this.handleSubmit}>
                        <CustomGroup onChange={this.handleChange} type="email" value={this.state.email} id="sign-in-username" label="Email" required />
                        <CustomGroup onChange={this.handleChange} type="password" value={this.state.password} id="sign-in-password" label="Password" required />

                        <Row className="sign-in-submit">
                            <Col><Button variant="outline-primary">Register</Button></Col>
                            <Col><Button variant="primary">Sign in</Button></Col>
                        </Row>

                    </Form>
                </Card.Body>
            </Card>
        );
    }
}

export default SignIn;
