**PropAIze – AI-Powered Real Estate Dashboard**


**Overview**

**PropAIze** is an intelligent web dashboard designed to predict real estate prices and provide 
data-driven insights using Machine Learning and AI visualization.
It assists property investors, buyers, and analysts in making informed decisions backed by real data.

**Key Features**

AI-based real estate price prediction

Interactive data visualization dashboard

Batch prediction through CSV upload

Clean and modern interface built with Next.js and Tailwind CSS

Flask backend for model inference and data processing

**Tech Stack**

Frontend:	Next.js, React, Tailwind CSS

Backend:	Flask (Python)

Machine Learning:	Scikit-learn, Pandas, NumPy

Version Control:	Git & GitHub

**How to Run Locally**

**Step 1:** Clone the Repository

git clone https://github.com/Dollachaitra-0608/PropAIze-RealEstate-Dashboard.git

cd PropAIze-RealEstate-Dashboard

**Step 2:** Create and Activate a Virtual Environment

python -m venv venv

venv\Scripts\activate    # On Windows

source venv/bin/activate  # On Mac/Linux

**Step 3:** Install Dependencies

pip install -r requirements.txt

**Step 4:** Run Flask Server

python app.py

Open your browser and go to **http://127.0.0.1:5000**

**Model Information**

The model is trained on real estate data (data.csv) containing features such as:

Location

Area (sq. ft)

Bedrooms

Bathrooms

Price

The trained model is stored as model.pkl and used by Flask for making predictions.

**Contributing**

Contributions are welcome.

Please open an issue first to discuss any proposed changes before submitting a pull request.

**License**

This project is open-source and licensed under the MIT License.

**Author**

Dolla Chaitra

AI/ML & Data Expert using Python
