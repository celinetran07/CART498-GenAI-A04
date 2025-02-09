from flask import Flask, render_template, request
from openai import OpenAI  # Import the new OpenAI client
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Initialize the new OpenAI client

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_url = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        try:
            # Generate Jungian interpretation using the new API
            response = client.chat.completions.create(
                model="gpt-4", 
                messages=[
                    {"role": "system", "content": "You are a Jungian psychoanalyst. Analyze the user's dream using Carl Jung's theories. Focus on archetypes, the collective unconscious, and individuation. Explore the symbolic meaning of figures, actions, and settings, and connect them to the dreamer's emotions and personal growth. Provide a concise interpretation (around 150 words) that is insightful and easy to understand, helping the dreamer uncover messages from their unconscious mind."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            result = response.choices[0].message.content

            # Generate image using DALL-E
            image_response = client.images.generate(
                prompt=f"Visual representation of the dream: {prompt}",
                n=1,
                size="1024x1024"
            )
            image_url = image_response.data[0].url

        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template("index.html", result=result, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)  # Run locally for testing