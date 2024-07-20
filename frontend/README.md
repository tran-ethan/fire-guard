# Fire Guard Front-end
This is the front-end part of the Fire Guard project associated with the Dawson AI Accelerator program. 
The front-end is built with vite + svelte + typescript.

## Getting Started
After cloning the repository, you can run the following commands to start the front-end:

1. Install dependencies
```bash
npm install
```

2. Start the development server
```bash
npm run dev
```

3. Open the localhost domain given in the terminal to view the front-end.


## Setting up the environment
To set up the environment, you need to create a `.env` file in the root directory of the project. The `.env` file should contain the following variables:

```t
VITE_FIREBASE_API_KEY="YOUR_API_KEY"
VITE_FIREBASE_AUTH_DOMAIN="YOUR_AUTH_DOMAIN"
VITE_FIREBASE_PROJECT_ID="YOUR_PROJECT_ID"
VITE_FIREBASE_STORAGE_BUCKET="YOUR_STORAGE_BUCKET"
VITE_FIREBASE_MESSAGE_SENDER_ID="YOUR_MESSAGE_SENDER_ID"
VITE_FIREBASE_APP_ID="YOUR_APP_ID"
VITE_FIREBASE_MEASUREMENT_ID="YOUR_MEASUREMENT_ID"
```
Make sure that you replace the placeholders with your own Firebase project credentials. Moreover, make sure that there is no space between the variable name and the value.
