from config import APP_ENV
import uvicorn, os

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    debug = APP_ENV == 'development'
    uvicorn.run("src.main:app", host="0.0.0.0", port=port, reload=debug)