# 📁 Project Structure

```
loan-approval-prediction/
│
├── 📄 app.py                    # Main Flask application
├── 📄 requirements.txt          # Python dependencies
├── 📄 README.md                 # Project documentation
├── 📄 .gitignore               # Git ignore rules
├── 📄 PROJECT_STRUCTURE.md     # This file
├── 📄 run.bat                  # Windows batch file to run the app
│
├── 📊 loan_data.csv            # Training dataset (614 records)
├── 🤖 loan_model.pkl           # Trained ML model (Random Forest)
│
├── 📄 index.html               # Main dashboard interface
│
├── 📁 static/                  # Static files
│   └── 📄 manifest.json        # PWA manifest (optional)
│
└── 📁 flask_session/           # Flask session data (auto-generated)
```

## 📋 File Descriptions

### Core Application Files
- **`app.py`**: Main Flask application with ML model, API endpoints, and smart data imputation
- **`requirements.txt`**: All Python package dependencies
- **`run.bat`**: Quick start script for Windows users

### Data & Model Files
- **`loan_data.csv`**: Training dataset with 614 loan applications
- **`loan_model.pkl`**: Trained Random Forest model (76% accuracy)

### Frontend Files
- **`index.html`**: Complete dashboard with:
  - Dark/Light mode toggle
  - Interactive charts (Chart.js)
  - Real-time notifications
  - Mobile-responsive design
  - Loan prediction form

### Configuration Files
- **`.gitignore`**: Excludes unnecessary files from Git
- **`static/manifest.json`**: PWA configuration (optional)

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd loan-approval-prediction
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```
   Or on Windows: `run.bat`

4. **Open browser**
   Navigate to `http://127.0.0.1:5000`

## 🔧 Technical Stack

- **Backend**: Flask, scikit-learn, pandas, numpy
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Charts**: Chart.js with animations
- **ML Model**: Random Forest Classifier
- **Data Processing**: Smart imputation for missing values
