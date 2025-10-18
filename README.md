# 🚀 Advanced Loan Approval Prediction System

A comprehensive, professional-grade web application that predicts loan approval using advanced machine learning algorithms with real-time analytics, user authentication, and interactive data visualization.

## ✨ Features

### 🎯 Core Features
- **Advanced ML Model**: Random Forest Classifier with 100 estimators
- **Real-time Prediction**: Instant loan approval predictions with probability scores
- **Interactive Dashboard**: Beautiful analytics dashboard with live charts
- **User Authentication**: Secure login/registration system
- **Data Visualization**: Interactive charts and business insights
- **Application Tracking**: Complete loan application history

### 📊 Dashboard Features
- **Live Statistics**: Real-time approval rates and application counts
- **Interactive Charts**: Income vs approval, property distribution, credit impact
- **Business Insights**: Key insights and patterns from data analysis
- **Multi-tab Interface**: Dashboard, Prediction, Analytics, and Insights tabs

### 🔐 Security Features
- **User Authentication**: Secure login with password hashing
- **Session Management**: Flask-Session for secure user sessions
- **Data Protection**: Secure data handling and storage

### 📈 Analytics Features
- **Income Analysis**: Approval rates by income brackets
- **Demographic Insights**: Education, marital status, property area impact
- **Credit History Impact**: Detailed credit score analysis
- **Trend Analysis**: Historical approval patterns

## Project Structure

```
loan-approval-prediction/
├── app.py                 # Advanced Flask backend with ML & Auth
├── laon_data.csv         # Training dataset
├── requirements.txt      # Python dependencies
├── index.html            # Main dashboard interface
├── run.bat               # Windows startup script
├── run.sh                # Linux/Mac startup script
└── README.md             # This file
```

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone or Download

Download the project files to your local machine.

### Step 2: Install Dependencies

```bash
cd loan-approval-prediction
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Usage

### 🌐 Web Interface (Recommended)

1. **Start the Application**
   ```bash
   python app.py
   ```

2. **Access the Dashboard**
   - Open your browser and navigate to `http://localhost:5000`
   - You'll see the advanced dashboard with multiple tabs

3. **User Registration/Login**
   - Click "Register" to create a new account
   - Or click "Login" if you already have an account
   - Authentication is required for full dashboard access

4. **Dashboard Features**
   - **Dashboard Tab**: View live statistics and interactive charts
   - **Predict Tab**: Submit loan applications for prediction
   - **Analytics Tab**: Detailed analytics and insights
   - **Insights Tab**: Key business insights and patterns

5. **Making Predictions**
   - Switch to the "Predict Loan" tab
   - Fill in all required loan application details
   - Click "Predict Loan Approval" for instant results
   - View probability scores and detailed analysis

### 📱 Dashboard Features

#### Dashboard Tab
- **Live Statistics**: Real-time approval rates and counts
- **Interactive Charts**: 
  - Loan approval trends over time
  - Income vs approval rate analysis
  - Property area distribution
  - Credit history impact

#### Analytics Tab
- **Detailed Analytics**: Comprehensive data analysis
- **Education Impact**: Graduate vs non-graduate approval rates
- **Marital Status Impact**: Married vs single applicant analysis

#### Insights Tab
- **Key Insights**: Automated business insights
- **Pattern Recognition**: Data-driven recommendations
- **Risk Analysis**: Credit and demographic risk factors

### API Usage

You can also use the API directly:

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Gender": "Male",
    "Married": "Yes",
    "Dependents": "2",
    "Education": "Graduate",
    "Self_Employed": "No",
    "ApplicantIncome": 5000,
    "CoapplicantIncome": 2000,
    "LoanAmount": 150000,
    "Loan_Amount_Term": 360,
    "Credit_History": 1,
    "Property_Area": "Urban"
  }'
```

## API Endpoints

### 🔐 Authentication Endpoints

#### POST /login
Authenticate user login.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful"
}
```

#### POST /register
Register new user.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Registration successful"
}
```

#### GET /logout
Logout current user.

**Response:** Redirects to home page

### 📊 Dashboard Endpoints

#### GET /dashboard-data
Get analytics data for dashboard (requires authentication).

**Response:**
```json
{
  "statistics": {
    "total_applications": 500,
    "approved_count": 342,
    "rejected_count": 158,
    "approval_rate": 68.4
  },
  "income_analysis": {
    "ranges": ["0-5K", "5K-10K", "10K-15K", "15K-20K", "20K+"],
    "approval_rates": [45.2, 65.8, 78.3, 85.1, 92.4]
  },
  "property_distribution": {
    "Urban": 180,
    "Rural": 150,
    "Semiurban": 170
  },
  "credit_impact": {
    "good_credit_rate": 85.2,
    "poor_credit_rate": 25.8
  },
  "education_impact": {
    "graduate_rate": 78.5,
    "not_graduate_rate": 45.2
  },
  "marital_impact": {
    "married_rate": 72.3,
    "single_rate": 68.1
  }
}
```

### 🔮 Prediction Endpoints

#### POST /predict
Predicts loan approval based on application data.

**Request Body:**
```json
{
  "Gender": "Male",
  "Married": "Yes",
  "Dependents": "2",
  "Education": "Graduate",
  "Self_Employed": "No",
  "ApplicantIncome": 5000,
  "CoapplicantIncome": 2000,
  "LoanAmount": 150000,
  "Loan_Amount_Term": 360,
  "Credit_History": 1,
  "Property_Area": "Urban"
}
```

**Response:**
```json
{
  "prediction": "Y",
  "probability": {
    "approved": 0.85,
    "rejected": 0.15
  },
  "message": "Loan Approved"
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

## Model Details

- **Algorithm**: Random Forest Classifier
- **Features**: 11 input features including demographic, financial, and property information
- **Preprocessing**: Automatic handling of missing values and categorical encoding
- **Performance**: Model accuracy is displayed in the console on startup

## Data Features

The model uses the following features for prediction:

1. **Gender**: Applicant's gender
2. **Married**: Marital status
3. **Dependents**: Number of dependents
4. **Education**: Education level
5. **Self_Employed**: Self-employment status
6. **ApplicantIncome**: Monthly income
7. **CoapplicantIncome**: Co-applicant's income
8. **LoanAmount**: Requested loan amount
9. **Loan_Amount_Term**: Loan term in days
10. **Credit_History**: Credit history score
11. **Property_Area**: Property location type

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `app.py` (line 95)
2. **Missing dependencies**: Run `pip install -r requirements.txt`
3. **Data file not found**: Ensure `laon_data.csv` is in the same directory as `app.py`

### Error Messages

- **"Model not loaded"**: The machine learning model failed to load
- **"Missing field"**: Required form fields are not filled
- **"Prediction failed"**: Server error during prediction

## Development

### Adding New Features

1. **New ML Algorithm**: Modify the `load_and_preprocess_data()` function
2. **Additional Features**: Update the feature list and preprocessing logic
3. **UI Improvements**: Edit the HTML file `index.html`

### Model Retraining

To retrain the model with new data:

1. Replace `laon_data.csv` with updated data
2. Restart the application
3. The model will automatically retrain on startup

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please check the troubleshooting section or create an issue in the project repository.
