import json
import time

def lambda_handler(event, context):
    request = event['Records'][0]['cf']['request']
    headers = request['headers']
    user_agent = headers.get('user-agent', [{'value': 'unknown'}])[0]['value']
    
    SECURITY_KEY = "DevSecOps-Alpha-2026"
    KEY_HEADER = 'x-devsecops-key'
    
    bot_list = ['curl', 'python-requests', 'wget']
    is_bot = any(bot in user_agent.lower() for bot in bot_list)
    client_key = headers.get(KEY_HEADER, [{'value': ''}])[0]['value']
    
    if is_bot and client_key != SECURITY_KEY:
        return {
            'status': '403',
            'statusDescription': 'Forbidden',
            'body': json.dumps({
                "error": "Automated Access Denied",
                "message": "Please provide a valid DevSecOps Security Token.",
                "timestamp": int(time.time())
            }),
            'headers': {
                'content-type': [{'key': 'Content-Type', 'value': 'application/json'}]
            }
        }
    request['headers']['x-edge-verified'] = [{'key': 'X-Edge-Verified', 'value': 'true'}]
    request['headers']['x-edge-timestamp'] = [{'key': 'X-Edge-Timestamp', 'value': str(int(time.time()))}]

    print(f"Request verified at Edge for User-Agent: {user_agent}")
    return request