import matplotlib
matplotlib.use("Agg")  # Use a non-GUI backend
import matplotlib.pyplot as plt
import io
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def password_hashing(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)

def create_plot(timestamps: list, temperatures: list):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(timestamps, temperatures, marker="o", linestyle="-", color="b", label="Temperature")
    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Temperature Readings")
    ax.tick_params(axis='x',rotation=15)
    ax.legend()
    ax.grid(True)

    img = io.BytesIO()
    fig.savefig(img, format="png")
    plt.close(fig)
    img.seek(0)

    return img