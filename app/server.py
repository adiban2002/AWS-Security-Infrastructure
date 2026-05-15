import os
import uvicorn
import logging


logger = logging.getLogger("uvicorn.error")

HOST = "0.0.0.0"
PORT = int(os.getenv("PORT", 8003))  

if __name__ == "__main__":
    print(f"\n{'='*50}")
    print(f">>> FindMyProject Server Starting...")
    print(f">>> Mode: Production (Cloud-Native)")
    print(f">>> Interface: {HOST}:{PORT}")
    print(f">>> Domain: https://findmyproject.com")
    print(f"{'='*50}\n")
    
    try:
        uvicorn.run(
            "app.main:app", 
            host=HOST,
            port=PORT,
            reload=False,        
            workers=1,           
            proxy_headers=True,  
            forwarded_allow_ips="*", 
            log_level="info"
        )
    except Exception as e:
        logger.error(f"Server failed to start: {e}")