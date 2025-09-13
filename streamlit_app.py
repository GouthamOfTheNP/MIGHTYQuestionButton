import streamlit as st
from google import genai
import os

from google.api_core.exceptions import ServerError

client = genai.Client(api_key=os.getenv("GEMINI_API"))

st.set_page_config(page_title="MIGHTY Question Button", page_icon=":brain:")
st.title("The MIGHTY Question Button")
st.badge("Up-to-date", color="blue")
st.write("Press the MIGHTY Question Button to generate a challenging, thought-provoking practice question tailored to AP and SAT topics. Perfect for sharpening your problem-solving skills in a fun and engaging way. Side effects may include bursts of insight, sudden motivation, and an uncontrollable urge to solve “just one more” problem. 🧠⚡️")

if "question" not in st.session_state:
	st.session_state.question = None

topics = ["AP Spanish 4 MCQ Main Idea", "AP Spanish 4 MCQ Contextual", "AP Calculus AB", "AP Calculus BC", "AP Physics 1", "AP Physics 2", "AP Physics C", "AP Biology", "AP Chemistry", "AP World History", "AP United States History", "SAT Math", "SAT Reading and Writing", "Other"]
dropdown = st.selectbox("Select a topic", topics)

custom_topic = st.text_input("Enter your custom topic:") if dropdown == "Other" else "AP Spanish 4 MCQ Questions in Spanish with source article in full-text format following AP Spanish Guidelines for the length, paragraph count, and complexity of the source article, with questions focusing on specific details rather than the main idea" if dropdown == "AP Spanish 4 MCQ Contextual" else "AP Spanish 4 MCQ Questions in Spanish with source article in full-text format following AP Spanish Guidelines for the length, paragraph count, and complexity of the source article, with questions focusing on main idea" if dropdown == "AP Spanish 4 MCQ Main Idea" else ""

try:
	if st.button("Get Your Question"):
		topic_to_use = custom_topic if (dropdown == "Other" or "AP Spanish 4 MCQ" in dropdown) and custom_topic else dropdown
		question_contents = f"""Write one multiple-choice question about {topic_to_use}.
	Use this exact format:
	Question: [Your question here]  \n
	A) [Option A]  \n
	B) [Option B]  \n
	C) [Option C]  \n
	D) [Option D]  
	
	Do NOT include the answer."""
		with st.spinner("Generating your question..."):
			st.session_state.question = client.models.generate_content(
				model="gemini-2.5-flash",
				contents=question_contents,
			).text

	if st.session_state.question:
		st.markdown(st.session_state.question)
		if st.button("Reveal Answer"):
			with st.spinner("Behold the mighty answer..."):
				response = client.models.generate_content(
					model="gemini-2.5-pro",
					contents=f"Write the correct answer to the question above: {st.session_state.question}",
				)
				st.markdown(response.text)
except google.genai.errors.ServerError:
	st.error("Server is overloaded. Please try again later.")
