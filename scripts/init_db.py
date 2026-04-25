from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.db import engine
from src.models import Base


def main():
    Base.metadata.create_all(bind=engine)
    print("DB initialized")


if __name__ == "__main__":
    main()
