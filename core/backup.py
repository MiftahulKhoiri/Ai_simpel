import shutil
from datetime import datetime
from pathlib import Path

from core.logger import get_logger

log = get_logger("AI_BACKUP")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "qa.json"
BACKUP_DIR = BASE_DIR / "backups"


def backup_qa_once():
    """
    Backup qa.json sebelum diubah.
    - Hanya menyimpan 1 file backup
    - Nama file mengandung timestamp
    """
    if not DATA_PATH.exists():
        log.warning("qa.json belum ada, skip backup")
        return

    BACKUP_DIR.mkdir(exist_ok=True)

    # Hapus backup lama
    for f in BACKUP_DIR.glob("qa_backup_*.json"):
        f.unlink()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    backup_file = BACKUP_DIR / f"qa_backup_{timestamp}.json"

    shutil.copy2(DATA_PATH, backup_file)
    log.info(f"Backup dibuat: {backup_file.name}")