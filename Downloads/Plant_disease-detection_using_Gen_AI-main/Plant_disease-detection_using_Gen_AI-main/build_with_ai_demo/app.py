# Required Libraries
import os
from google import genai
from google.genai import types
import gradio as gr
from PIL import Image

# 🔑 Add your API key here (or set GEMINI_API_KEY environment variable)
api_key = os.getenv("GEMINI_API_KEY", "AIzaSyDmRc70kA2_VROl_HZ8OtjWXFCtN9PUiDE")

# ✅ Initialize the Gemini client
genai_client = genai.Client(api_key=api_key)

# 🧠 Prompt
input_prompt = """This image shows a plant with a possible disease or pest infestation.
Analyze the image and identify the disease.

Provide:
1. Disease name
2. Explanation
3. Remedies
4. Prevention tips
5. Indian agriculture website links
6. Helpline numbers in India

User symptoms: """

# ✅ Generate response using Gemini API
def generate_gemini_response(text_input, image_path):
    try:
        # Create the prompt
        prompt = input_prompt + text_input
        
        # Upload the image file
        image_file = genai_client.files.upload(file=image_path)
        
        # Generate content with image (using gemini-2.5-flash which supports vision)
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                prompt,
                image_file
            ]
        )
        
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"


# ✅ Upload handler
def upload_file(file, text_input):
    if file is None:
        return None, "No image uploaded"

    try:
        # Get the file path
        file_path = file.name
        
        # Display the image
        image = Image.open(file_path)
        
        # Generate response
        response = generate_gemini_response(text_input, file_path)
        
        return image, response

    except Exception as e:
        return None, f"Error: {str(e)}"


# 🎨 Custom CSS for nature theme
custom_css = """
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Playfair+Display:wght@400;600;700&display=swap');

/* Global Styles */
* {
    font-family: 'Poppins', sans-serif;
}

/* Main Container */
.gradio-container {
    background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 50%, #a5d6a7 100%);
    min-height: 100vh;
}

/* Header */
.gradio-container .gr-markdown h2 {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    color: #1b5e20;
    text-align: center;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 0.5rem;
}

.gradio-container .gr-markdown p {
    font-size: 1.1rem;
    color: #2e7d32;
    text-align: center;
}

/* Cards */
.gr-box {
    background: rgba(255, 255, 255, 0.95) !important;
    border-radius: 20px !important;
    border: 2px solid #a5d6a7 !important;
    box-shadow: 0 8px 32px rgba(27, 94, 32, 0.15) !important;
    backdrop-filter: blur(10px);
}

/* Buttons */
.gr-button {
    background: linear-gradient(135deg, #43a047 0%, #2e7d32 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3) !important;
}

.gr-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(46, 125, 50, 0.4) !important;
    background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%) !important;
}

/* Textbox */
.gr-textbox {
    border-radius: 12px !important;
    border: 2px solid #a5d6a7 !important;
    background: #f1f8e9 !important;
}

.gr-textbox:focus {
    border-color: #43a047 !important;
    box-shadow: 0 0 0 3px rgba(67, 160, 71, 0.2) !important;
}

/* Labels */
.gr-form label {
    color: #1b5e20 !important;
    font-weight: 600;
}

/* Image Container */
.gr-image {
    border-radius: 15px !important;
    border: 2px solid #a5d6a7 !important;
    overflow: hidden;
}

/* Result Textbox */
#result_output {
    background: linear-gradient(135deg, #f1f8e9 0%, #e8f5e9 100%) !important;
    border: 2px solid #81c784 !important;
    border-radius: 15px !important;
    color: #1b5e20 !important;
    font-size: 0.95rem;
    line-height: 1.6;
}

/* Examples */
.gr-examples {
    background: rgba(255, 255, 255, 0.9) !important;
    border-radius: 15px !important;
    border: 2px solid #a5d6a7 !important;
    padding: 20px !important;
}

.gr-examples .gr-label {
    color: #1b5e20 !important;
    font-weight: 600;
    font-size: 1.1rem;
}

/* Example Gallery */
.gr-gallery {
    border-radius: 12px !important;
    border: 2px solid #c8e6c9 !important;
}

/* Footer */
footer {
    text-align: center;
    padding: 20px;
    color: #2e7d32;
    font-size: 0.9rem;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #e8f5e9;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #a5d6a7 0%, #43a047 100%);
    border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #43a047 0%, #2e7d32 100%);
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.gr-box {
    animation: fadeIn 0.5s ease-out;
}

/* Leaf decoration */
.gradio-container::before {
    content: '🌿';
    position: fixed;
    top: 20px;
    left: 20px;
    font-size: 3rem;
    opacity: 0.3;
    z-index: -1;
}

.gradio-container::after {
    content: '🍃';
    position: fixed;
    bottom: 20px;
    right: 20px;
    font-size: 3rem;
    opacity: 0.3;
    z-index: -1;
}
"""

