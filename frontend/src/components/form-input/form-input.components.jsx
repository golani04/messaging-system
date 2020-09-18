import React from "react";
import Form from "react-bootstrap/Form";

const CustomGroup = ({ id, label, ...props }) => (
    <Form.Group>
        {label ? <Form.Label className="form-input-label" htmlFor={id}>{label}</Form.Label> : null}
        <Form.Control id={id} {...props} />
    </Form.Group>
);

export default CustomGroup;
