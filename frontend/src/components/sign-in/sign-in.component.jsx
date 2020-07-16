import React from "react";
import FormInput from "../form-input/form-input.components";


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

    render() {
        return (
            <div className="sign-in">
                <h2>I already have an account</h2>
                <p><small>Sign in with email and password</small></p>

                <form onSubmit={this.handleSubmit}>
                    <FormInput type="email" value={this.state.email} id="sign-in-username" label="Email" required />
                    <FormInput type="password" value={this.state.password} id="sign-in-password" label="Password" required />

                    <div className="sign-in-submit">
                        <button type="submit">Submit</button>
                    </div>

                </form>
            </div>
        );
    }
}

export default SignIn;
