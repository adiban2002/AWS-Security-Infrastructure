import os
import uvicorn
from app.main import app 


HOST = "0.0.0.0"
PORT = int(os.getenv("PORT", 8003))  

if __name__ == "__main__":
    print(f">>> FindMyProject Server Starting...")
    print(f">>> Interface: {HOST}:{PORT}")
    print(f">>> Domain: https://findmyproject.com")
    
    uvicorn.run(
        "app.main:app", 
        host=HOST,
        port=PORT,
        reload=False,        
        workers=1,           
    )