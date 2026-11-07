from data.loader import build_demo_service
from ui.admin_cli import AdminCLI


if __name__ == "__main__":
    AdminCLI(build_demo_service()).run()
