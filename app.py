import streamlit as st
from datetime import datetime, date, time
from backend import generate_routine, adapt_schedule
from cv_utils import verify_photo
from db import get_user, save_user_action, get_actions_for_date

# ---- HEADER ----
st.markdown("""
<div style='text-align:center;'>
    <h1 style='color:#2E86C1;'>🌟 Smart Routine Assistant 🌟</h1>
    <h3 style='color:#117A65;'>Your Personalized, Adaptive Daily Planner</h3>
    <p style='font-size:1.1em;'>Build healthy habits, eat right, and stay on track with AI-powered verification and adaptive routines.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---- MOTIVATIONAL QUOTE ----
import random
quotes = [
    "Every day is a fresh start!",
    "Small steps every day lead to big results.",
    "Discipline is the bridge between goals and accomplishment.",
    "Your future is created by what you do today, not tomorrow.",
    "Consistency is more important than perfection."
]
st.info(random.choice(quotes))

# ---- HOW IT WORKS ----
with st.expander("How does this app work?", expanded=False):
    st.markdown("""
    1. **Set up your profile** (allergies, dietary needs, habits).
    2. **Choose your daily activities** and set your preferred times.
    3. **Follow your personalized routine** and upload photos as proof.
    4. **Get instant feedback** with AI-powered photo verification.
    5. **Check your progress/history** anytime!
    """)

# ---- WELCOME CARD ----
col1, col2 = st.columns([1,2])
with col1:
    # Use an emoji instead of a remote image for reliability
    st.markdown("""
    <div style='font-size:64px; text-align:center;'>✅</div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style='background-color:#E8F8F5; padding:16px; border-radius:10px;'>
    <h4 style='color:#117A65;'>Welcome!</h4>
    <p style='color:#222; font-size:1.1em;'>Ready to build your best day? Start by filling out your profile in the sidebar, or scroll down to see your routine!</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---- SIDEBAR: PROFILE & HISTORY ----
st.sidebar.header("Your Profile")
if 'user' not in st.session_state:
    st.session_state['user'] = {}

with st.sidebar:
    st.header("Your Profile")
    name = st.text_input("Name", st.session_state['user'].get('name', ''))
    allergies = st.text_input("Allergies (comma-separated)", st.session_state['user'].get('allergies', ''))
    dietary = st.text_input("Dietary Restrictions", st.session_state['user'].get('dietary', ''))
    habits = st.text_area("Describe your morning habits", st.session_state['user'].get('habits', ''))
    st.subheader("Select Activities for Your Routine")
    # List of possible activities and their default times
    activity_options = [
        ("Morning Exercise", 'ex_time', time(6,30)),
        ("Breakfast", 'bf_time', time(8,0)),
        ("Work Block", 'work_time', time(9,0)),
        ("Lunch", 'lunch_time', time(13,0)),
        ("Break/Walk", 'walk_time', time(16,0)),
        ("Dinner", 'dinner_time', time(19,0)),
    ]
    # Parse habits to suggest activities
    habit_text = habits.lower()
    habit_suggestions = []
    if 'run' in habit_text or 'jog' in habit_text:
        habit_suggestions.append('Morning Exercise')
    if 'walk' in habit_text:
        habit_suggestions.append('Break/Walk')
    if 'meditate' in habit_text or 'yoga' in habit_text:
        habit_suggestions.append('Morning Exercise')
    if 'skip breakfast' in habit_text or 'no breakfast' in habit_text:
        # Remove breakfast if present
        if 'Breakfast' in st.session_state.get('selected_activities', []):
            st.session_state['selected_activities'].remove('Breakfast')
    if 'work' in habit_text:
        habit_suggestions.append('Work Block')
    if 'late lunch' in habit_text:
        habit_suggestions.append('Lunch')
    # Auto-select activities based on habits
    auto_selected = list(set(st.session_state.get('selected_activities', []) + habit_suggestions))
    st.session_state['selected_activities'] = auto_selected
    selected_activities = st.multiselect(
        "Which activities do you want in your daily routine?",
        [a[0] for a in activity_options],
        default=st.session_state['selected_activities']
    )
    # Use session_state to remember selected activities
    if 'selected_activities' not in st.session_state:
        st.session_state['selected_activities'] = [a[0] for a in activity_options]  # default: all selected
    # Show time inputs only for selected activities
    time_inputs = {}
    for label, key, default_time in activity_options:
        if label in selected_activities:
            time_inputs[key] = st.time_input(label, st.session_state['user'].get(key, None) or default_time)
    if st.button("Save Profile"):
        user_data = {
            'name': name, 'allergies': allergies, 'dietary': dietary, 'habits': habits,
        }
        for label, key, _ in activity_options:
            if label in selected_activities:
                user_data[key] = time_inputs[key]
        user_data['selected_activities'] = selected_activities
        st.session_state['user'] = user_data
        st.session_state['selected_activities'] = selected_activities
        st.success("Profile saved!")

    st.sidebar.markdown("---")
    st.sidebar.header("View History")
    history_date = st.sidebar.date_input("Select a date to view history", value=date.today())
    history = get_actions_for_date(history_date)

    if st.sidebar.button("Show Day's Routine & Status"):
        st.sidebar.write(f"### Routine for {history_date.strftime('%Y-%m-%d')}")
        # Generate the routine for that day (simulate as if user profile is the same)
        user = st.session_state.get('user', {})
        routine = generate_routine(user)
        # Build a mapping from (task, type) to list of results
        from collections import defaultdict
        task_status = defaultdict(list)
        for t, task, result in history:
            task_status[task].append((t, result))
        for item in routine:
            status = task_status.get(item['task'], [])
            if status:
                latest = status[-1][1]
                st.sidebar.success(f"{item['time']} - {item['task']}: {latest}")
            else:
                st.sidebar.warning(f"{item['time']} - {item['task']}: Not completed")
        if not routine:
            st.sidebar.write("No routine generated for this day.")
    else:
        if history:
            st.sidebar.write(f"### Actions on {history_date.strftime('%Y-%m-%d')}")
            for t, task, result in history:
                st.sidebar.write(f"{t[11:16]} - {task}: {result}")
        else:
            st.sidebar.write("No actions found for this date.")

# Routine generation
if st.session_state['user']:
    st.header("Today's Routine")
    routine = generate_routine(st.session_state['user'])
    for i, item in enumerate(routine):
        st.subheader(f"{item['time']} - {item['task']}")
        if item['type'] == 'meal':
            st.write(f"Meal: {item['details']}")
            uploaded = st.file_uploader(f"Upload meal photo for {item['task']}", type=['jpg', 'png'], key=f"meal_{i}")
            if uploaded:
                result = verify_photo(uploaded, 'meal')
                st.write(f"Verification: {result}")
                save_user_action(st.session_state['user'], item, result)
        elif item['type'] == 'exercise':
            st.write(f"Exercise: {item['details']}")
            uploaded = st.file_uploader(f"Upload exercise photo for {item['task']}", type=['jpg', 'png'], key=f"ex_{i}")
            if uploaded:
                result = verify_photo(uploaded, 'exercise')
                st.write(f"Verification: {result}")
                save_user_action(st.session_state['user'], item, result)
        if st.button(f"Missed {item['task']}?", key=f"miss_{i}"):
            new_time = adapt_schedule(item)
            st.info(f"Rescheduled to {new_time}")
