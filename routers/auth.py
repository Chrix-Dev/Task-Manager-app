from fastapi import APIRouter, HTTPException
from database import supabase

router = APIRouter

@router.post("/register")
def register(email: str, password: str, name: str):
    response = supabase.auth.sign_up({"email": email, "password": password, })

    if response.user is None:
        raise HTTPException(status_code=400, detail= "Registration failed")
    
    if name:
        supabase.table("Users"). insert({
            "id": response.user.id,
            "name": name,
            "email": email
        }).execute()

    return{
        "user_id": response.user.id,
        "message": "User registered successfully"
    }

@router.post("/login")
def login(email: str , password: str):
    response = supabase.auth.sign_in({"email": email, "password": password})
    if response.user is None:
        raise HTTPException(status_code=400, detail= "Invalid credentials")
    
    return{
        "user_id": response.user.id,
        "access_token": response.session.access_token,
        "token_type": "bearer"
    }