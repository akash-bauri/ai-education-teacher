def detect_intent(action):
    mapping = {
        "Explain Topic": "explain",
        "Notes": "notes",
        "MCQs": "mcqs",
        "Question Paper": "question_paper",
        "Lesson Plan": "lesson_plan",
        "Ask Question": "qa"
    }

    return mapping.get(action, "qa")
