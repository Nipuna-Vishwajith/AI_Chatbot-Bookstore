import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './home.css'; 
//import './App.css'; // Import the CSS file for styling

function Home() {
    const [orders, setOrders] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:3002/api/orders')
            .then(response => setOrders(response.data))
            .catch(error => console.error('API request error:', error));
    }, []);

    return (
        <div className="container">
            <h1 className='h1'>Telegram - AI powered Chatbot</h1>
            <h2> Handle Book Orders</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Book ID</th>
                        <th>Telephone Number</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {orders.map(order => (
                        <tr key={order.id}>
                            <td>{order.id}</td>
                            <td>{order.book_id}</td>
                            <td>{order.telephone_number}</td>
                            <td>
                                {/* "Next" button linking to the "process" route with parameters */}
                                <Link to={`/process/${order.book_id}/${order.telephone_number}`}>
                                    <button className='btn'>Next</button>
                                </Link>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default Home;