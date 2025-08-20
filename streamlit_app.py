import streamlit as st
from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API"))

st.set_page_config(page_title="MIGHTY Question Button", page_icon=":brain:")
st.title("The MIGHTY Question Button")
st.badge("Up-to-date", color="blue")
st.write("SMASH THIS BUTTON!!! The MIGHTY Question Button will spit out a brain-boggling and brainrotted question just for YOU! Side effects may include sudden genius, mild panic, and a strange urge to do math in your sleep. 🧠💥💅")

if "question" not in st.session_state:
	st.session_state.question = None

dropdown = st.selectbox("Select a topic", ["AP Physics C", "AP Calculus BC", "SAT Math", "SAT Reading and Writing"])

question_contents = f"""Write one multiple-choice question that asks about a topic in {dropdown}. 
Use this exact format:
Question: [Your question here]  \n
A) [Option A]  \n
B) [Option B]  \n
C) [Option C]  \n
D) [Option D]  

Do NOT include the answer."""

if st.button("Get Your Question"):
	with st.spinner("Generating your question..."):
		st.session_state.question = client.models.generate_content(
			model="gemini-2.5-flash",
			contents=question_contents,
		).text

if st.session_state.question:
	st.markdown(st.session_state.question)

if st.session_state.question is not None and st.button("Reveal Answer"):
	with st.spinner("💥🥀 Behold the mighty answer, mere mortal..."):
		response = client.models.generate_content(
			model="gemini-2.5-pro",
			contents=f"Write the correct answer to the question above: {st.session_state.question}",
		)
		st.markdown(response.text)
