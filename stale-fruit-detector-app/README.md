# Stale Fruit Detector 🍎

An AI-powered application that detects fruit freshness and provides storage recommendations using advanced machine learning models.

## Features

- 🤖 AI-Powered Detection
- ⚡ Instant Results
- 📊 Detailed Analysis
- 🌐 Multi-language Support
- 📱 Responsive Design

## Tech Stack

- Python 3.8+
- Streamlit
- PyTorch
- MongoDB
- Vision Transformer & Swin Transformer Models

## Local Development Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd stale-fruit-detector-app
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with:
```
MONGODB_URI=your_mongodb_uri
SECRET_KEY=your_secret_key
```

5. Run the application:
```bash
streamlit run main.py
```

## Deployment

### Deploy on Streamlit Cloud

1. Push your code to GitHub
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository and branch
6. Set the main file path as `main.py`
7. Click "Deploy"

### Environment Variables

Set the following in Streamlit Cloud:
- `MONGODB_URI`: Your MongoDB connection string
- `SECRET_KEY`: Your application secret key

## Project Structure

```
stale-fruit-detector-app/
├── main.py              # Main application file
├── pages/              # Streamlit pages
├── models/             # ML model files
├── utils/              # Utility functions
├── background_images/  # UI assets
├── requirements.txt    # Dependencies
└── README.md          # Documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 