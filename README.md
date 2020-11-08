# Clean Calendar

Clean Calendar is a simple python script that deletes your old Google Calendar
events.

## Setup

- Clone and enter the repository

    ```bash
    git clone https://github.com/zjrubin/clean_calendar.git
    cd clean_calendar
    ```

- Install the required python packages

    ```bash
    python3 -m pip install -r requirements.txt
    ```

- Enable [the Google Calendar API.](https://developers.google.com/calendar/quickstart/python)

- After enabling the Google Calendar API, save the file `credentials.json` into the repository directory.

- Run the script! ***This will delete all your calendar events 30 or more days in the past from today.***

    ```bash
    python3 clean_calendar.py
    ```

    The sample will attempt to open a new window or tab in your default browser. If this fails, copy the URL from the console and manually open it in your browser.

    If you are not already logged into your Google account, you will be prompted to log in. If you are logged into multiple Google accounts, you will be asked to select one account to use for the authorization.
