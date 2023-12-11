const response = await fetch(
  "$endpoint_url?lat=52.520008&lon=13.404954&date=2024-12-24"
);
const json = await response.json();

// Get sunrise and sunset times
const sunriseTime = json.properties.sunrise.time;
const sunsetTime = json.properties.sunset.time;

console.log(`Sunrise: ${sunriseTime}`);
console.log(`Sunset: ${sunsetTime}`);
