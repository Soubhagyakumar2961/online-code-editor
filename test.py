from flask import Flask, request, jsonify
from flask import render_template, send_from_directory
from flask_cors import CORS
import subprocess
import tempfile
import os
result = subprocess.run(["javac", "-version"], capture_output=True, text=True)
print(result.stdout, result.stderr)
app = Flask(__name__)
CORS(app) 
def run_python_code(code):
    """Execute Python code securely using a temporary file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_file:
        temp_file.write(code)
        temp_file_name = temp_file.name
    
    try:
        result = subprocess.run(["python", temp_file_name], capture_output=True, text=True, timeout=5)
        output = result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        output = str(e)
    finally:
        os.remove(temp_file_name)  
    return output
def run_js_code(code):
    """Execute JavaScript code securely using Node.js."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False) as temp_file:
        temp_file.write(code)
        temp_file_name = temp_file.name
    try:
        result = subprocess.run(["node", temp_file_name], capture_output=True, text=True, timeout=5)
        output = result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        output = str(e)
    finally:
        os.remove(temp_file_name)  
        return output
def run_java_code(code):
    """Execute Java code securely using a temporary directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        java_file = os.path.join(temp_dir, "Main.java")
        with open(java_file, "w") as f:
            f.write(code)
        try:
            compile_result = subprocess.run(["javac", java_file], capture_output=True, text=True, timeout=5)
            if compile_result.returncode != 0:
                return compile_result.stderr  
            
            run_result = subprocess.run(["java", "-cp", temp_dir, "Main"], capture_output=True, text=True, timeout=5)
            return run_result.stdout if run_result.returncode == 0 else run_result.stderr

        except Exception as e:
            return str(e)
@app.route('/run', methods=['POST'])
def run_code():
    """API endpoint to execute code based on language."""
    data = request.get_json()
    language = data.get("language")
    code = data.get("code")

    if language == "python":
        output = run_python_code(code)
    elif language == "javascript":
        output = run_js_code(code)
    elif language == "java":
        output = run_java_code(code)
    else:
        return jsonify({"error": "Unsupported language"}), 400

    return jsonify({"output": output})

@app.route("/")
def index():
    return render_template('index1.html')

if __name__ == '__main__':
    app.run(debug=True)
