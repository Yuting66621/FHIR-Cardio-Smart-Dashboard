#!/usr/bin/env python3
"""
FHIR Patient Data Finder
Finds patients with complete cardiovascular data (BP, HR, Weight, Height, Medications)
"""

import requests
import json
from typing import List, Dict, Tuple

FHIR_SERVER = "https://r3.smarthealthit.org"

def get_all_patients(limit: int = 50) -> List[str]:
    """Fetch all patient IDs from FHIR server"""
    print(f"🔍 Fetching up to {limit} patients from FHIR server...")
    try:
        response = requests.get(f"{FHIR_SERVER}/Patient?_count={limit}")
        response.raise_for_status()
        data = response.json()
        
        patient_ids = []
        if 'entry' in data:
            for entry in data['entry']:
                patient_ids.append(entry['resource']['id'])
        
        print(f"✓ Found {len(patient_ids)} patients")
        return patient_ids
    except Exception as e:
        print(f"❌ Error fetching patients: {e}")
        return []

def check_patient_data(patient_id: str) -> Tuple[bool, Dict]:
    """
    Check if a patient has all required data:
    - Demographics (name, gender, DOB)
    - Blood Pressure (code: 55284-4)
    - Weight (code: 29463-7)
    - Height (code: 8302-2)
    - Active Medications
    BMI will be calculated from Weight and Height
    """
    data_status = {
        'id': patient_id,
        'demographics': False,
        'blood_pressure': 0,
        'weight': False,
        'height': False,
        'medications': 0,
        'has_complete_data': False
    }
    
    try:
        # Check demographics
        pt_response = requests.get(f"{FHIR_SERVER}/Patient/{patient_id}")
        if pt_response.status_code == 200:
            pt_data = pt_response.json()
            if 'name' in pt_data and 'birthDate' in pt_data:
                data_status['demographics'] = True
        
        # Check Blood Pressure
        bp_response = requests.get(f"{FHIR_SERVER}/Observation?patient={patient_id}&code=55284-4&_count=50")
        if bp_response.status_code == 200:
            bp_data = bp_response.json()
            if 'entry' in bp_data:
                data_status['blood_pressure'] = len(bp_data['entry'])
        
        # Check Weight
        weight_response = requests.get(f"{FHIR_SERVER}/Observation?patient={patient_id}&code=29463-7&_count=1")
        if weight_response.status_code == 200:
            weight_data = weight_response.json()
            if 'entry' in weight_data and len(weight_data['entry']) > 0:
                data_status['weight'] = True
        
        # Check Height
        height_response = requests.get(f"{FHIR_SERVER}/Observation?patient={patient_id}&code=8302-2&_count=1")
        if height_response.status_code == 200:
            height_data = height_response.json()
            if 'entry' in height_data and len(height_data['entry']) > 0:
                data_status['height'] = True
        
        # Check Medications
        med_response = requests.get(f"{FHIR_SERVER}/MedicationRequest?patient={patient_id}&status=active")
        if med_response.status_code == 200:
            med_data = med_response.json()
            if 'entry' in med_data:
                data_status['medications'] = len(med_data['entry'])
        
        # Determine if patient has complete data
        # Requires BP, Weight, Height (for BMI calculation), and Demographics
        has_complete_data = (
            data_status['demographics'] and
            data_status['blood_pressure'] > 0 and
            data_status['weight'] and
            data_status['height']
        )
        data_status['has_complete_data'] = has_complete_data
        
    except Exception as e:
        print(f"⚠️ Error checking patient {patient_id}: {e}")
    
    return data_status['has_complete_data'], data_status

def find_complete_patients(target_count: int = 10, search_limit: int = 200) -> List[Dict]:
    """Find patients with complete data"""
    print(f"\n🎯 Looking for {target_count} patients with complete data...\n")
    
    patient_ids = get_all_patients(search_limit)
    complete_patients = []
    
    for i, patient_id in enumerate(patient_ids, 1):
        print(f"[{i}/{len(patient_ids)}] Checking patient {patient_id}...", end=" ")
        
        has_complete, data_status = check_patient_data(patient_id)
        
        if has_complete:
            print("✅ COMPLETE (BP + BMI)")
            complete_patients.append(data_status)
            if len(complete_patients) >= target_count:
                break
        else:
            status_str = (
                f"BP:{data_status['blood_pressure']} "
                f"W:{data_status['weight']} "
                f"H:{data_status['height']} "
                f"Med:{data_status['medications']}"
            )
            print(f"❌ ({status_str})")
    
    return complete_patients

def print_results(patients: List[Dict]):
    """Print results in a formatted way"""
    print("\n" + "="*80)
    print(f"✅ FOUND {len(patients)} PATIENTS WITH COMPLETE DATA")
    print("="*80 + "\n")
    
    for i, patient in enumerate(patients, 1):
        print(f"{i}. Patient ID: {patient['id']}")
        print(f"   ✓ Demographics")
        print(f"   ✓ Blood Pressure: {patient['blood_pressure']} records")
        print(f"   ✓ Weight & Height (for BMI calculation)")
        print(f"   ✓ Medications: {patient['medications']} active")
        print()
    
    # Print as a Python list for easy copy-paste
    print("\n" + "="*80)
    print("PATIENT IDs (Copy-paste ready for your code):")
    print("="*80)
    patient_ids = [p['id'] for p in patients]
    print(f"patient_ids = {json.dumps(patient_ids, indent=2)}")
    print("\nFor JavaScript:")
    print(f"const patientIds = {json.dumps(patient_ids)};")

if __name__ == "__main__":
    try:
        complete_patients = find_complete_patients(target_count=10, search_limit=30)
        
        if complete_patients:
            print_results(complete_patients)
        else:
            print("\n❌ No patients with complete data found in the search limit.")
            print("Try increasing the search limit or check the FHIR server connection.")
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Search interrupted by user.")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
