from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Folder aur File setup
DATA_FOLDER = "saved_accounts"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

ACCOUNTS_FILE = os.path.join(DATA_FOLDER, "accounts.txt")

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "online", "message": "FF Level Checker API is running successfully!"}), 200

@app.route('/upload_batch', methods=['POST'])
def upload_batch():
    try:
        data = request.get_json()
        server = data.get('server', 'IND')
        accounts = data.get('accounts', []) # List of "uid:pass"
        
        if not accounts:
            return jsonify({"status": "error", "message": "Koi account nahi mila!"}), 400
        
        # File me save karna (uid:pass:server format me)
        with open(ACCOUNTS_FILE, "a") as f:
            for acc in accounts:
                f.write(f"{acc}:{server}\n")
                
        # Total counts nikalna
        with open(ACCOUNTS_FILE, "r") as f:
            total_lines = len(f.readlines())
            
        return jsonify({
            "status": "success", 
            "message": f"Successfully added {len(accounts)} accounts!",
            "total_saved": total_lines
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get_stats', methods=['GET'])
def get_stats():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as f:
            count = len(f.readlines())
        return jsonify({"status": "success", "total_accounts": count}), 200
    return jsonify({"status": "success", "total_accounts": 0}), 200

# 👇 Naya Route: /show (Jisse browser me saari IDs dikh jayengi)
@app.route('/show', methods=['GET'])
def show_accounts():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as f:
            content = f.read()
        
        # Agar file khali hai
        if not content.strip():
            return "<h3>Folder me abhi koi account save nahi hai!</h3>", 200
            
        # Browser me saari IDs ko ek line me ya clean format me dikhane ke liye
        # HTML <pre> tag lagane se formatting kharab nahi hoti
        html_output = f"""
        <html>
            <head><title>Saved Accounts List</title></head>
            <body style="background-color: #121212; color: #00ff00; font-family: monospace; padding: 20px;">
                <h2>Saved Accounts & Levels Data:</h2>
                <pre style="background: #1e1e1e; padding: 15px; border-radius: 5px; border: 1px solid #333;">{content}</pre>
            </body>
        </html>
        """
        return html_output, 200
    else:
        return "<h3>accounts.txt file abhi create nahi hui hai!</h3>", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
