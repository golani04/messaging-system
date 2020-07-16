import React from "react";

const FormInput = ({ id, label, ...props }) => (
    <div className="group">
        {<label class="form-input-label" htmlFor={id}>{label}</label> ? label : null}
        <input id={id} className="form-input" {...props} />
    </div>
);

export default FormInput;
