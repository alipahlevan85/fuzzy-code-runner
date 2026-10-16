  import io
  import re
  from fastapi import FastAPI
  from fastapi.responses import Response
  import matplotlib
  from pydantic import BaseModel

  # تنظیم بک‌اند به حالت غیرتعاملی تا روی سرور بدون صفحه نمایش کار کند
  matplotlib.use("Agg")
  import matplotlib.pyplot as plt

  app = FastAPI()


  class CodeRequest(BaseModel):
    code: str


  @app.post("/run-code")
  def run_code(req: CodeRequest):
    code = req.code
    # پاک‌سازی تگ‌های احتمالی مارک‌داون
    code = re.sub(r"
```(?:python)?", "", code)
code = code.replace("
```", "")

    # پاک کردن اشکال قبلی
    plt.close("all")

    # اجرای کد
    local_env = {}
    exec(code, globals(), local_env)

    # ذخیره تصویر در حافظه
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    plt.close("all")
    buf.seek(0)

    return Response(content=buf.getvalue(), media_type="image/png")
