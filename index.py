from flask import Flask, render_template_string, request, redirect, url_for
import jwt

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>JWT Token Generator</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .toast {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px;
            background-color: #28a745;
            color: white;
            border-radius: 5px;
            display: none;
            z-index: 1000;
        }
        .pre-copy {
            position: relative;
        }
        .copy-btn {
            position: absolute;
            top: 5px;
            right: 5px;
        }
    </style>
</head>
<body class="container mt-5">
    <div id="copyToast" class="toast">
        Copied to clipboard!
    </div>
    
    <h1>JWT Token Generator</h1>
    <form method="post" action="/" class="mt-4" id="tokenForm">
        <div class="form-group">
            <label for="secret_key">Secret Key:</label>
            <input type="text" class="form-control" id="secret_key" name="secret_key" required>
        </div>

        <div class="form-group">
            <label for="store_id">Store ID:</label>
            <input type="text" class="form-control" id="store_id" name="store_id" required>
        </div>

        <div class="form-group">
            <label for="sync_with_ai">Sync with AI:</label>
            <input type="text" class="form-control" id="sync_with_ai" name="sync_with_ai" required>
        </div>

        <button type="submit" class="btn btn-primary">Generate Token</button>
    </form>
    {% if token %}
    <div class="mt-4">
        <h3>Generated Token:</h3>
        <div class="pre-copy">
            <pre id="tokenText" class="bg-light p-3">{{ token }}</pre>
            <button onclick="copyToken()" class="btn btn-sm btn-secondary copy-btn">Copy</button>
        </div>
    </div>
    {% endif %}

    <script>
        // Clear form on page load
        window.onload = function() {
            document.getElementById('tokenForm').reset();
            {% if token %}
            copyToken();
            {% endif %}
        };

        // Prevent form resubmission on page reload
        if (window.history.replaceState) {
            window.history.replaceState(null, null, window.location.href);
        }

        function copyToken() {
            const tokenText = document.getElementById('tokenText').innerText;
            navigator.clipboard.writeText(tokenText).then(function() {
                showToast();
            }).catch(function(err) {
                console.error('Failed to copy text: ', err);
            });
        }

        function showToast() {
            const toast = document.getElementById('copyToast');
            toast.style.display = 'block';
            setTimeout(function() {
                toast.style.display = 'none';
            }, 2000);
        }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template_string(html_template, token=None)
    
    if request.method == 'POST':
        secret_key = request.form['secret_key']
        store_id = request.form['store_id']
        sync_with_ai = request.form['sync_with_ai']
        
        payload = {
            "store_id": store_id,
            "sync_with_ai": sync_with_ai
        }
        
        try:
            token = jwt.encode(payload, secret_key, algorithm="HS256")
            return render_template_string(html_template, token=token)
        except Exception as e:
            token = f"Error: {str(e)}"
            return render_template_string(html_template, token=token)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)