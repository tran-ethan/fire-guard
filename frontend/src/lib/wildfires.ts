
export async function getWildFires(start: string, end: string) {
    const data = {
        args: [start, end]
    };
    
    try {
        const response = await fetch('http://18.217.35.228:5000/get-fires', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        return result;

    } catch (error) {
        console.error('Failed to fetch data:', error);
        throw error;
    }
}

