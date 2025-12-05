# Cardio Smart Dashboard - Final Project

## Project Overview

The **Cardio Smart Dashboard** is an interactive web-based application designed to visualize and manage patient cardiovascular health data. It integrates with FHIR (Fast Healthcare Interoperability Resources) servers to retrieve real-time patient information and provides a comprehensive view of cardiac health metrics.

## Key Features

### 📊 Patient Data Visualization
- **Patient Demographics**: Name, gender, date of birth
- **Blood Pressure Monitoring**: Real-time BP status with color-coded health indicators (Normal/Elevated/High)
- **BMI Tracking**: Body Mass Index calculation with health status classification
- **Vital Signs Trends**: Dual-axis line chart showing blood pressure trends over time alongside BMI changes
- **High BP Reference Line**: Visual indicator (dashed red line at 140 mmHg) for hypertension threshold

### 💊 Medication Management
- **Active Medications Display**: Complete list of current prescriptions
- **Medication Lookup**: Automatic fetching of detailed medication information from FHIR Medication resources
- **Medication Control**: Ability to mark medications as stopped
- **Prescription Interface**: Add new medications to the patient's treatment plan

### 📈 Visual Analytics
- **Interactive Charts**: Chart.js-powered visualizations with dual-axis support
- **Responsive Design**: Mobile-friendly dashboard with clean, modern UI
- **Color-Coded Status Indicators**: Quick visual assessment of patient health status

## Technical Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Charting Library**: Chart.js
- **FHIR Integration**: FHIR Client (fhirclient.js)
- **Data Source**: FHIR R3 Server (https://r3.smarthealthit.org)
- **Patient Discovery**: Python 3 with requests library

## File Structure

```
final project/
├── index.html              # Main dashboard application
├── find_patients.py        # Python utility to find patients with complete data
└── README.md              # Project documentation
```

## Installation & Setup

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Python 3.6+ (for patient discovery script)
- Internet connection to access FHIR server

### Running the Dashboard

1. **Open the dashboard in your browser**:
   ```bash
   # Simply open index.html in any modern web browser
   open index.html
   ```

2. **Select a patient from the dropdown** to load their data

3. **View the visualizations and manage medications**

### Finding Patients with Complete Data

The project includes a Python utility to help identify patients with complete cardiovascular data:

```bash
python3 find_patients.py
```

This script will:
- Search through available patients
- Check for complete data sets (BP, weight, height, demographics, medications)
- Return 10 patients with complete data
- Output ready-to-use patient IDs for the dashboard

**Note**: The search limit is set to 30 patients by default. Modify the script to increase this if needed.

## Data Requirements

For optimal dashboard functionality, patients should have:
- ✅ Demographics (Name, Gender, Date of Birth)
- ✅ Blood Pressure observations (code: 55284-4)
- ✅ Weight measurements (code: 29463-7)
- ✅ Height measurements (code: 8302-2)
- ✅ Active medications (optional but recommended)

## API Endpoints Used

The dashboard queries the following FHIR endpoints:
- `Patient/{id}` - Patient demographics
- `Observation?patient={id}&code=55284-4` - Blood pressure data
- `Observation?patient={id}&code=29463-7` - Weight data
- `Observation?patient={id}&code=8302-2` - Height data
- `MedicationRequest?patient={id}&status=active` - Active medications
- `Medication/{id}` - Medication details

## Dashboard Metrics Explained

### Blood Pressure Status
- **Normal** (Green): Systolic < 130 mmHg
- **Elevated** (Orange): Systolic 130-139 mmHg
- **High - Stage 2** (Red): Systolic ≥ 140 mmHg

### BMI Status
- **Underweight** (Green): BMI < 18.5
- **Normal** (Green): BMI 18.5-24.9
- **Overweight** (Orange): BMI ≥ 25

### Chart Features
- **Blood Pressure Trend**: Shows mean blood pressure (average of systolic and diastolic) over time
- **BMI Trend**: Calculated from weight and height measurements on the same dates
- **High BP Threshold Line**: Red dashed reference line at 140 mmHg for easy identification of hypertension
- **Dual-Axis Display**: BP on left axis (mmHg), BMI on right axis (kg/m²)

## Debugging

The application includes comprehensive console logging for troubleshooting:
- Open Developer Tools (F12 or Cmd+Option+I)
- Go to the Console tab
- Look for "Processing medication" and "Parsed medication name" logs
- Use `inspectPatient("patient-id")` in console for detailed patient data inspection

## Features for Future Enhancement

- Additional vital signs (heart rate, respiratory rate, oxygen saturation)
- Cholesterol and lipid panel integration
- Patient risk assessment scores (Framingham, etc.)
- Medication interaction checking
- Historical trend analysis
- PDF report generation
- Multi-patient comparison

## Course Information

**Course**: [INSERT COURSE NAME AND NUMBER HERE]  
**Institution**: [INSERT INSTITUTION NAME HERE]  
**Term**: Fall 2025  
**Instructor**: [INSERT INSTRUCTOR NAME HERE]  
**Project Type**: Final Project  

## Author

Developed as a final project for healthcare IT education.

## License

This project is provided as-is for educational purposes.

## Acknowledgments

- FHIR R3 Test Server (https://r3.smarthealthit.org)
- Chart.js documentation and community
- FHIR Client library contributors

## Support & Troubleshooting

**Issue**: Dashboard shows "Error connecting to FHIR server"
- Check internet connection
- Verify FHIR server is accessible
- Check browser console for CORS errors

**Issue**: Medications showing as "Unknown"
- Verify patient has active MedicationRequest resources
- Check browser console for medication fetch errors
- Ensure Medication resources exist in the database

**Issue**: No vital signs data displayed
- Confirm patient has Observation resources with correct LOINC codes
- Increase `_count` parameter in API queries if needed

For additional support, check the console logs with F12 Developer Tools.
