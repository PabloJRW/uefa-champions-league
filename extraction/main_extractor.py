import os
import requests
import subprocess


def run_script(script_name):
    try:
        # Ejecuta el script y espera a que finalice
        subprocess.run(["python", os.path.join("extraction","scripts", script_name)], check=True)
        print(f"'{script_name}' ejecutado con éxito.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar '{script_name}': {e}")


def main():
    scripts = [
        "players.py",
        "players_key_stats.py",
        "players_gols.py",
        "players_attempts.py",
        "players_distribution.py",
        "players_attacking.py",
        "players_defending.py",
        "players_goalkeepers.py",
        "players_disciplinary.py"
    ]
    
    for script in scripts:
        run_script(script)


if __name__ == "__main__":
    main()
