import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = int(os.environ.get("PORT", 10000))
HOST = "0.0.0.0"
TARGET_FILE = "homepage.html"

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Intercept root request "/"
        if self.path == "/":
            self.path = f"/{TARGET_FILE}"
        
        # Prevent directory listing if path ends in /
        if self.path.endswith("/"):
            self.path += TARGET_FILE
            
        return super().do_GET()

    def log_message(self, format, *args):
        # Cleaner logs for debugging
        print(f"[{self.log_date_time_string()}] {format % args}")

def main():
    if not os.path.exists(TARGET_FILE):
        print(f"[-] Error: {TARGET_FILE} not found in current directory ({os.getcwd()})")
        # List contents for debug
        print("Contents:", os.listdir("."))
        sys.exit(1)

    print(f"[+] Serving {TARGET_FILE} as index on http://{HOST}:{PORT}")
    
    # Change dir to where homepage.html lives (repo root)
    # If it's in a subfolder like 'web/', change os.chdir(".") to os.chdir("web/")
    os.chdir(".") 
    
    httpd = HTTPServer((HOST, PORT), CustomHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
