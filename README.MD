# File Converter WebUI

A web-based file conversion application that allows users to upload files and convert them into various formats. This application leverages Flask for the backend and `ffmpeg` for handling the file conversion processes, supporting a range of video and image formats.

## Features

- **Convert Video and Image Files:** Supports a variety of popular video and image formats.
- **Asynchronous Task Handling:** Efficiently handles file conversion jobs in the background.
- **User-Friendly Interface:** Simple web-based interface for a seamless user experience.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Supported Formats](#supported-formats)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Ensure you have the following installed on your system:

- **Python 3.12 or later**
- **Flask** (Python package)
- **ffmpeg** (command-line tool for media file conversion)

## Installation

1. **Clone this repository:**

   ```bash
   git clone https://github.com/your-username/file-converter.git
   cd file-converter
   ```

2. **Install required Python packages:**

   ```bash   
    pip install flask
    ```

3.    **Run the application:**

   ```
    python app.py
   ```

4. **Access the Web UI:**

    Open a browser and navigate to http://localhost:5006 (or replace localhost with your server IP if hosting remotely).

## Configuration

To change the application's default port, modify the last line in app.py:
```app.run(host='0.0.0.0', port=5006)```

Replace  ```5006``` with the port number you prefer.


## Usage

1. **Upload a File:** Choose either an image or video file to upload through the web interface.

2. **Select Conversion Format:** Once uploaded, select the desired format to convert the file into.
3. **Convert and Download:** Click "Convert and Download," and the file in the new format will be ready for download shortly.


## Supported Formats
The application supports conversions between the following formats:

- **Image Formats:** ```jpg```, ```jpeg```, ```png```, ```gif```, ```webp```
- **Video Formats:** ```mp4```, ```avi```, ```mov```, ```mkv```, ```webm```

## File Structure

- **app.py:** Main application file, which runs the Flask server and handles routes.
- **uploads/:** Directory where uploaded files are temporarily stored.
- **converted/:** Directory where converted files are saved.

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request for any improvements, bug fixes, or new features.
