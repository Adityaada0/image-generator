"""
Web interface for the image generator using Flask.
Access at http://localhost:5000
"""
import os
from flask import Flask, render_template, request, jsonify, send_file
from generate import ImageGenerator
import threading
import base64
from io import BytesIO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'outputs'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global generator instance
generator = None
generation_in_progress = False

def init_generator():
    """Initialize the image generator on startup."""
    global generator
    if generator is None:
        print("Initializing image generator...")
        generator = ImageGenerator()
        generator.build_pipeline()
        print("Generator ready!")

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_image():
    """API endpoint to generate an image."""
    global generation_in_progress
    
    if generation_in_progress:
        return jsonify({'error': 'Generation already in progress'}), 400
    
    try:
        generation_in_progress = True
        
        data = request.json
        prompt = data.get('prompt', 'a beautiful landscape')
        steps = int(data.get('steps', 20))
        height = int(data.get('height', 512))
        width = int(data.get('width', 512))
        
        # Validate inputs
        steps = max(10, min(50, steps))  # 10-50 steps
        height = max(256, min(768, height)) & ~63  # 256-768, multiple of 64
        width = max(256, min(768, width)) & ~63
        
        print(f"Generating: {prompt}")
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'generated.png')
        
        # Generate image
        generator.generate(
            prompt=prompt,
            steps=steps,
            height=height,
            width=width,
            output_path=output_path
        )
        
        # Convert to base64 for response
        with open(output_path, 'rb') as f:
            img_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        return jsonify({
            'success': True,
            'image': f'data:image/png;base64,{img_base64}',
            'path': output_path
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        generation_in_progress = False

@app.route('/api/status', methods=['GET'])
def status():
    """Check if generation is in progress."""
    return jsonify({'in_progress': generation_in_progress})

if __name__ == '__main__':
    init_generator()
    app.run(debug=False, host='localhost', port=5000)
