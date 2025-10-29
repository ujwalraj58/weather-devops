document.getElementById("getBtn").addEventListener("click", getWeather);

async function getWeather() {
  const city = document.getElementById("city").value.trim();
  if (!city) return alert("Please enter a city name!");

  const geoRes = await fetch(`https://geocoding-api.open-meteo.com/v1/search?name=${city}&count=1`);
  const geoData = await geoRes.json();

  if (!geoData.results) return alert("City not found!");

  const { latitude, longitude, name, country } = geoData.results[0];
  document.getElementById("cityName").textContent = `${name}, ${country}`;

  const weatherRes = await fetch(
    `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,weather_code&timezone=auto`
  );
  const weatherData = await weatherRes.json();

  const current = weatherData.current;
  const daily = weatherData.daily;

  document.getElementById("temp").textContent = `${current.temperature_2m}°C`;
  document.getElementById("feelsLike").textContent = `${current.apparent_temperature}°C`;
  document.getElementById("humidity").textContent = `${current.relative_humidity_2m}%`;
  document.getElementById("wind").textContent = `${current.wind_speed_10m} km/h`;
  document.getElementById("sunrise").textContent = daily.sunrise[0].split("T")[1];
  document.getElementById("sunset").textContent = daily.sunset[0].split("T")[1];
  document.getElementById("dateTime").textContent = new Date().toLocaleString();

  const code = current.weather_code;
  const desc = getWeatherDescription(code);
  document.getElementById("desc").textContent = desc;
  document.getElementById("icon").src = getWeatherIcon(code);

  const currentWeatherDiv = document.querySelector(".current-weather");
  const theme = getWeatherTheme(code);
  currentWeatherDiv.className = `current-weather ${theme}`;

  const forecastDiv = document.getElementById("forecast");
  forecastDiv.innerHTML = "";

  for (let i = 0; i < 5; i++) {
    const day = document.createElement("div");
    const code = daily.weather_code[i];
    const desc = getWeatherDescription(code);
    const theme = getWeatherTheme(code);
    const icon = getWeatherIcon(code);

    day.className = `forecast-card ${theme}`;
    day.innerHTML = `
      <h4>${daily.time[i]}</h4>
      <img src="${icon}" alt="icon" />
      <p>${desc}</p>
      <p>${daily.temperature_2m_max[i]}° / ${daily.temperature_2m_min[i]}°</p>
    `;
    forecastDiv.appendChild(day);
  }
}

function getWeatherDescription(code) {
  const map = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Rime Fog",
    51: "Light Drizzle",
    61: "Rainy",
    71: "Snowy",
    80: "Showers",
    95: "Thunderstorm",
  };
  return map[code] || "Unknown";
}

function getWeatherIcon(code) {
  if (code === 0) return "https://cdn-icons-png.flaticon.com/512/869/869869.png";
  if (code <= 3) return "https://cdn-icons-png.flaticon.com/512/1163/1163624.png";
  if (code <= 61) return "https://cdn-icons-png.flaticon.com/512/414/414974.png";
  if (code <= 71) return "https://cdn-icons-png.flaticon.com/512/642/642102.png";
  if (code >= 95) return "https://cdn-icons-png.flaticon.com/512/1146/1146869.png";
  return "https://cdn-icons-png.flaticon.com/512/1163/1163624.png";
}

function getWeatherTheme(code) {
  if (code === 0 || code === 1) return "sunny";
  if (code === 2 || code === 3) return "cloudy";
  if (code >= 51 && code <= 80) return "rainy";
  if (code >= 95) return "stormy";
  if (code >= 71 && code < 80) return "snowy";
  if (code === 45 || code === 48) return "foggy";
  return "cloudy";
}