# 🎨 UI with custom theme
with gr.Blocks(css=custom_css) as demo:
    
    # Header
    gr.HTML("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 2.8rem; color: #1b5e20; margin-bottom: 0.5rem; font-family: 'Playfair Display', serif;">
            🌿 Plant Disease Detection
        </h1>
        <p style="font-size: 1.2rem; color: #2e7d32; margin-top: 0;">
            Powered by Google Gemini AI • Identify plant diseases instantly
        </p>
    </div>
    """)
    
    # Main content area
    with gr.Row(equal_height=True):
        # Left panel - Input
        with gr.Column(scale=1):
            gr.Markdown("### 📤 Upload Plant Image")
            
            text_input = gr.Textbox(
                label="🌱 Describe Symptoms (Optional)",
                placeholder="e.g., leaves turning yellow with brown spots, wilting...",
                lines=4,
                elem_classes=["symptom-input"]
            )
            
            upload_button = gr.UploadButton(
                "📸 Click to Upload Plant Image",
                file_types=["image"],
                file_count="single",
                variant="primary",
                size="lg"
            )
            
            gr.Markdown("""
            **Supported formats:** JPG, PNG, WebP
            **Max size:** 10MB
            """)
        
        # Right panel - Output
        with gr.Column(scale=1):
            gr.Markdown("### 🔬 Analysis Results")
            
            image_output = gr.Image(
                label="Uploaded Image",
                type="pil",
                height=300,
                interactive=False
            )
    
    # Results section
    result_output = gr.Textbox(
        label="📋 Diagnosis & Treatment Recommendations",
        lines=18,
        elem_id="result_output"
    )
    
    # Processing status
    status_text = gr.Textbox(
        label="Status",
        interactive=False,
        visible=False
    )
    
    # Examples section
    gr.Markdown("### 📚 Try These Examples")
    
    gr.Examples(
        examples=[
            ["planT_disesase.jpg", "Yellow spots on leaves, some browning at edges"],
            ["Tobacco-Mosaic-Virus-GettyImages-1200783801.webp", "Mosaic pattern, mottled yellow and green"],
            ["Fusarium-Wilt-GettyImages-1221194369.jpg", "Wilting, yellowing lower leaves"]
        ],
        inputs=[upload_button, text_input],
        label="Click an example to load a sample image and symptoms",
        examples_per_page=3
    )
    
    # Footer
    gr.HTML("""
    <div style="text-align: center; padding: 2rem 0; margin-top: 2rem; border-top: 2px solid #a5d6a7;">
        <p style="color: #2e7d32; font-size: 0.9rem;">
            🌍 Built with ❤️ for sustainable agriculture | 
            <a href="https://ai.google.dev/" style="color: #1b5e20; text-decoration: none;">Powered by Google Gemini AI</a>
        </p>
        <p style="color: #66bb6a; font-size: 0.8rem; margin-top: 0.5rem;">
            For educational purposes only. Consult agricultural experts for professional advice.
        </p>
    </div>
    """)

# 🚀 Launch app
if __name__ == "__main__":
    demo.launch(
        debug=True,
        server_name="0.0.0.0",
        server_port=7860,
        theme=gr.themes.Soft(
            primary_hue="green",
            secondary_hue="lime",
            neutral_hue="gray",
            radius_size=gr.themes.sizes.radius_lg,
            font=("Poppins", "sans-serif"),
            font_mono=("Courier New", "monospace")
        )
    )
