# backend_service_improvements

## Backend Service - Digital Biomarker Data Collection Service

This project provides a Flask-based backend service for collecting digital biomarker data from patients enrolled in experiments.

---


## Features
- Collects patient and experiment data via REST API
- Simple in-memory storage for quick prototyping
- Input validation and logging included 

## Project Structure

```
backendservice/
├── app.py                   
├── datastructure.py         
├── datastructure_test.py   
├── memory.py               
├── idgenerator.py          
├── requirements.txt        
├── *.json (dev_env.json)   
├── backend_service.log     
```

---

## How to Run

```
# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment file if needed
export WORKING_ENV=dev_env.json

# Run the service
python app.py
```

Service will start at: `http://127.0.0.1:5000`

---

## Postman API Test Summary

- `GET /` with basic auth (`user:password`) returns project metadata
- `POST /patient` with `{ "name": "Dr. House" }` returns valid patient object
- `POST /experiment` with `{ "name": "It’s always Lupus" }` creates experiment
- `POST /upload` with references to valid IDs uploads a datapoint

**Screenshots available covering:**
- GET `/`
- POST `/patient`
- POST `/experiment`
- POST `/upload`

---

## ⚡ Pylint Improvements

- **Scores:** 4.66-7.73/10 

**Improvements Made:**
- Added docstrings to all routes and functions
- Replaced invalid variable names (e.g., `id`, `ds`)
- Ordered imports
- Removed unused imports like `idgenerator`, `profile`

---

## Logging

Configured using `logging.basicConfig()`:

```python
logging.basicConfig(filename="backend_service.log", encoding='utf-8', level=logging.INFO)
```

- Logs written to `backend_service.log`
- Each route logs entry, creation, or warning messages (e.g., "Patient not found")

---

## Assertions

Added to validate input data:

```python
assert 'name' in body, "Missing 'name' in request body"
assert 'patientId' in body, "Missing 'patientId'"
```

---

## Unit Tests

- `datastructure_test.py` created
- Tests the creation of `Experiment`, `Patient`, and `DataPoint` classes

Run tests with:

```bash
python datastructure_test.py
```

---

## Git Tag

Committed and tagged in local Git repository:

```bash
git add .
git commit -m "Initial cleaned version with tests and logging"
git tag v1.0
```

---

2025, Sarah Deckarm
