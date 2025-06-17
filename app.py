from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
    <head>
        <title>DGR KPI Dashboard</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
                padding: 50px;
            }
            h1 { font-size: 3em; margin-bottom: 20px; }
            p { font-size: 1.2em; }
        </style>
    </head>
    <body>
        <h1>🚀 DGR KPI Dashboard</h1>
        <p>Successfully deployed on Render!</p>
        <p>This is your working Flask application.</p>
        <p>Ready to add your dashboard features!</p>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return {'status': 'healthy', 'message': 'App is running!'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)