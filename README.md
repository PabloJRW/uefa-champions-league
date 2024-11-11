# UEFA CHAMPIONS LEAGUE | PLAYERS DATA
 
Welcome to the Champions League Players Data Extraction!.
This project is a comprehensive data extraction initiative focused on gathering and analyzing data about players participating in the UEFA Champions League. The aim is to provide a detailed dataset that can be used for further analysis, visualizations, and reporting. This project highlights skills in web scraping and data processing.

## Table of Contents
1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Contributing](#contributing)
6. [License](#license)

## Introduction
The goal of this project is to extract player performance data from UEFA Champions League. This project aims to provide a comprehensive dataset that can be used for various analyses, including player statistics, performance trends, and team comparisons.

## Installation
To get started with this project, follow these steps:
1. Clone the repository:
```bash
git clone git@github.com:PabloJRW/uefa-champions-league.git
```
2. Navigate to the project directory:
```bash
cd uefa-champions-league
```
3. Install the required dependencies:
``` bash
pip install -r requirements.txt
```

## Usage
1. Run the data extraction script:
``` bash
python extraction\main_extractor.py
```
2. Load the data to MongoDB
```bash
python load\load_to_mongodb.py
```

## Project Structure
``` bash
uefa-champions-league/
├── extraction/                    # Directory for data extraction
│   ├── main_extractor.py          # Script that runs all extraction scripts
│   ├── raw_data/                  # Directory to store raw data extracted from the API
│   └── scripts/                   # Directory containing individual extraction scripts
│       ├── players.py
│       ├── players_attacking.py  
│       ├── players_attempts.py
│       ├── players_defending.py
│       ├── players_disciplinary.py
│       ├── players_distribution.py
│       ├── players_goalkeeping.py
│       ├── players_goals.py
│       ├── players_key_stats.py
│       └── teams_extraction.py
├── load_to_database/              # Directory for data loading
│   └── load_to_mongodb.py         # Script for loading data into MongoDB database
├── tests/                         # Directory for testing scripts
│       ├── test_players.py
│       ├── test_attacking.py  
│       ├── test_attempts.py
│       ├── test_defending.py
│       ├── test_disciplinary.py
│       ├── test_distribution.py
│       ├── test_goalkeeping.py
│       ├── test_goals.py
│       ├── test_key_stats.py
│       └── test_teams_extraction.py
├── requirements.txt               # File listing required Python libraries for the project
└── README.md                      # Project documentation providing an overview and instructions

```

## Contributing
Contributions are welcome! If you would like to contribute to this project, feel free to submit a pull request or open an issue with suggestions for improvement.

## License
This project is licensed under the MIT License. See the LICENSE file for details.



