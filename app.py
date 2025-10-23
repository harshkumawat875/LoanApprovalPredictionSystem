from flask import Flask, render_template, request, jsonify, session, send_from_directory
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import json
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# Enable CORS for all routes with explicit configuration
CORS(app, resources={
    r"/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Global variables for model and encoders
model = None
label_encoders = {}
feature_columns = []
df_original = None
applications_db = []  # Store loan applications

def load_and_preprocess_data():
    """Load and preprocess the loan data"""
    global model, label_encoders, feature_columns, df_original
    
    # Load data
    df_original = pd.read_csv('loan_data.csv')
    df = df_original.copy()
    
    # Handle missing values
    df['Gender'].fillna(df['Gender'].mode()[0], inplace=True)
    df['Married'].fillna(df['Married'].mode()[0], inplace=True)
    df['Dependents'].fillna(df['Dependents'].mode()[0], inplace=True)
    df['Self_Employed'].fillna(df['Self_Employed'].mode()[0], inplace=True)
    df['LoanAmount'].fillna(df['LoanAmount'].median(), inplace=True)
    df['Loan_Amount_Term'].fillna(df['Loan_Amount_Term'].mode()[0], inplace=True)
    
    # Smart imputation for Credit History based on multiple factors
    def smart_credit_imputation(row):
        if pd.isna(row['Credit_History']):
            # Rule-based imputation using income, education, and other factors
            score = 0
            
            # Income factor (higher income = better credit likelihood)
            if row['ApplicantIncome'] >= 5000:
                score += 2
            elif row['ApplicantIncome'] >= 3000:
                score += 1
            
            # Education factor (graduates tend to have better credit)
            if row['Education'] == 'Graduate':
                score += 1
            
            # Married people tend to have more stable credit
            if row['Married'] == 'Yes':
                score += 1
            
            # Urban areas tend to have better credit infrastructure
            if row['Property_Area'] == 'Urban':
                score += 1
            
            # Self-employed might have irregular income
            if row['Self_Employed'] == 'No':
                score += 1
            
            # Decision: score >= 3 means good credit (1), else poor credit (0)
            return 1.0 if score >= 3 else 0.0
        else:
            return row['Credit_History']
    
    df['Credit_History'] = df.apply(smart_credit_imputation, axis=1)
    
    # Convert categorical variables to numerical
    categorical_columns = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area']
    
    for col in categorical_columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
    
    # Define feature columns
    feature_columns = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 
                      'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 
                      'Credit_History', 'Property_Area']
    
    # Prepare features and target
    X = df[feature_columns]
    y = df['Loan_Status']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")
    
    # Save model
    joblib.dump(model, 'loan_model.pkl')
    
    return model, label_encoders

def predict_loan_approval(data):
    """Predict loan approval based on input data"""
    global model, label_encoders, feature_columns
    
    if model is None:
        return None
    
    # Convert input data to DataFrame
    df_input = pd.DataFrame([data])
    
    # Encode categorical variables
    for col in ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area']:
        if col in df_input.columns:
            df_input[col] = label_encoders[col].transform(df_input[col])
    
    # Ensure all feature columns are present
    for col in feature_columns:
        if col not in df_input.columns:
            df_input[col] = 0
    
    # Reorder columns to match training data
    df_input = df_input[feature_columns]
    
    # Make prediction
    prediction = model.predict(df_input)[0]
    probability = model.predict_proba(df_input)[0]
    
    return {
        'prediction': prediction,
        'probability': {
            'approved': float(probability[1]) if len(probability) > 1 else 0.0,
            'rejected': float(probability[0]) if len(probability) > 0 else 0.0
        }
    }


@app.route('/')
def home():
    """Serve the professional dashboard page"""
    return send_from_directory('.', 'index.html')


@app.route('/dashboard-data', methods=['GET', 'OPTIONS'])
def dashboard_data():
    """Get dashboard analytics data"""
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    global df_original
    
    if df_original is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    # Calculate statistics
    total_applications = len(df_original)
    approved_count = len(df_original[df_original['Loan_Status'] == 'Y'])
    rejected_count = len(df_original[df_original['Loan_Status'] == 'N'])
    approval_rate = (approved_count / total_applications) * 100
    
    # Income distribution
    income_ranges = ['0-5K', '5K-10K', '10K-15K', '15K-20K', '20K+']
    income_approval_rates = []
    
    for i, range_label in enumerate(income_ranges):
        if i == 0:
            mask = df_original['ApplicantIncome'] <= 5000
        elif i == len(income_ranges) - 1:
            mask = df_original['ApplicantIncome'] > 20000
        else:
            lower = 5000 * i
            upper = 5000 * (i + 1)
            mask = (df_original['ApplicantIncome'] > lower) & (df_original['ApplicantIncome'] <= upper)
        
        range_data = df_original[mask]
        if len(range_data) > 0:
            approval_rate_range = (len(range_data[range_data['Loan_Status'] == 'Y']) / len(range_data)) * 100
        else:
            approval_rate_range = 0
        income_approval_rates.append(approval_rate_range)
    
    # Property area distribution
    property_counts = df_original['Property_Area'].value_counts().to_dict()
    
    # Credit history impact
    credit_good = df_original[df_original['Credit_History'] == 1]
    credit_poor = df_original[df_original['Credit_History'] == 0]
    
    credit_good_rate = (len(credit_good[credit_good['Loan_Status'] == 'Y']) / len(credit_good)) * 100 if len(credit_good) > 0 else 0
    credit_poor_rate = (len(credit_poor[credit_poor['Loan_Status'] == 'Y']) / len(credit_poor)) * 100 if len(credit_poor) > 0 else 0
    
    # Education impact
    graduate = df_original[df_original['Education'] == 'Graduate']
    not_graduate = df_original[df_original['Education'] == 'Not Graduate']
    
    graduate_rate = (len(graduate[graduate['Loan_Status'] == 'Y']) / len(graduate)) * 100 if len(graduate) > 0 else 0
    not_graduate_rate = (len(not_graduate[not_graduate['Loan_Status'] == 'Y']) / len(not_graduate)) * 100 if len(not_graduate) > 0 else 0
    
    # Marital status impact
    married = df_original[df_original['Married'] == 'Yes']
    single = df_original[df_original['Married'] == 'No']
    
    married_rate = (len(married[married['Loan_Status'] == 'Y']) / len(married)) * 100 if len(married) > 0 else 0
    single_rate = (len(single[single['Loan_Status'] == 'Y']) / len(single)) * 100 if len(single) > 0 else 0
    
    return jsonify({
        'statistics': {
            'total_applications': total_applications,
            'approved_count': approved_count,
            'rejected_count': rejected_count,
            'approval_rate': round(approval_rate, 1)
        },
        'income_analysis': {
            'ranges': income_ranges,
            'approval_rates': [round(rate, 1) for rate in income_approval_rates]
        },
        'property_distribution': property_counts,
        'credit_impact': {
            'good_credit_rate': round(credit_good_rate, 1),
            'poor_credit_rate': round(credit_poor_rate, 1)
        },
        'education_impact': {
            'graduate_rate': round(graduate_rate, 1),
            'not_graduate_rate': round(not_graduate_rate, 1)
        },
        'marital_impact': {
            'married_rate': round(married_rate, 1),
            'single_rate': round(single_rate, 1)
        }
    })

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    """API endpoint for loan prediction"""
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
                          'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 
                          'Loan_Amount_Term', 'Credit_History', 'Property_Area']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # Make prediction
        result = predict_loan_approval(data)
        
        if result is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        # Store application in database
        application_record = {
            'id': len(applications_db) + 1,
            'timestamp': datetime.now().isoformat(),
            'user_id': session.get('user_id', 'anonymous'),
            'application_data': data,
            'prediction': result['prediction'],
            'probability': result['probability']
        }
        applications_db.append(application_record)
        
        return jsonify({
            'prediction': result['prediction'],
            'probability': result['probability'],
            'message': 'Loan Approved' if result['prediction'] == 'Y' else 'Loan Rejected',
            'application_id': application_record['id']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/business-intelligence')
def business_intelligence():
    """Get business intelligence data"""
    global df_original
    
    if df_original is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    # Calculate advanced metrics
    total_applications = len(df_original)
    approved_count = len(df_original[df_original['Loan_Status'] == 'Y'])
    approval_rate = (approved_count / total_applications) * 100
    
    # Risk Score Calculation
    risk_factors = {
        'credit_history': len(df_original[df_original['Credit_History'] == 0]) / total_applications,
        'low_income': len(df_original[df_original['ApplicantIncome'] < 5000]) / total_applications,
        'high_dependents': len(df_original[df_original['Dependents'].isin(['2', '3+'])]) / total_applications,
        'rural_area': len(df_original[df_original['Property_Area'] == 'Rural']) / total_applications
    }
    
    risk_score = 100 - (sum(risk_factors.values()) * 25)  # Convert to 0-100 scale
    
    # Growth Rate (simulated)
    growth_rate = 12.5  # Monthly growth percentage
    
    # Revenue Impact (simulated based on loan amounts)
    avg_loan_amount = df_original['LoanAmount'].mean()
    monthly_revenue = (approved_count * avg_loan_amount * 0.05) / 12  # 5% interest annually
    
    # Key Insights
    insights = {
        'credit_history_impact': {
            'good_credit_rate': len(df_original[(df_original['Credit_History'] == 1) & (df_original['Loan_Status'] == 'Y')]) / len(df_original[df_original['Credit_History'] == 1]) * 100,
            'poor_credit_rate': len(df_original[(df_original['Credit_History'] == 0) & (df_original['Loan_Status'] == 'Y')]) / len(df_original[df_original['Credit_History'] == 0]) * 100
        },
        'urban_vs_rural': {
            'urban_rate': len(df_original[(df_original['Property_Area'] == 'Urban') & (df_original['Loan_Status'] == 'Y')]) / len(df_original[df_original['Property_Area'] == 'Urban']) * 100,
            'rural_rate': len(df_original[(df_original['Property_Area'] == 'Rural') & (df_original['Loan_Status'] == 'Y')]) / len(df_original[df_original['Property_Area'] == 'Rural']) * 100
        },
        'education_impact': {
            'graduate_rate': len(df_original[(df_original['Education'] == 'Graduate') & (df_original['Loan_Status'] == 'Y')]) / len(df_original[df_original['Education'] == 'Graduate']) * 100,
            'not_graduate_rate': len(df_original[(df_original['Education'] == 'Not Graduate') & (df_original['Loan_Status'] == 'Y')]) / len(df_original[df_original['Education'] == 'Not Graduate']) * 100
        }
    }
    
    return jsonify({
        'risk_score': round(risk_score, 1),
        'growth_rate': growth_rate,
        'monthly_revenue': round(monthly_revenue / 100000, 1),  # Convert to lakhs
        'insights': insights,
        'risk_factors': risk_factors,
        'total_applications': total_applications,
        'approval_rate': round(approval_rate, 1)
    })

@app.route('/integration-status')
def integration_status():
    """Get integration status"""
    integrations = {
        'bank_api': {
            'name': 'Bank API Integration',
            'status': 'online',
            'description': 'Real-time bank data synchronization',
            'last_sync': datetime.now().isoformat()
        },
        'credit_bureau': {
            'name': 'Credit Bureau',
            'status': 'online',
            'description': 'Credit score verification system',
            'last_sync': datetime.now().isoformat()
        },
        'email_service': {
            'name': 'Email Service',
            'status': 'online',
            'description': 'Automated notification system',
            'last_sync': datetime.now().isoformat()
        },
        'sms_gateway': {
            'name': 'SMS Gateway',
            'status': 'offline',
            'description': 'Instant SMS notifications',
            'last_sync': None
        },
        'document_service': {
            'name': 'Document Service',
            'status': 'online',
            'description': 'PDF generation and storage',
            'last_sync': datetime.now().isoformat()
        },
        'cloud_storage': {
            'name': 'Cloud Storage',
            'status': 'online',
            'description': 'Secure data backup and sync',
            'last_sync': datetime.now().isoformat()
        }
    }
    
    return jsonify(integrations)

@app.route('/export-data')
def export_data():
    """Export data in various formats"""
    global df_original
    
    if df_original is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    format_type = request.args.get('format', 'json')
    
    if format_type == 'csv':
        csv_data = df_original.to_csv(index=False)
        return csv_data, 200, {'Content-Type': 'text/csv', 'Content-Disposition': 'attachment; filename=loan_data.csv'}
    
    elif format_type == 'excel':
        # For Excel export, we'd need openpyxl library
        return jsonify({'message': 'Excel export requires additional setup'})
    
    else:  # JSON
        return jsonify({
            'data': df_original.to_dict('records'),
            'metadata': {
                'total_records': len(df_original),
                'columns': list(df_original.columns),
                'exported_at': datetime.now().isoformat()
            }
        })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

if __name__ == '__main__':
    # Load model on startup
    print("Loading and training model...")
    load_and_preprocess_data()
    print("Model loaded successfully!")
    
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
