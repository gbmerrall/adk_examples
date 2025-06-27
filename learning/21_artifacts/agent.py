from google.adk.agents import LlmAgent
from google.adk.tools import load_artifacts
from google.adk.tools import ToolContext
from google.genai import types


from fpdf import FPDF
import string

def make_filename(text: str) -> str:
    """
    Removes all punctuation from a given string.
    """
    # Create a translation table that maps each punctuation character to None
    translator = str.maketrans('', '', string.punctuation)
    # Use the translate method to remove punctuation
    cleaned_text = text.translate(translator)

    # now just jam together the first 3 words with underscores
    cleaned_text = cleaned_text.split()[:3]
    cleaned_text = "_".join(cleaned_text)+".pdf"
    return cleaned_text


async def generate_pdf(text: str, tool_context: 'ToolContext') -> dict[str, str, str]:
    """
    Generates a PDF with the given text.

    Args:
        text: The text to generate a PDF from.
        tool_context: The tool context to save the PDF to.
    Returns:
        A dictionary with the status, detail, and filename of the PDF.
    """

    filename = make_filename(text)
    print(f"Generated filename: {filename}")  # Debug line

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=text, ln=1, align="C")

    # this should be a bytes object
    pdf_bytes = pdf.output(dest='S').encode('latin-1')

    # convert to base64?
    # pdf_bytes = base64.b64encode(pdf_bytes).decode('utf-8')

    await tool_context.save_artifact(
        filename,
        types.Part.from_bytes(data=pdf_bytes, mime_type='application/pdf'),
    )    

    return {
        'status': 'success',
        'detail': 'Created the PDF you asked for!',
        'filename': filename,
    }

root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='pdf_agent',
    description="An agent that generates PDFs from text submitted by the user.",
    instruction="""You are an agent whose job is to generate a PDF from the text 
        submitted by the user. The PDF should be named based on the supplied filename.""",
    tools=[generate_pdf, load_artifacts],
)