Sure! Here’s the complete `README.md` without any breaks:


# Weather Info HTTP Server

## Description

This project is a Python-based HTTP server that utilizes the Open Weather Map API to provide weather information for a specified city. Users can request weather data via a command-line interface (CLI) or through a simple HTML page.

## Features

- Responds to HTTP requests for weather information
- Fetches weather data from the Open Weather Map API
- Provides a command-line interface for user input
- Serves an HTML page to display weather information

## Requirements

To run this project, you need Python installed on your machine. You also need to install the required packages listed in `requirements.txt`.

### Dependencies

- `pytz`: For timezone handling

## Installation

1. **Clone the repository** (or download the ZIP file):

   ```bash
   git clone <your-repo-url>
   cd <your-project-directory>
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the HTTP server, execute the main Python script:

```bash
python weather_server.py
```

### CLI Usage

Once the server is running, execute the following Python script to be able to request weather information by entering the city name in the command line.

```bash
python weather_client.py
```

### HTML Page

You can also access the weather information through the provided HTML page by navigating to `http://localhost:8080/weather_client`.

## Configuration

Make sure to set up your **Open Weather Map API key** in the script where necessary. You may need to sign up for an API key if you haven't done so already.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Open Weather Map API for providing weather data
- Python Standard Library for HTTP handling
- `pytz` for timezone management
```

Feel free to modify any sections as needed! Let me know if you need further assistance.