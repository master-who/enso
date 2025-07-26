
# Save tithi for reuse

- Currently `tithi.notify_today()` fetches the current tithi and sends a notification
- It should save the current tithi in `today.json` file
- `today.json` should contain the following keys:
    - `tithi`:
    - `till`:
- `tithi.notify_today()` should first open the `today.json` file and check if the current date time is still before the `till` date.
- If it is, then it should just use the `tithi` value from the json instead of fetching again with an API request.
- If the current time has passed the date time mentioned in the value of the `till` key in `today.json`, it should make an API request and fetch the latest `tithi` from the API. Then it should update the `tithi` and `till` values in `today.json` and overwrite it.

