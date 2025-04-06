const API_KEY = '81bdb230e5e5201078981ef3d6493562';

// Weather + City based place suggestions
const combinedWeatherCityData = {
  'Bhubaneswar': {
    'clear sky': [
      { name: 'Cafe Coffee Day', location: 'Infocity' },
      { name: 'Nandankanan Zoological Park', location: 'Chandaka' }
    ],
    'few clouds': [
      { name: 'Cafe Coffee Day', location: 'Infocity' }
    ],
    'scattered clouds': [
      { name: 'Odisha State Museum', location: 'Kalpana Square' },
      { name: 'Kalinga Art Gallery', location: 'Kharavela Nagar' }
    ],
    'broken clouds': [
      { name: 'Odisha State Museum', location: 'Kalpana Square' },
      { name: 'Kalinga Art Gallery', location: 'Kharavela Nagar' }
    ],
    'shower rain': [
      { name: 'Odisha State Museum', location: 'Kalpana Square' },
      { name: 'Esplanade One', location: 'Rasulgarh' }
    ],
    'rain': [
      { name: 'Odisha State Museum', location: 'Kalpana Square' },
      { name: 'Esplanade One', location: 'Rasulgarh' }
    ],
    'thunderstorm': [
      { name: 'Esplanade One', location: 'Rasulgarh' },
      { name: 'Bhubaneswar Public Library', location: 'BJB Nagar' }
    ],
    'snow': [
      { name: 'Bhubaneswar Public Library', location: 'BJB Nagar' },
      { name: 'Barista', location: 'Saheed Nagar' }
    ],
    'mist': [
      { name: 'Bhubaneswar Public Library', location: 'BJB Nagar' },
      { name: 'Barista', location: 'Saheed Nagar' }
    ]
  },
  'Puri': {
    'clear sky': [
      { name: 'Honey Bee Cafe', location: 'CT Road' }
    ],
    'few clouds': [
      { name: 'Honey Bee Cafe', location: 'CT Road' }
    ],
    'scattered clouds': [
      { name: 'Sudharshan Craft Museum', location: 'Station Road' },
      { name: 'Raghurajpur Artist Village', location: 'Raghurajpur' }
    ],
    'broken clouds': [
      { name: 'Sudharshan Craft Museum', location: 'Station Road' },
      { name: 'Raghurajpur Artist Village', location: 'Raghurajpur' }
    ],
    'shower rain': [
      { name: 'Sudharshan Craft Museum', location: 'Station Road' },
      { name: 'Puri Grand Mall', location: 'VIP Road' }
    ],
    'rain': [
      { name: 'Sudharshan Craft Museum', location: 'Station Road' },
      { name: 'Puri Grand Mall', location: 'VIP Road' }
    ],
    'thunderstorm': [
      { name: 'Puri Grand Mall', location: 'VIP Road' },
      { name: 'District Library Puri', location: 'Grand Road' }
    ],
    'snow': [
      { name: 'District Library Puri', location: 'Grand Road' },
      { name: 'The Tea Pot', location: 'Chakratirtha Road' }
    ],
    'mist': [
      { name: 'District Library Puri', location: 'Grand Road' },
      { name: 'The Tea Pot', location: 'Chakratirtha Road' }
    ]
  }
};

// Get recommended places for a city and weather condition
function getRecommendedPlaces(city, condition) {
  const cityData = combinedWeatherCityData[city];
  if (!cityData) {
    console.warn('No data for city:', city);
    return [];
  }

  return cityData[condition] || [];
}

// Fetch weather and show recommendations
async function getWeather() {
  const cityInput = document.getElementById('cityInput');
  const city = cityInput.value.trim();
  const resultDiv = document.getElementById('result');

  if (!city) {
    alert('Please enter a city name');
    return;
  }

  const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${API_KEY}&units=metric`;

  try {
    const response = await fetch(url);
    const data = await response.json();

    if (response.ok) {
      const condition = data.weather[0].description.toLowerCase();
      const temp = data.main.temp;
      const humidity = data.main.humidity;
      const wind = data.wind.speed;

      const recommendedPlaces = getRecommendedPlaces(city, condition);

      resultDiv.style.display = 'block';
      resultDiv.innerHTML = `
        <h2 class="location-title">Weather & Recommendations for <span style="color: #4CAF50;">${city}</span></h2>

        <div class="card">
          <p><strong>Condition:</strong> ${condition}</p>
          <p><strong>Temperature:</strong> ${temp}°C</p>
          <p><strong>Humidity:</strong> ${humidity}%</p>
          <p><strong>Wind Speed:</strong> ${wind} m/s</p>
        </div>

        <div class="card">
          <h3>Recommended Places <span>✦</span></h3>
          ${
            recommendedPlaces.length > 0
              ? `<ul>${recommendedPlaces.map(place => `
                  <li><strong>${place.name}</strong>, ${place.location}</li>
                `).join('')}</ul>`
              : '<p>No specific recommendations for this weather condition.</p>'
          }
        </div>
      `;
    } else {
      alert(data.message || 'Weather not found.');
      resultDiv.style.display = 'none';
    }
  } catch (error) {
    console.error('Error:', error);
    alert('Something went wrong. Please try again.');
  }
}
