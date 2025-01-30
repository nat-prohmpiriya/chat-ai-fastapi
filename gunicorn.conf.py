# Server Socket
bind = "0.0.0.0:80"
backlog = 2048

# Worker Processes
workers = 4  # จำนวน workers (2-4 x NUM_CORES)
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 30
keepalive = 2

# Process Naming
proc_name = "fastapi_demo"

# Logging
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = "info"

# SSL
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Server Mechanics
preload_app = True
reload = False  # ไม่ใช้ auto-reload ใน production
spew = False
daemon = False

# Server Hooks
def on_starting(server):
    pass

def on_reload(server):
    pass

def when_ready(server):
    pass