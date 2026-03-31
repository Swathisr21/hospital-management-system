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


# 🎨 UI
with gr.Blocks() as demo:
    gr.Markdown("## 🌿 Plant Disease Detection using AI")
    gr.Markdown("""
    Upload an image of a plant leaf to detect diseases and get treatment recommendations.
    Powered by Google Gemini AI.
    """)

    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(
                label="Describe symptoms (optional)",
                placeholder="e.g., leaves turning yellow with spots",
                lines=3
            )
            
            upload_button = gr.UploadButton(
                "📤 Click to upload plant image",
                file_types=["image"],
                file_count="single",
                variant="primary"
            )
        
        with gr.Column():
            image_output = gr.Image(label="Uploaded Image", type="pil")
    
    result_output = gr.Textbox(
        label="🔬 Diagnosis and Remedies",
        lines=15
    )

    upload_button.upload(
        upload_file,
        inputs=[upload_button, text_input],
        outputs=[image_output, result_output]
    )
    
    # Add examples
    gr.Examples(
        examples=[
            ["planT_disesase.jpg", "Yellow spots on leaves"],
            ["Tobacco-Mosaic-Virus-GettyImages-1200783801.webp", "Mosaic pattern on leaves"],
            ["Fusarium-Wilt-GettyImages-1221194369.jpg", "Wilting and yellowing"]
        ],
        inputs=[upload_button, text_input],
        label="Try these examples (click to upload)"
    )

# 🚀 Launch app
if __name__ == "__main__":
    demo.launch(debug=True, server_name="0.0.0.0", server_port=7860)