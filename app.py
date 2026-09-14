import streamlit as st
from pypdf import PdfReader

from agent import generate_notes
from quiz import generate_quiz
from self_correction import evaluate_answer


st.set_page_config(
    page_title="StudyMate AI",
    page_icon="📚",
    layout="wide"
)

st.title("📚 StudyMate AI")
st.subheader("Your self-correcting PDF study assistant")

st.write(
    "Upload your study material, generate simple notes, "
    "test yourself, and get simpler explanations when you make mistakes."
)


# ---------------------------------------------------
# PDF UPLOAD
# ---------------------------------------------------

uploaded_file = st.file_uploader(
    "📄 Upload your study PDF",
    type=["pdf"]
)


if uploaded_file:

    reader = PdfReader(uploaded_file)

    st.success(
        f"PDF uploaded successfully — {len(reader.pages)} pages"
    )

    # ---------------------------------------------------
    # EXTRACT TEXT
    # ---------------------------------------------------

    pages = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        pages.append(page_text)

    # ---------------------------------------------------
    # GENERATE NOTES
    # ---------------------------------------------------

    if st.button("📝 Generate Study Notes"):

        chunk_size = 1
        chunks = []

        for i in range(0, len(pages), chunk_size):

            chunk = "\n".join(
                pages[i:i + chunk_size]
            )

            if chunk.strip():
                chunks.append(chunk)

        st.write(
            f"Processing {len(chunks)} sections..."
        )

        progress = st.progress(0)

        all_notes = []

        for i, chunk in enumerate(chunks):

            st.write(
                f"📖 Processing section {i + 1} "
                f"of {len(chunks)}..."
            )

            with st.spinner(
                f"Agent is studying section {i + 1}..."
            ):

                notes = generate_notes(chunk)

            all_notes.append(
                f"## Section {i + 1}\n\n{notes}"
            )

            progress.progress(
                (i + 1) / len(chunks)
            )

        final_notes = "\n\n---\n\n".join(
            all_notes
        )

        # Save notes in session
        st.session_state["notes"] = final_notes

        # Save source material for quiz
        st.session_state["study_material"] = "\n".join(
            chunks
        )

        st.success(
            "✅ Notes generated successfully!"
        )


# ---------------------------------------------------
# DISPLAY NOTES
# ---------------------------------------------------

if "notes" in st.session_state:

    st.divider()

    st.header("📝 Your Study Notes")

    st.markdown(
        st.session_state["notes"]
    )

    # ---------------------------------------------------
    # QUIZ
    # ---------------------------------------------------

    st.divider()

    st.header("🧠 Self-Check Quiz")

    if st.button("Generate 3-Question Quiz"):

        with st.spinner(
            "Agent is creating your quiz..."
        ):

            quiz = generate_quiz(
                st.session_state["study_material"]
            )

        st.session_state["quiz"] = quiz

        st.success(
            "✅ Quiz generated!"
        )


# ---------------------------------------------------
# SHOW QUIZ
# ---------------------------------------------------

if "quiz" in st.session_state:

    st.markdown(
        st.session_state["quiz"]
    )

    st.divider()

    st.header("✍️ Test Yourself")

    question = st.text_area(
        "Paste one quiz question here:"
    )

    student_answer = st.text_input(
        "Your answer:"
    )

    if st.button("Check My Answer"):

        if question and student_answer:

            with st.spinner(
                "🤖 Agent is evaluating your answer..."
            ):

                feedback = evaluate_answer(
                    topic="Study material",
                    question=question,
                    student_answer=student_answer,
                    study_material=st.session_state[
                        "study_material"
                    ]
                )

            st.subheader(
                "🤖 Agent Feedback"
            )

            st.markdown(
                feedback
            )

            # ---------------------------------------------------
            # SELF-CORRECTING LOOP
            # If the agent's feedback indicates the answer was
            # wrong, automatically regenerate a simpler explanation
            # without the student having to ask.
            # ---------------------------------------------------

            if "incorrect" in feedback.lower() or "needs correction" in feedback.lower():

                with st.spinner(
                    "Agent noticed you're struggling — simplifying this topic..."
                ):

                    simpler_notes = generate_notes(
                        f"The student struggled with this concept. Re-explain it in an "
                        f"even simpler way, using short sentences and a concrete analogy.\n\n"
                        f"ORIGINAL QUESTION:\n{question}\n\n"
                        f"RELEVANT MATERIAL:\n{st.session_state['study_material'][:1500]}"
                    )

                st.info(
                    "📘 Here's a simpler explanation, generated automatically:"
                )

                st.markdown(
                    simpler_notes
                )

        else:

            st.warning(
                "Please enter both the question and your answer."
            )