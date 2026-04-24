BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "tasks.json"
APP_OWNER = "Sobhi"

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key"


@app.context_processor
def inject_app_owner() -> dict[str, str]:
    return {"app_owner": APP_OWNER}


def load_tasks() -> list[dict[str, Any]]:
    if not DATA_FILE.exists():
        return []
