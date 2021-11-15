# musology

To initialise the game (more than just a temporary solution - a really temporary s0lution)
```
from game_test import main
main()
```

Click around in the admin and see what was created!

We don't have any venues yet..

Create a superuser..
```
./manage.py createsuperuser
```

Please post data to /take_turn (this endpoint currently doesn't do anything) in this format:
```
  <!-- Payload example -->
  {
    "locations": [
      {
        "id": 1,
        "events": [
          {
            "slot": 1,
            "kind": "gig",  # taken from 'type' on a location's event_options
            "band_ids": [1],
            "promoter_ids": [],
            "people_ids": [], # Excludes band musicians, but add this in the backend for bonuses or whatever
          },
          {
            "slot": 2,
            "kind": "", # Leave all fields empty for nothing to occur in this slot
            "band_ids": [],
            "promoter_ids": [],
            "people_ids": [],
          },
          {
            "slot": 3,
            "kind": "gig",
            "band_ids": [2],
            "promoter_ids": [],
            "people_ids": [],
          },
          {
            "slot": 4,
            "kind": "deep clean upgrade",
            "band_ids": [],
            "promoter_ids": [],
            "people_ids": [5], # Bar staff can do cleaning and upgrade work
          },
        ],
        "updates": {
          "entry_price": 12, # Set the new value, overriding whatever is in there
          "name": "Swiss Cheese Cafeeeeé"
        }
      },
      {
        "id": 2,
        "events": [
              {
                "slot": 1,
                "kind": "training",  # EVENT_TYPE
                "band_ids": [1],
                "promoter_ids": [],
                "people_ids": [15, 16, 17, 18], # Excludes band musicians, but add this in the backend for bonuses or whatever
              },
              {
                "slot": 2,
                "kind": "training", # Leave all fields empty for nothing to occur in this slot
                "band_ids": [],
                "promoter_ids": [],
                "people_ids": [15, 16, 17, 18],
              },
              {
                "slot": 3,
                "kind": "training",
                "band_ids": [2],
                "promoter_ids": [],
                "people_ids": [15, 16, 17, 18],
              },
              {
                "slot": 4,
                "kind": "deep clean upgrade",
                "band_ids": [],
                "promoter_ids": [],
                "people_ids": [15, 16, 17, 18], # Bar staff can do cleaning and upgrade work
          },
        ],
      }
    ]
  }
  ```

# Reset from game_test and create new fixtures
alias musreset='rm -f db.sqlite3 && python manage.py migrate && python manage.py resetgame && python manage.py dumpdata > fixtures/level1.json
# Fresh load from fixtures
alias musload='rm -f db.sqlite3 && python manage.py migrate && python manage.py loaddata fixtures/level1.json'
# Resets and creates fixtures, then tests them by dropping DB and loading them
alias musreload='musreset && musload'
