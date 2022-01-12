import datetime
import os
import subprocess

from invoke import run as local
from invoke.tasks import task

# Process .env file
if os.path.exists(".env"):
    with open(".env", "r") as f:
        for line in f.readlines():
            if not line or line.startswith("#") or "=" not in line:
                continue
            var, value = line.strip().split("=", 1)
            os.environ.setdefault(var, value)


LOCAL_DATABASE_NAME = os.getenv("DATABASE_NAME")
LOCAL_DATABASE_USERNAME = os.getenv("DATABASE_USER")

PLATFORM_PROJECT_ID = "rasrzs7pi6sd4"
PRODUCTION_APP_INSTANCE = "main"
STAGING_APP_INSTANCE = "demo"

LOCAL_DB_DUMP_DIR = "database_dumps"

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def container_exec(cmd, container_name="web"):
    return subprocess.run(["docker-compose", "exec", "-T", container_name, "bash", "-c", cmd])


def db_exec(cmd):
    "Execute something in the 'db' Docker container."
    return container_exec(cmd, "db")


def web_exec(cmd):
    "Execute something in the 'web' Docker container."
    return container_exec(cmd, "web")


def cli_exec(cmd):
    return container_exec(cmd, "cli")


@task
def run_management_command(c, cmd):
    """
    Run a Django management command in the 'web' Docker container
    with access to Django and other Python dependencies.
    """
    return container_exec(f"poetry run ./manage.py {cmd}", "web")


# -----------------------------------------------------------------------------
# Container management
# -----------------------------------------------------------------------------


@task
def build(c):
    """
    Build (or rebuild) local development containers.
    """
    local("docker-compose build")


@task
def start(c, container_name=None):
    """
    Start the local development environment.
    """
    cmd = "docker-compose up -d"
    if container_name:
        cmd += f" {container_name}"
    local(cmd)


@task
def stop(c, container_name=None):
    """
    Stop the local development environment.
    """
    cmd = "docker-compose stop"
    if container_name:
        cmd += f" {container_name}"
    local(cmd)


@task
def restart(c):
    """
    Restart the local development environment.
    """
    start(c)
    stop(c)


@task
def sh(c):
    """
    Run bash in a local container (with access to dependencies)
    """
    subprocess.run(["docker-compose", "exec", "web", "poetry", "run", "bash"])


@task
def test(c):
    """
    Run python tests in the web container
    """
    subprocess.call(
        [
            "docker-compose",
            "exec",
            "web",
            "poetry",
            "run",
            "./manage.py",
            "test",
            "--parallel",
        ]
    )


# -----------------------------------------------------------------------------
# Database operations
# -----------------------------------------------------------------------------


@task
def psql(c, command=None):
    """
    Connect to the local postgres DB using psql
    """
    cmd_list = [
        "docker-compose",
        "exec",
        "db",
        "psql",
        *["-d", LOCAL_DATABASE_NAME],
        *["-U", LOCAL_DATABASE_USERNAME],
    ]
    if command:
        cmd_list.extend(["-c", command])

    subprocess.run(cmd_list)


def delete_local_renditions(c):
    psql(c, "TRUNCATE wagtailimages_rendition;")


def delete_db(c):
    db_exec(
        f"dropdb --if-exists --host db --username={LOCAL_DATABASE_USERNAME} {LOCAL_DATABASE_NAME}"
    )
    db_exec(
        f"createdb --host db --username={LOCAL_DATABASE_USERNAME} {LOCAL_DATABASE_NAME}"
    )


@task
def dump_db(c, filename):
    """Snapshot the database, files will be stored in the db container"""
    if not filename.endswith(".psql"):
        filename += ".psql"
    db_exec(
        f"pg_dump -d {LOCAL_DATABASE_NAME} -U {LOCAL_DATABASE_USERNAME} > {filename}"
    )
    print(f"Database dumped to: {filename}")


@task
def restore_db(c, filename, delete_dump_after=False):
    """Restore the database from a snapshot in the db container"""
    print("Stopping 'web' to sever DB connection")
    stop(c, "web")
    if not filename.endswith(".psql"):
        filename += ".psql"
    delete_db(c)
    db_exec(f"psql -d {LOCAL_DATABASE_NAME} -U {LOCAL_DATABASE_USERNAME} < {filename}")
    print(f"Database restored from: {filename}")
    if delete_dump_after:
        db_exec(f"rm {filename}")
    start(c, "web")


# -----------------------------------------------------------------------------
# Pull from Production
# -----------------------------------------------------------------------------


@task
def pull_production_data(c):
    """Pull database from the production platform.sh env"""
    pull_database_from_platform(c, PRODUCTION_APP_INSTANCE)


@task
def pull_production_media(c):
    """Pull all media from the production platform.sh env"""
    pull_media_from_platform(c, PRODUCTION_APP_INSTANCE)


# -----------------------------------------------------------------------------
# Pull from Staging
# -----------------------------------------------------------------------------


@task
def pull_staging_data(c):
    """Pull database from the staging platform.sh env"""
    pull_database_from_platform(c, STAGING_APP_INSTANCE)


@task
def pull_staging_media(c):
    """Pull all media from the staging platform.sh env"""
    pull_media_from_platform(c, STAGING_APP_INSTANCE)


# -----------------------------------------------------------------------------
# Platform.sh helpers
# -----------------------------------------------------------------------------


def pull_database_from_platform(c, environment_name):
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    print("Fetching data from platform.sh")
    start(c, "cli")
    cli_exec(
        f"platform db:dump -e {environment_name} -p {PLATFORM_PROJECT_ID} -f {timestamp}.psql -d {LOCAL_DB_DUMP_DIR}"
    )

    print("Stopping 'web' to sever DB connection")
    stop(c, "web")

    print("Replacing local database with downloaded version")
    start(c, "db")
    delete_db(c)
    restore_db(c, f"app/{LOCAL_DB_DUMP_DIR}/{timestamp}.psql", delete_dump_after=True)

    print("Applying migrations from local environment")
    run_management_command(c, "migrate")

    print("Anonymising downloaded data")
    run_management_command(c, "run_birdbath")

    print("Database updated successfully")
    print(
        "NOTE: Any Django users you were using before will no longer exist. "
        "You may want to run `python manage.py createsuperuser` from a container "
        "shell to create yourself a new one."
    )


def pull_media_from_platform(
    c,
    environment_name,
):
    """
    Copies the entire 'media' folder from a platform.sh environment
    to a local one (including original image, documents, videos, and audio),
    but excluding thumnails generated by Wagtail.
    """
    cli_exec(
        f"platform mount:download -e {environment_name} -p {PLATFORM_PROJECT_ID} -m media "
        "--target=media --exclude='/images/*' --yes"
    )
    delete_local_renditions(c)
