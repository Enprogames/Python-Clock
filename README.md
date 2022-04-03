# Python-Clock

A school clock written in python with a customizable schedule.
![clock1.JPG](docs//img/clock1.JPG)

## Creating Custom Schedules

Coming soon...

## Future 

- [ ] Create better schedules using JSON instead of CSV files
    ```
    {
        "Default Schedule": {
            "default": "Break", // Leave blank for no text to show up between events
            "events": {
                "Before School": ["0:00", "8:55"],
                "A Block": ["8:55", "10:20"],
                "B Block": ["10:30", "11:45"],
                "C Block": [],
                "D Block": [],
                "School Over": []
            }
        }
    }
    ```

- [ ] Create admin dashboard
    - [ ] CRUDL menu for schedule
    - [ ] Fully customizable color scheme

- [ ] Use pack() layout manager instead of place() for better handling of different display sizes

## License

Copyright 2022 Ethan Posner

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
