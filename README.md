# Smart Routine Assistant

A personalized, AI-powered daily routine and meal planner that adapts to your lifestyle, dietary needs, and real-world adherence using computer vision and behavioral learning.

---

## Features

- **Custom Routine Builder:**
  - Select only the activities you want in your day (e.g., skip exercise if not needed).
  - Set your preferred start times for each activity.
- **Meal & Activity Personalization:**
  - Meals are suggested based on your dietary restrictions and allergies.
  - Only safe and suitable meals are shown for breakfast, lunch, and dinner.
- **Visual Verification (AI):**
  - Upload a photo for each meal or exercise.
  - A real image classifier (MobileNetV2 via PyTorch) verifies if the photo matches the expected category (e.g., food, exercise).
- **Behavioral Adaptation:**
  - The app learns from your actions (completed, missed, or rescheduled tasks) and can adapt future routines accordingly.
- **Routine History:**
  - View your actions for any previous day via a date picker in the sidebar.
- **Habit Parsing:**
  - Describe your morning habits in free text. The app automatically suggests activities based on keywords in your description.

---

## How to Run This Project

### 1. **Clone the Repository**
```bash
git clone <your-repo-url>
cd hackathon
```

### 2. **Set Up a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt --break-system-packages
```

### 4. **Run the App**
```bash
streamlit run app.py
```

---

## Code Structure & Implementation

### `app.py`  
- **User Profile Sidebar:**
  - Enter name, allergies, dietary restrictions, and a free-text habits field.
  - Select desired routine activities (multi-select) and set times only for those.
  - Habits field is parsed for keywords to auto-suggest activities.
- **Routine Generation:**
  - Calls `generate_routine` from `backend.py`, which uses your selections, times, allergies, and dietary restrictions.
- **Photo Upload & Verification:**
  - For each meal/exercise, upload a photo. Calls `verify_photo` from `cv_utils.py` for AI-based validation.
- **Missed Task Handling:**
  - Click to reschedule any missed task.
- **History Viewer:**
  - Date picker to view all logged actions for any day (from `routine.db`).

### `backend.py`
- **Routine Logic:**
  - Builds the daily routine based on user-selected activities and times.
  - Filters meal suggestions based on allergies and dietary restrictions.
  - Fallbacks to safe meal options if needed.
- **Meal Filtering:**
  - `filter_meal` excludes meals with forbidden ingredients.
- **Adaptation:**
  - Simple logic to reschedule missed tasks.

### `cv_utils.py`
- **Computer Vision Verification:**
  - Uses PyTorch MobileNetV2 to classify uploaded images.
  - Checks if the top predictions match food or exercise categories.

### `db.py`
- **SQLite Logging:**
  - Logs every action (timestamp, task, result) to `routine.db`.
  - Provides functions to fetch actions for a given date for history viewing.

### `requirements.txt`
- Lists all required packages, including: `streamlit`, `opencv-python`, `pillow`, `torch`, `torchvision`, `numpy`, `scikit-learn`, `sqlalchemy`, etc.

---

## Example Usage

1. **Fill out your profile:**
   - Name, allergies (e.g., "peanuts, gluten"), dietary restrictions (e.g., "vegan"), and describe your habits (e.g., "I run and skip breakfast").
2. **Select your desired activities** and set times for each.
3. **Save your profile** to generate your personalized routine.
4. **Upload photos** for meals and exercises as you complete them.
5. **View your history** for any day using the date picker.

---

## Notes & Extensibility
- Easily add new meals or activities in `backend.py`.
- To support more dietary rules, extend the `filter_meal` logic.
- To add more advanced AI/ML, enhance `cv_utils.py` or add new models.

---

## Troubleshooting
- **Torch install errors:** Use the `--break-system-packages` flag if pip blocks install.
- **First image upload is slow:** Model loads on first use.
- **Database file:** All history is stored in `routine.db` in your project folder.

---

## License
MIT (or specify your own)

## Author
Your Name Here
