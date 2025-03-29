# 📍RoamEase - Nextstep Predictor

## 🚀 Project Overview
This is an interactive location-based platform designed to help users quickly locate nearby emergency services such as hospitals, police stations, fire departments, and pharmacies. It integrates real-time maps with emergency response functionalities, providing an efficient and accessible solution for public safety, disaster management, and healthcare accessibility.

The system uses:
- **OpenStreetMap's Overpass API** and **Google Places API** to fetch nearby emergency services.
- **React.js**, **JavaScript**, and **Leaflet.js** (or **Google Maps API**) for a dynamic and seamless user interface.
- **Real-time location tracking** and interactive markers for enhanced accessibility and decision-making during critical situations.

---

## 🔥 **Key Features**
✅ **Real-Time Location Tracking:**  
- Displays the user's current location on the map.  
- Automatically fetches nearby emergency services.

✅ **Emergency Service Markers:**  
- Shows hospitals, police stations, fire departments, and pharmacies with distinct icons.  
- Clickable markers provide additional information (e.g., name, contact info).

✅ **Dynamic Map Integration:**  
- Uses **Leaflet.js** (OpenStreetMap) or **Google Maps API** for responsive, interactive map rendering.  
- Smooth panning, zooming, and real-time updates.

✅ **Flexible Data Sources:**  
- Supports both **free OpenStreetMap data** and **premium Google Places API**, allowing scalability based on usage.  

✅ **User-Friendly Interface:**  
- Clean and responsive UI with intuitive navigation.  
- Optimized for both desktop and mobile devices.  

✅ **AI-Powered Future Enhancements:**  
- Includes provisions for AI-based **predictive modeling** and **risk assessments**.  
- Potential for **voice-activated searches** and **IoT integration**.

---

## 🛠️ **Tech Stack**
- **Frontend:** React.js, JavaScript, HTML, CSS  
- **Mapping Libraries:** Leaflet.js / Google Maps API  
- **Backend:** Python (for AI and predictive modeling)  
- **APIs:** OpenStreetMap Overpass API, Google Places API  
- **Geospatial Tech:** GIS-based data visualization  

---

## 🔧 **Installation and Setup**
### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/your-username/emergency-service-finder.git
cd emergency-service-finder
```

### 2️⃣ **Install Dependencies**
Run the following command to install the required dependencies:
```bash
npm install
```

### 3️⃣ **API Keys Setup**
- Sign up for the **Google Places API** and obtain an API key.  
- Add the key to your `.env` file:
```
REACT_APP_GOOGLE_MAPS_API_KEY=YOUR_API_KEY
```
- For OpenStreetMap, no key is required for public use.  

### 4️⃣ **Start the Development Server**
```bash
npm start
```
- The application will be accessible at:  
  `http://localhost:3000`

---

## ⚙️ **Folder Structure**
```
/public               → Static assets  
/src                  → Source code  
 ├── /components      → Reusable React components  
 ├── /services        → API call handlers  
 ├── /assets          → Icons, images, and styles  
 ├── App.js           → Main React component  
 ├── index.js         → React DOM rendering  
.env                  → API keys configuration  
package.json          → Project dependencies  
README.md             → Project documentation  
```

---

## 🛡️ **Usage Instructions**
1. **Launch the application** to see your current location on the map.  
2. Click the **"Find Services"** button to display nearby emergency services.  
3. Interact with the **markers** to view service details (name, address, contact info).  
4. Use the **zoom and pan** controls to navigate the map.  

---

## 🚀 **Deployment**
To build the project for production:
```bash
npm run build
```
Deploy it to a hosting service such as:
- **Vercel**  
- **Netlify**  
- **GitHub Pages**  

---

## 📌 **Future Enhancements**
- 🌐 **Voice-Activated Search:** Locate services using voice commands.  
- 🤖 **AI-Powered Risk Assessment:** Predict emergency needs based on real-time data.  
- 🔥 **IoT Integration:** Connect with IoT devices for live incident reporting.  
- 📊 **Advanced Data Visualization:** Use charts and heatmaps for better insights.

