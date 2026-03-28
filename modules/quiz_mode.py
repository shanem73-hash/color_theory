from __future__ import annotations

import csv
import io
import random
from datetime import datetime
from typing import Dict, List

import streamlit as st


QUIZ_BANK: List[Dict[str, object]] = [
    {
        "prompt": "In additive color mixing (light), what is Red + Green?",
        "choices": ["Yellow", "Blue", "Magenta", "Cyan"],
        "answer": "Yellow",
        "explanation": "In RGB additive mixing, red light plus green light makes yellow.",
    },
    {
        "prompt": "In additive color mixing (light), what is Green + Blue?",
        "choices": ["Cyan", "Yellow", "Red", "White"],
        "answer": "Cyan",
        "explanation": "Green and blue light combine to cyan.",
    },
    {
        "prompt": "In additive color mixing (light), what is Red + Blue?",
        "choices": ["Magenta", "Green", "Yellow", "Black"],
        "answer": "Magenta",
        "explanation": "Red and blue light combine to magenta.",
    },
    {
        "prompt": "In additive color mixing, what do full-intensity R + G + B produce?",
        "choices": ["White", "Black", "Gray", "Brown"],
        "answer": "White",
        "explanation": "All RGB light channels at full intensity produce white light.",
    },
    {
        "prompt": "In subtractive color mixing (pigments), what is Cyan + Yellow approximately?",
        "choices": ["Green", "Blue", "Red", "Magenta"],
        "answer": "Green",
        "explanation": "Cyan and yellow pigments absorb red and blue respectively, leaving mostly green.",
    },
    {
        "prompt": "In subtractive color mixing (pigments), what is Cyan + Magenta approximately?",
        "choices": ["Blue", "Green", "Yellow", "White"],
        "answer": "Blue",
        "explanation": "Cyan and magenta pigments leave mostly blue reflected light.",
    },
    {
        "prompt": "In subtractive color mixing (pigments), what is Magenta + Yellow approximately?",
        "choices": ["Red", "Blue", "Cyan", "White"],
        "answer": "Red",
        "explanation": "Magenta and yellow pigments leave mostly red reflected light.",
    },
    {
        "prompt": "In HSV, which channel mainly controls the color family (red, green, blue, etc.)?",
        "choices": ["Hue", "Saturation", "Value/Brightness", "Alpha"],
        "answer": "Hue",
        "explanation": "Hue determines the base color angle on the color wheel.",
    },
    {
        "prompt": "In HSV, decreasing Saturation generally makes a color look...",
        "choices": ["More gray / less vivid", "Brighter", "Darker", "More transparent"],
        "answer": "More gray / less vivid",
        "explanation": "Lower saturation reduces color purity, moving it toward gray.",
    },
    {
        "prompt": "In HSV, lowering Value (Brightness) while keeping hue and saturation fixed makes the color...",
        "choices": ["Darker", "More vivid", "Lighter", "More pastel"],
        "answer": "Darker",
        "explanation": "Value controls lightness in HSV; lowering it darkens the color.",
    },
    {
        "prompt": "Which format is commonly used in web CSS like #FF8800?",
        "choices": ["HEX", "CMYK", "LAB", "Pantone"],
        "answer": "HEX",
        "explanation": "HEX is the compact base-16 RGB notation used on the web.",
    },
    {
        "prompt": "CMYK is most directly associated with which workflow?",
        "choices": ["Printing", "LED displays", "3D rendering", "Audio mixing"],
        "answer": "Printing",
        "explanation": "CMYK represents ink channels used in many print processes.",
    },
    {
        "prompt": "In CIELAB, which axis corresponds to green↔red variation?",
        "choices": ["a*", "b*", "L*", "H"],
        "answer": "a*",
        "explanation": "In CIELAB, a* is the green (negative) to red (positive) axis.",
    },
    {
        "prompt": "In CIELAB, what does L* primarily represent?",
        "choices": ["Lightness", "Saturation", "Hue", "Ink density"],
        "answer": "Lightness",
        "explanation": "L* is perceptual lightness from dark to light.",
    },
    {
        "prompt": "Why are CIELAB/OKLab often used in color-difference tasks?",
        "choices": [
            "Distances better align with perceived differences",
            "They are native printer ink formats",
            "They use fewer channels than RGB",
            "They avoid gamma entirely in all workflows",
        ],
        "answer": "Distances better align with perceived differences",
        "explanation": "Perceptual spaces are designed so numeric distance is closer to visual difference.",
    },
    {
        "prompt": "OKLab is generally considered...",
        "choices": [
            "A newer perceptual model useful for gradients/UI work",
            "An old subtractive print model",
            "A replacement for HEX in CSS syntax",
            "A camera sensor color filter",
        ],
        "answer": "A newer perceptual model useful for gradients/UI work",
        "explanation": "OKLab is modern and often smoother than older models for interpolation and UI color operations.",
    },
]


