import requests
import streamlit as st
from app.config import API_URL

def call(method, path, **kwargs):
    try:
        response = requests.request(method, f"{API_URL}{path}", timeout=12, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        message = str(exc)
        if getattr(exc, "response", None) is not None:
            try:
                message = exc.response.json().get("detail", message)
            except ValueError:
                pass
        st.error(f"Could not reach the backend: {message}")
        return None

def get(path, **kwargs):
    return call("GET", path, **kwargs)

def post(path, **kwargs):
    return call("POST", path, **kwargs)
