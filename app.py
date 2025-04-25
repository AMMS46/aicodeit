import re
import textwrap
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
# Replace with your actual API key

os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")

code_iteration_template = """
You are a coding assistant that helps game developers improve their code.
The developer will provide a code snippet and a prompt describing desired changes.
Your task is to suggest modified code that fulfills the prompt, along with a clear explanation.

Follow these steps:

1.  Understand the Prompt: Carefully analyze the developer's prompt to determine the exact code modifications requested.  Focus on the specific changes, not the overall program logic.

2.  Identify Relevant Code:  Pinpoint the specific parts of the provided code snippet that need to be changed to satisfy the prompt.

3.  Apply Changes:  Modify the code according to the prompt.  Do not add new functionality or change the program's behavior beyond what is explicitly requested.

4.  Explain Changes:  Provide a concise explanation of the modifications made.  Focus on *what* was changed and *why*, not on the overall code.

5.  Return Output:  Return the modified code snippet and the explanation.

Example:
Prompt: "Rename the variable 'player_speed' to 'speed'."
Code Snippet:
```python
def update_player_position(player_speed, direction):
    new_position = player_speed * direction
    return new_position
```
Response:
```
Explanation: Renamed the variable 'player_speed' to 'speed' in the function definition and within the function body.

Modified Code:
```python
def update_player_position(speed, direction):
    new_position = speed * direction
    return new_position
```

Prompt: {prompt}
Code Snippet:
{code_snippet}
Response:
"""

code_iteration_prompt = PromptTemplate(
    input_variables=["prompt", "code_snippet"],
    template=code_iteration_template,
)

def main():
    st.title("AI Code Iterator for Game Developers")

    # Initialize the LLM
    llm = GoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2, google_api_key=os.getenv("GOOGLE_API_KEY"))
    chain = code_iteration_prompt | llm

    # Input areas for prompt and code snippet
    prompt = st.text_area("Enter your prompt:", "Rename the variable 'player_speed' to 'speed'.")
    code_snippet = st.text_area("Enter your code snippet:",
                               """def update_player_position(player_speed, direction):
    new_position = player_speed * direction
    return new_position""")

    if st.button("Generate Modified Code"):
        with st.spinner("Processing..."):
            response = chain.invoke({"prompt": prompt, "code_snippet": code_snippet})

        # Basic parsing of the response
        explanation_match = re.search(r"Explanation:(.*)Modified Code:", response, re.DOTALL)
        code_match = re.search(r"Modified Code:\n(.*?)$", response, re.DOTALL)

        explanation = ""
        modified_code = ""

        if explanation_match:
            explanation = explanation_match.group(1).strip()
        if code_match:
            modified_code = code_match.group(1).strip()

        st.subheader("Explanation:")
        st.write(explanation)

        st.subheader("Modified Code:")
        st.code(modified_code, language="python")  # Use st.code for formatted output

if __name__ == "__main__":
    main()
