
# Save tithi for reuse

- Currently `tithi.notify_today()` fetches the current tithi and sends a notification
- It should save the current tithi in `today.json` file
- `today.json` should contain the following keys:
    - `tithi`:
    - `till`:
- `tithi.notify_today()` should first open the `today.json` file and check if the current date time is still before the `till` date.
- If it is, then it should just use the `tithi` value from the json instead of fetching again with an API request.
- If the current time has passed the date time mentioned in the value of the `till` key in `today.json`, it should make an API request and fetch the latest `tithi` from the API. Then it should update the `tithi` and `till` values in `today.json` and overwrite it.




# Refactor subscriptions out of `tithi.py`

- Restrict all changes to `/src/lib`. DO NOT change anything in the `src/api` or `src/cli`
- `lib/subscriptions.json` should have a `tithi` key. Its value should be a list of subscription objects. The `subscription` defined in `tithi.py` should be moved under the `tithi` key in `subscriptions.json`
- `notify.py` should have another `push(key, message)` which sends `message` to all subscriptions listed in `subscriptions.json` under `key`.
- `tithi.py` should just call `notify.push('tithi', message)`
- If `subscriptions.json` does not exist when `notify.py` tries to access it, the file should be created with `{}`



# Save subscription in `lib/subscriptions.json`

- Rename the `key` parameter in `notify.push()` to `thread`. The keys in the `subscriptions.json` will be called threads.
- Change API route `POST /subscribe` to `POST /subscriptions/<thread>/`. `<thread>` could be any string value. For now only `tithi` is a supported value. Any other value should return a 404.
- The API should not attempt to save to `subscriptions.json` on its own. It should rather use the `lib/notify` module as follows.
- A new `subscribe(thread, subscription)` should be added to `notify.py` which appends the `subscription` to the value of `thread` key in `subscriptions.json`.
- The `subscription` details sent in the POST body should be appended to the `<thread>` key in `lib/subscriptions.json` using `notify.subscribe(thread, subscription)`
- `notify.subscribe()` should ensure not to add duplicate subscriptions to any `<thread>` in `subscriptions.json`. A subscription can be uniquely identified by its `.endpoint`. So, `notify.subscribe()` has to ensure that another subscription with the same `.endpoint` doesn't already exist for the same `<thread>` before adding it to the `subscriptions.json`
- Update `index.html` to POST to `/subscriptions/tithi/` instead of `/subscribe`. Change the button title to `Subscribe to Tithi`