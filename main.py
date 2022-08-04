from fastapi import FastAPI

app = FastAPI()

@app.post("/auth/regist_user")
def regist_user():
    pass

@app.post("/auth/login_user")
def login_user():
    pass

@app.post("/auth/reset_pswd")
def reset_pswd():
    pass

@app.post("/auth/check_my_info")
def check_my_info():
    pass