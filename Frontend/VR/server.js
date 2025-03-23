// Use ESM import statements
import express from 'express';
import axios from 'axios';
import cors from 'cors';

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Free Unsplash API Key
const UNSPLASH_ACCESS_KEY = 'szNd4tN0c5TTTpBTXCmD038rlke4DW3w3smkKcm-zEQ'; // Replace with your Unsplash API key

// Route to fetch location images
app.get('/image/:location', async (req, res) => {
  const location = req.params.location;

  try {
    const response = await axios.get(`https://api.unsplash.com/photos/random`, {
      params: {
        query: location,
        client_id: UNSPLASH_ACCESS_KEY
      }
    });

    const imageUrl = response.data.urls.regular;
    res.json({ imageUrl });
  } catch (error) {
    console.error('Error fetching image:', error);
    res.status(500).json({ error: 'Failed to fetch image' });
  }
});

// Start server
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
