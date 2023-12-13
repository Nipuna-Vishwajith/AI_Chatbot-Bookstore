const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql');
const cors = require('cors'); 

const app = express();
const PORT = 3002;
app.use(cors()); 

app.use(bodyParser.json());
app.use(express.json());
// Create a MySQL connection
const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '',
  database: 'book_orders',
});

// Connect to the MySQL database
connection.connect((err) => {
  if (err) {
    console.error('Error connecting to MySQL database:', err);
    return;
  }
  console.log('Connected to MySQL database');
});
connection.connect((err) => {
  if (err) {
    console.error('Error connecting to MySQL database:', err);
    return;
  }
  console.log('Connected to MySQL database');
});
// Route to receive order details from the main.py script
app.post('/orders', (req, res) => {
    const { orders } = req.body;
    console.log('Received order details from main.py:', orders);
  
    // Update the database with the received order details
    orders.forEach((order) => {
      const { book_id, telephone_number } = order;
  
      // Insert the order details into the 'orders' table (modify the SQL query as needed)
      const sql = `INSERT INTO orders (book_id, telephone_number) VALUES (?, ?)`;
      connection.query(sql, [book_id, telephone_number], (err, result) => {
        if (err) {
          console.error('Error inserting into the database:', err);
        } else {
          //console.log('Inserted into the database:', result);
        }
      });
    });
  
    // You can add logic to store or display the orders as needed
    res.sendStatus(200);
  });
  
 // Define an endpoint to get orders from the database
app.get('/api/orders', (req, res) => {
  // SQL query to select all rows from the 'orders' table
  const sql = 'SELECT * FROM orders';

  // Execute the SQL query
  connection.query(sql, (err, result) => {
      if (err) {
          // If there's an error with the MySQL query, log the error and send a 500 Internal Server Error response
          console.error('MySQL query error:', err);
          res.status(500).send('Internal Server Error');
      } else {
          // If the query is successful, send the result (data) as a JSON response
          res.json(result);
      }
  });
});

app.post('/api/complete-orders', async (req, res) => {
  const { bookId, telephoneNumber, username } = req.body;

  // Prepare SQL statements for transaction
  const insertSql = 'INSERT INTO complete_orders (book_id, telephone_number, username) VALUES (?, ?, ?)';
  const deleteSql = 'DELETE FROM orders WHERE book_id = ? AND telephone_number = ?';

  try {
    // Start transaction
    await connection.beginTransaction();

    // Execute insert statement
    await connection.query(insertSql, [bookId, telephoneNumber, username]);

    // Execute delete statement
    await connection.query(deleteSql, [bookId, telephoneNumber]);

    // Commit transaction on success
    await connection.commit();

    res.status(200).send('Data successfully updated.');
  } catch (error) {
    console.error('MySQL transaction error:', error);

    // Rollback transaction on error
    await connection.rollback();

    // Send error response
    res.status(500).send('Internal Server Error');
  }
});

  
  
  app.listen(PORT, () => {
    console.log(`Web server is running on http://localhost:${PORT}`);
  });