def _init_state(total_questions: int) -> None:
    if "quiz_total" not in st.session_state:
        st.session_state.quiz_total = total_questions
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "quiz_index" not in st.session_state:
        st.session_state.quiz_index = 0
    if "quiz_answered" not in st.session_state:
        st.session_state.quiz_answered = False
    if "quiz_selected" not in st.session_state:
        st.session_state.quiz_selected = None
    if "quiz_was_correct" not in st.session_state:
        st.session_state.quiz_was_correct = None
    if "quiz_question" not in st.session_state:
        st.session_state.quiz_question = random.choice(QUIZ_BANK)
    if "quiz_results" not in st.session_state:
        st.session_state.quiz_results = []
    if "quiz_student_name" not in st.session_state:
        st.session_state.quiz_student_name = ""


def _reset_quiz(total_questions: int) -> None:
    st.session_state.quiz_total = total_questions
    st.session_state.quiz_score = 0
    st.session_state.quiz_index = 0
    st.session_state.quiz_answered = False
    st.session_state.quiz_selected = None
    st.session_state.quiz_was_correct = None
    st.session_state.quiz_question = random.choice(QUIZ_BANK)
    st.session_state.quiz_results = []


def _next_question() -> None:
    st.session_state.quiz_index += 1
    st.session_state.quiz_answered = False
    st.session_state.quiz_selected = None
    st.session_state.quiz_was_correct = None
    st.session_state.quiz_question = random.choice(QUIZ_BANK)


def _quiz_results_csv() -> bytes:
    buffer = io.StringIO()
    writer = csv.DictWriter(
        buffer,
        fieldnames=["student", "timestamp", "question", "selected", "correct_answer", "correct", "explanation"],
    )
    writer.writeheader()
    for row in st.session_state.quiz_results:
        writer.writerow(row)
    return buffer.getvalue().encode("utf-8")


def render() -> None:
    st.subheader("Quiz Mode (Classroom Assignments)")
    st.caption("Predict the result first, then reveal your score.")

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        total_questions = st.selectbox("Assignment length", [5, 10, 15], index=1)
    with col2:
        st.session_state.quiz_student_name = st.text_input("Student name", value=st.session_state.quiz_student_name)
    with col3:
        st.markdown(" ")
        if st.button("Start New Assignment", type="primary"):
            _reset_quiz(total_questions)

    _init_state(total_questions)

    # Keep selected length synced if user changes before starting.
    if st.session_state.quiz_index == 0 and not st.session_state.quiz_answered:
        st.session_state.quiz_total = total_questions

    score = st.session_state.quiz_score
    idx = st.session_state.quiz_index
    total = st.session_state.quiz_total

    progress = min(idx / max(total, 1), 1.0)
    st.progress(progress, text=f"Progress: {idx}/{total} | Score: {score}")

    if idx >= total:
        percent = (score / total) * 100 if total else 0
        st.success(f"Assignment complete! Final score: {score}/{total} ({percent:.0f}%)")
        if percent >= 90:
            st.balloons()

        filename = f"quiz_results_{(st.session_state.quiz_student_name or 'student').replace(' ', '_')}.csv"
        st.download_button(
            "Download Results CSV",
            data=_quiz_results_csv(),
            file_name=filename,
            mime="text/csv",
            use_container_width=False,
        )
        st.info("Click **Start New Assignment** to run another quiz.")
        return

    q = st.session_state.quiz_question
    prompt = q["prompt"]
    choices = list(q["choices"])  # type: ignore[arg-type]
    answer = q["answer"]

    st.markdown(f"### Question {idx + 1}")
    st.write(prompt)

    selected = st.radio(
        "Choose one:",
        choices,
        key=f"quiz_radio_{idx}",
        index=None,
    )

    if not st.session_state.quiz_answered:
        if st.button("Submit Answer", type="primary"):
            if selected is None:
                st.warning("Pick an answer first.")
                return
            st.session_state.quiz_selected = selected
            is_correct = selected == answer
            st.session_state.quiz_was_correct = is_correct
            st.session_state.quiz_answered = True
            if is_correct:
                st.session_state.quiz_score += 1

            st.session_state.quiz_results.append(
                {
                    "student": st.session_state.quiz_student_name,
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                    "question": prompt,
                    "selected": selected,
                    "correct_answer": answer,
                    "correct": "yes" if is_correct else "no",
                    "explanation": q["explanation"],
                }
            )
            st.rerun()
    else:
        if st.session_state.quiz_was_correct:
            st.success("Correct ✅")
        else:
            st.error(f"Not quite. Correct answer: **{answer}**")
        st.caption(q["explanation"])

        if st.button("Next Question"):
            _next_question()
            st.rerun()
