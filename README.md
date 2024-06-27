[trick-gxds-sql-tables-url]: https://github.com/Evvvai/trick-surf-compose
[trick-surf-api-url]: https://api.trick.surf

# Trick Surf Data Dump
## About
This project contains database dumps of [TrickGxds' SQL tables][trick-gxds-sql-tables-url]
that were published in the late of 2022 and data retrieved from [TrickSurf API][trick-surf-api-url].
There are several types of data you can find — TrickGxds' raw SQL dumps of database,
TrickGxds' SQL dumps of database converted to JSON files w/ friendly column names,
TrickGxds' JSON dumps of tricks for their \`surf_ski_2\` CS:GO map, which is also present in CS:S recently,
those \`surf_ski_2\` tricks were presented in two formats — original & sifted.
The original version contains original trick, player, and trigger names.
The sifted version contains only tricks that could be added to the CS:S version of TrickGxds' \`surf_ski_2\` map,
also title cased trick names, fixed player names, and mapped trigger names to those used on CS:S TrickSurf.


## Structure & Data Paths
### TrickGxds' Database Raw Data
+ `/trick-gxds/<players|routes|tricks|triggers><.json|.min.json|.sql>`

### TrickGxds' Database Unified Data
+ `/unified/ski2-gxds-tricks~<original|sifted><.json|.min.json>`

### TrickSurf's API Raw Data
+ `/trick-surf/<events|games|maps|players|servers><.json|.min.json>`
+ `/trick-surf/events/<event-id><.json|.min.json>`
+ `/trick-surf/games/<game-id><.json|.min.json>`
+ `/trick-surf/games/<game-id>/maps/<map-id>/tricks<.json|.min.json>`
+ `/trick-surf/games/<game-id>/maps/<map-id>/tricks/<trick-id><.json|.min.json>`
+ `/trick-surf/maps/<map-id><.json|.min.json>`
+ `/trick-surf/maps/<map-id>/<triggers|teleports><.json|.min.json>`
+ `/trick-surf/maps/<map-id>/triggers/<trigger-id><.json|.min.json>`
+ `/trick-surf/maps/<map-id>/teleports/<teleport-id><.json|.min.json>`
+ `/trick-surf/players/<player-id><.json|.min.json>`
+ `/trick-surf/servers/<server-id><.json|.min.json>`


## Running Update Script
### About
The script is located in the [/src/](./src) directory & named [main.py](./src/main.py).
The script supports several flags that you can pass to it — `--license`, `--dump-trick-gxds`,
`--dump-trick-surf`, `--unified-points-system`, `--unified-title-names`. 
To gather more information & make yourself familiar w/ the utility,
execute the [main.py](./src/main.py) file w/ `--help` flag attached.
```text
usage: main.py [-h] [-l] [--dump-trick-gxds] [--dump-trick-surf] [--unified-points-system {old,new}]
               [--unified-title-names]

optional arguments:
  -h, --help            show this help message and exit
  -l, --license         show the project license and exit
  --dump-trick-gxds     dump trick gxds data to json files
  --dump-trick-surf     dump trick surf data to json files
  --unified-points-system {old,new}
                        type of points system to use for unified~sifted data dump
  --unified-title-names
                        convert trick names to title case for unified~sifted data dump
```
The update script depends on two python packages that you can install using \`pip\`.
Run `pip install -r requirements.txt` in the root of this project and it will recursively install
all needed packages to run the [main.py](./src/main.py) file.

### Dumping TrickGxds' Data
Run `python src/main.py --dump-trick-gxds --unified-points-system=old --unified-title-names` and
it will dump everything it can to the [/trick-gxds/](./trick-gxds) & [/unified/](./unified) directories.

```text
SUCCESS :: TrickGxds :: Created & wrote data dumps to JSON files
```

### Dumping TrickSurf's Data
Run `python src/main.py --dump-trick-surf` and it will dump everything it can to the [/trick-surf/](./trick-surf) directory.
Be careful, dumping TrickSurf's API is an expensive operation, don't panic if it takes a long period of time, just wait
or interrupt execution using <kbd>CTRL</kbd>+<kbd>C</kbd>.
```text
SUCCESS :: TrickSurf :: Created & wrote data dumps to JSON files
```


## Setting Development Environment
Follow this [documentation](https://docs.python.org/3/library/venv.html) to
setup a virtual python environment. Then active the environment you just set-up
and install required packages using the [requirements.txt](./requirements.txt) file placed in the root of this project.
Be sure that you use Python 3.9.


## License
Licensed under the [GPL-3.0 license](./COPYING).
