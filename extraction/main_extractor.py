import os
import subprocess
import sys

# Configura el directorio de salida
output_dir = "day6"
raw_data_path = os.path.join('data','raw')

# Lista de scripts que quieres ejecutar
scripts_to_run = [
    "players.py",
    "players_key_stats.py",
    "players_goals.py",
    "players_attempts.py",
    "players_distribution.py",
    "players_attacking.py",
    "players_defending.py",
    "players_goalkeeping.py",
    "players_disciplinary.py"
]

# Crear directorio de salida si no existe
os.makedirs(os.path.join('extraction','data','raw',output_dir), exist_ok=True)

# Función para ejecutar los scripts
def run_script(script_name, output_dir):
    script_path = os.path.join(os.path.dirname(__file__), 'scripts', script_name)
    if os.path.exists(script_path):
        print(f"Running {script_name}...")
        try:
            result = subprocess.run(
                [sys.executable, script_path, output_dir], 
                check=True,
                capture_output=True,
                text=True
            )
            print(f"{script_name} ran successfully.")
            print("Output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error while running {script_name}: {e}")
            print("Error Output:", e.stderr)
        except Exception as e:
            print(f"An unexpected error occurred while running {script_name}: {e}")
    else:
        print(f"{script_name} not found in the specified path.")


for script in scripts_to_run:
    run_script(script, output_dir)
