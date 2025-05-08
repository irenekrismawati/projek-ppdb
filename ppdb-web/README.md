# PPDB Web Application

This is a simple web application for managing student registrations (PPDB - Penerimaan Peserta Didik Baru) using Python and Flask.

## Project Structure

```
ppdb-web
├── app
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   └── templates
│       ├── base.html
│       ├── index.html
│       └── register.html
├── static
│   ├── css
│   │   └── styles.css
│   └── js
│       └── scripts.js
├── app.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ppdb-web.git
   cd ppdb-web
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python app.py
   ```

2. Open your web browser and go to `http://127.0.0.1:5000`.

## Features

- Student registration form
- Basic validation for user input
- Responsive design with CSS
- JavaScript for client-side functionality

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.