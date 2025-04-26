function getWeatherData() {
    const city = document.getElementById("city-input").value;
    const apiUrl = `https://lory1992.github.io/Meteo/${city}`;

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Dati ricevuti:", data); // Aggiunto per debug
            if (data.error) {
                alert(data.error);
                document.getElementById("current-weather").style.display = "none";
                document.getElementById("forecast").style.display = "none";
            } else {
                displayCurrentWeather(data.current);
                displayForecast(data.forecast);
            }
        })
        .catch(error => {
            console.error('Errore durante la chiamata all\'API:', error);
            alert('Si è verificato un errore nel recupero dei dati meteo.');
            document.getElementById("current-weather").style.display = "none";
            document.getElementById("forecast").style.display = "none";
        });
}

function displayCurrentWeather(data) {
    document.getElementById("current-city").textContent = data.city;
    document.getElementById("current-temp").textContent = data.temp;
    document.getElementById("current-description").textContent = data.description;
    document.getElementById("current-humidity").textContent = data.humidity;
    document.getElementById("current-wind").textContent = data.wind;
    document.getElementById("current-weather").style.display = "block";
}

function displayForecast(forecasts) {
    const forecastContainer = document.getElementById("forecast-container");
    forecastContainer.innerHTML = "";
    forecasts.forEach(day => {
        const dayDiv = document.createElement("div");
        dayDiv.classList.add("forecast-day");
        dayDiv.innerHTML = `
            <h3>${day.date}</h3>
            <p>${day.icon}</p>
            <p>Min: ${day.min_temp}°C</p>
            <p>Max: ${day.max_temp}°C</p>
            <p class="condition">${day.conditions}</p>
        `;
        forecastContainer.appendChild(dayDiv);
    });
    document.getElementById("forecast").style.display = "block";
}
