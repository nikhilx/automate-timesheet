# Zoho Time Logger

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Copy `config.sample.ini` to `config.ini`:
   ```
   cp config.sample.ini config.ini
   ```
4. Edit `config.ini` with your actual Zoho API credentials and preferences
5. Set up your `.env` file with any additional environment variables

## Usage

Run the application using one of these commands:

- Use configuration from config.ini: `python main.py`
- Use weekly preset: `python main.py --preset weekly`
- Use monthly preset: `python main.py --preset monthly`

## Configuration

- `config.ini`: Contains your Zoho API credentials and time logging preferences

Note: `config.ini` is ignored by git to keep your credentials safe. Always use `config.sample.ini` as a template and create your own `config.ini` file locally.# automate-timesheet