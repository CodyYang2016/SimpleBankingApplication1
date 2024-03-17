import React, { useState } from 'react';

const RegistrationForm = () => {
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        email: '',
        raw_password: ''
    });

    const handleInputChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/customers/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            if (response.ok) {
                // Registration successful, redirect to login page
                console.log('Registration successful');
            } else {
                // Registration failed, handle error response
                const errorData = await response.json();
                console.error('Registration failed:', errorData);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="text" name="first_name" value={formData.first_name} onChange={handleInputChange} placeholder="First Name" />
            <input type="text" name="last_name" value={formData.last_name} onChange={handleInputChange} placeholder="Last Name" />
            <input type="email" name="email" value={formData.email} onChange={handleInputChange} placeholder="Email" />
            <input type="password" name="raw_password" value={formData.raw_password} onChange={handleInputChange} placeholder="Password" />
            <button type="submit">Register</button>
        </form>
    );
};

export default RegistrationForm;
