from fastapi import Request, Response
from fastapi.exceptions import RequestValidationError
from uuid import uuid4
from loguru import logger
import json
import sys

# Configure logger format
logger.configure(
    handlers=[
        {
            "sink": sys.stdout,
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {extra[request_id]} | {message}",
        }
    ]
)

async def request_middleware(request: Request, call_next):
    request_id = str(uuid4())
    request.state.request_id = request_id
    
    with logger.contextualize(request_id=request_id):
        # Log request
        body = await request.body()
        if body:
            try:
                body = json.loads(body)
            except:
                body = body.decode()
                
        logger.info(f"req: {request.method} {request.url.path} | {body}")
        
        try:
            # Original response
            response: Response = await call_next(request)
            
            # Get response body
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk
            
            # Log response
            try:
                response_json = json.loads(response_body)
            except:
                response_json = response_body.decode()
                
            logger.info(f"res: {response.status_code} | {response_json}")
            
            # Reconstruct response
            return Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )
            
        except RequestValidationError as e:
            # Log validation error
            error_response = {"detail": e.errors()}
            logger.info(f"res: 422 | {error_response}")
            return Response(
                content=json.dumps(error_response),
                status_code=422,
                media_type="application/json"
            )
