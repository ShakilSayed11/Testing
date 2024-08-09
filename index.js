const express = require('express');
const { createClient } = require('@supabase/supabase-js');
const path = require('path');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

// Supabase client setup
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);

// Serve static files
app.use(express.static(path.join(__dirname, 'public')));

// Middleware to parse JSON
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/data', async (req, res) => {
    const { data, error } = await supabase.from('attendance').select('*');
    if (error) return res.status(500).json({ error: 'Error fetching data' });
    
    res.json(data);
});

app.post('/update', async (req, res) => {
    const { id, dateColumn, newValue } = req.body;
    const { data, error } = await supabase
        .from('attendance')
        .update({ [dateColumn]: newValue })
        .eq('id', id);

    if (error) {
        return res.status(500).json({ status: 'error', message: error.message });
    }
    res.json({ status: 'success', data });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
