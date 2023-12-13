import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './process.css'; 

import { useNavigate } from 'react-router-dom';

function Process() {
    const { bookId, telephoneNumber } = useParams();
    const [username, setUsername] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
    
        // Send data to the server for insertion
        try {
            await axios.post('http://localhost:3000/api/complete-orders', {
                bookId: bookId,
                telephoneNumber: telephoneNumber,
                username: username,
            });

            console.log('Data successfully submitted!');
            
            navigate('/');
        } catch (error) {
            console.error('Error submitting data:', error);
        }
    };
    

    return (
        <div className="pcontainer">
            <Link to="/"><button className='btnBack'>Back</button></Link>
            <h3>Click Submit to Take the Order</h3>
            <p>Book ID: {bookId}</p>
            <p>Telephone Number: {telephoneNumber}</p>

            {/* Form for username submission */}
            <form onSubmit={handleSubmit}>
                <label>
                    Username:
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </label>
                <button type="submit">Submit</button>
                
            </form>
            
        </div>

    );
}

export default Process;
