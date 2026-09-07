# Exploratory Data Analysis Interface (Streamlit)

An interactive Streamlit app for uploading a CSV dataset, inspecting its metadata,
and visualizing individual columns (histogram for numerical, bar chart for categorical).

## Features
- CSV file upload with validation
- Dataset preview (first 5 rows)
- Shape, column data types, missing values (count + %)
- Basic statistics (mean, median, min, max) for numerical columns
- Dropdown to select any column
- Automatic detection of numerical vs. categorical attribute
- Dynamic histogram (numerical) or bar chart with optional percentage view (categorical)
- All controls in the sidebar; preview/metadata on top, visualization at the bottom

## Project Structure
```
eda_streamlit_app/
├── app.py
├── requirements.txt
├── Titanic-Dataset.csv   # sample/test dataset
└── README.md
```

## Run Locally
1. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   streamlit run app.py
   ```
4. In the app, upload `Titanic-Dataset.csv` (or any CSV) via the sidebar.

## Deploy to Streamlit Community Cloud
1. Push this folder to a new GitHub repository:
   ```
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin YOUR_REPOSITORY_URL
   git push -u origin main
   ```
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **Create app**, choose your repo/branch, set the main file path to `app.py`.
4. Click **Deploy**.
5. Once deployed, toggle **Make this app public** so others can access it, then copy the link.

## Notes
- Tested with `Titanic-Dataset.csv` (891 rows, 12 columns).
- For the submission, attach the deployed app link and the `.ipynb`/`app.py` file to GCR as required.
