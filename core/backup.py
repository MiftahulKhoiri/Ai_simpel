import shutil
from datetime import datetime
from pathlib import Path

from core.logger import get_logger

log = get_logger("AI_BACKUP")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "qa.json"
BACKUP_DIR = BASE_DIR / "backups"


def backup_qa():
    """
    Backup qa.json dengan timestamp.
    Dipanggil SETIAP KALI sebelum qa.json ditulis ulang.
    """
    if not DATA_PATH.exists():
        log.warning("qa.json belum ada, skip backup")
        return

    BACKUP_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = BACKUP_DIR / f"qa_{timestamp}.json"

    shutil.copy2(DATA_PATH, backup_file)
    log.info(f"Backup qa.json dibuat: {backup_file.name}")