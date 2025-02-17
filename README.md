# Modular-Save-Parser-For-Collectibles

Don't you hate it when you're missing 2 of 100 collectibles in a 5 hours game, but have no way to know which ones ?
I sure do.

Heck, the game know which items I'm missing, why can't it tell me ?
Why isn't there a tool that can parse the save files and display the list of missed collectibles ?

Well, some exist : I've seen a few of them, but not that much. And all of them were separate projects.

I aim to create a modular program, flexible enough to allow devs to cover more games in the future.

## Supported games

| Game name | App name   | Comment                                                                                   |
|-----------|------------|-------------------------------------------------------------------------------------------|
| Alan Wake | `alanwake` | Retrieve the list of in-game collectible ID, which are already ordered for the most part. |

Once again, this program is made to support more than one game, don't hesitate to make a pull request.

## How to use

Clone the project, by downloading
[the archive](https://github.com/fsabre/modular-save-parser-for-collectibles/archive/refs/heads/master.zip)
or by cloning the project

```bash
git clone https://github.com/fsabre/modular-save-parser-for-collectibles.git
```

Run the program

```bash
python -m src APP_NAME
```

You may want to change constants in the `src/constants.py` file if the program doesn't work properly.

## Roadmap

This project is not actively maintained. I will update it if I need its framework for another game.

Nevertheless, here's a list of possible improvements:

- Add support for more games
- Make it friendlier to edit constants such as paths
