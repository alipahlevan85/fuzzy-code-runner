
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import Response

app = FastAPI()

class CodePayload(BaseModel):
code: str

@app.get("/")
def home():
return {"status": "ok"}

@app.post("/run-code")
def run_code(payload: CodePayload):
plt.close('all')
clean_code = payload.code.strip()

# حذف تگ‌های مارک‌داون کد
if clean_code.startswith("
```python"):
        clean_code = clean_code[9:]
    elif clean_code.startswith("
```"):
clean_code = clean_code[3:]

if clean_code.endswith("
```"):
        clean_code = clean_code[:-3]
        
    clean_code = clean_code.strip()

    local_vars = {"plt": plt, "np": np}
    try:
        exec(clean_code, local_vars)
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close('all')
        return Response(content=buf.getvalue(), media_type="image/png")
    except Exception as e:
        plt.close('all')
        raise HTTPException(status_code=400, detail=str(e))
