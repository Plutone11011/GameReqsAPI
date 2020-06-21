# GameReqs API

## Overview
GameReqs API provides endpoints to gain informations about games' system requirements. Data is scraped from Steam store(might add other sources in the future).

## URI and versioning
Every endpoint is prefixed with http://*domain*/api/v1/. The API is currently in its first iteration.

# Resources

## Games
You can find information about games' system requirements from `/games`. You can also create, update and delete games resources. Every resource has the following properties:

Field | Description
------|------------
id    | The resource unique id
name  | The game's name
description | The game's description
developer | The game's developer team
ram_min | Minimum RAM required to play the game
ram_rec | Recommended RAM required to play the game
storage_min | Minimum storage required to play the game
storage_rec | Recommended storage required to play the game
cpu_min | Minimum cpu required to play the game
cpu_rec | Recommended cpu required to play the game
gpu_min | Minimum gpu required to play the game
gpu_rec | Recommended gpu required to play the game
OS_min | Minimum OS version required to play the game
OS_rec | Recommended OS version required to play the game

### Games request
Making a request to `/games` with no parameters returns a list of every resource.

#### Query parameters

* **name**: search by game's name (*optional*)
* **page**: a url-encoded JSON object that allows pagination of results. Ignored if used with name search. Needs two properties:
    * **limit**: maximum number of returned results
    * **last_id**: indicates that the next page will yield games from *last_id+1* onward
* **filter**: a url-encoded array of JSON objects that allows filtering over RAM and storage. Can be combined with pagination. Every object needs 3 properties:
    * **op**: a comparison operator string (eq, neq, gt, ge, le, lt)
    * **memory**: the name of the property (storage or ram)
    * **value**: value that need to be filtered

### Games response object

```
[
    {
        "id": 1,
        "info": {
          "description": "Legends of Persia is a highly ambitious Action RPG Adventure...",
          "developer": "Sourena Game Studio",
          "name": "Legends of Persia"
        },
        "minimum_requirements": {
          "OS_min": " Windows XP, Vista, 7 and 8",
          "cpu_min": " AMD 3500+ – Intel 2.2 Pentium 4 CPU",
          "gpu_min": " Geforce7000 series – ATI X1400 & HD series or greater",
          "ram_min": 1,
          "storage_min": 3.5
        },
        "recommended_requirements": {
          "OS_rec": null,
          "cpu_rec": null,
          "gpu_rec": null,
          "ram_rec": null,
          "storage_rec": null
        }
  }
]
```

### Info
This resource yields a subset of informations of the game resource. The endpoint is `/games/info`
In particular, it returns only the `info` object of the games response object. As such, it accepts the same parameters as the **Games** resource.

### Minimum requirements
This resource yields a subset of informations of the game resource. The endpoint is `/games/minimum_requirements`
In particular, it returns only the `minimum_requirements` object of the games response object. As such, it accepts the same parameters as the **Games** resource.

### Recommended requirements
This resource yields a subset of informations of the game resource. The endpoint is `/games/recommended_requirements`
In particular, it returns only the `recommended_requirements` object of the games response object. As such, it accepts the same parameters as the **Games** resource.

## Contributing
Contributions are encouraged. Please refer to CONTRIBUTING.md