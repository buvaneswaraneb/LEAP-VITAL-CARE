Create a professional README.md for a project named "LEAP-VITAL-CARE".

Project description:
LEAP-VITAL-CARE is an IoT-based health monitoring system that measures real-time body temperature and heart rate using an ESP32. The ESP32 sends data to a Flask-based backend API running on a local network. The API is exposed securely to the internet using ngrok. A frontend web dashboard hosted on Netlify consumes the API and displays live health data to users from anywhere.

Key requirements for the README:
- Use a formal and professional tone
- Do NOT use emojis
- Suitable for academic submission or public GitHub repository
- Clear explanation of system architecture
- Emphasize security (ESP32 not exposed to the internet)
- Explain separation of frontend and backend

Include the following sections:
1. Project Title
2. Overview
3. Key Features
4. System Architecture (use ASCII diagram)
5. Technology Stack (Hardware, Backend, Frontend)
6. Project Structure (folder tree)
7. Setup Instructions
   - ESP32 setup
   - Flask backend setup
   - ngrok usage
   - Frontend deployment on Netlify
8. Security Considerations
9. Intended Use Cases
10. Future Enhancements
11. License

Technical details to include:
- ESP32 reads pulse sensor and DS18B20 temperature sensor
- Flask uses flask-cors and requests
- Frontend uses HTML, CSS, and JavaScript
- API endpoint: /api/data
- ngrok provides HTTPS public access
- Netlify hosts only the frontend

Output should be formatted as valid Markdown and saved as README.md.
