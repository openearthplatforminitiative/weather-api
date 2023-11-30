from httpx import Client

with Client() as client:
    response = client.get(
        url="$endpoint_url",
        params={"lat": 52.520008, "lon": 13.404954, "date": "2024-12-24"},
    )

    json = response.json()

    print(f"Sunrise: {json['properties']['sunrise']['time']}")
    print(f"Sunset: {json['properties']['sunset']['time']}")
