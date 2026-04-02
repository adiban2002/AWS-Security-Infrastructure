import os
import uvicorn

HOST = "0.0.0.0"
PORT = int(os.getenv("PORT", 8003))  

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=PORT,
        reload=False,        
        workers=1,           
    )