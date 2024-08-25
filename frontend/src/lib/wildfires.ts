
export type WildFire = {
    lat: number;
    lon: number;
    hectares: number;
    date: string;
    elevation: number;
    temp_c: number;
    max_temp_c: number;
    min_temp_c: number;
    wind_kph: number;
    wind_dir: number;
    precip_mm: number;
    humidity: number;
    pressure_hPa: number;
    soil_temp_c: number;
    soil_moisture: number;
    totalsnow_cm: number;
}


export async function getWildFires() {
    try {
        // Perform the GET request to the server
        const response = await fetch('http://18.217.35.228:5000/get-fires');

        // Check if the response is successful
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Parse the JSON response
        const data = await response.json();

        return data
    } catch (error) {
        console.error('Failed to fetch data:', error);
    }
}
