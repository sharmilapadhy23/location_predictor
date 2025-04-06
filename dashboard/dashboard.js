const API_KEY = '81bdb230e5e5201078981ef3d6493562';

    const weatherPlaceMapping = {
      'clear sky': ['Park', 'Outdoor Cafe', 'Zoo'],
      'few clouds': ['Park', 'Outdoor Cafe'],
      'scattered clouds': ['Museum', 'Art Gallery'],
      'broken clouds': ['Museum', 'Art Gallery'],
      'shower rain': ['Museum', 'Indoor Shopping Mall'],
      'rain': ['Museum', 'Indoor Shopping Mall'],
      'thunderstorm': ['Indoor Shopping Mall', 'Library'],
      'snow': ['Library', 'Coffee Shop'],
      'mist': ['Library', 'Coffee Shop']
    };

    async function getWeather() {
      const city = document.getElementById('cityInput').value.trim();
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
          const places = weatherPlaceMapping[condition] || [];

          resultDiv.style.display = 'block';
          resultDiv.innerHTML = `
            <div class="card">
              <p><strong>Condition:</strong> ${condition}</p>
              <p><strong>Temperature:</strong> ${temp}°C</p>
              <p><strong>Humidity:</strong> ${humidity}%</p>
              <p><strong>Wind Speed:</strong> ${wind} m/s</p>
            </div>

            <div class="cardd">
              <h3>Recommended Places <span>✦</span> </h3>
              ${
                places.length > 0
                  ? `<ul>${places.map(place => `<li>${place}</li>`).join('')}</ul>`
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
