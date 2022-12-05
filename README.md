# Lidless

*A backup tool for devs.*

## Overview

Lidless helps you create a personal backup strategy using rsync, rclone, git and other tools.

It exists because even with those tools, backups are difficult:

* We want to exclude directories
* 

As a developer I want the ability to:

* Backup my data to multiple remote locations using rsync or rclone.
* Exclude directories which are git repos as they are already backed up.
* Include some files from repos (e.g. gitignored config).
* Be told if I am about to backup files I don't want to backup.
* Tell if any repos are not fully backed up (unpushed commits).
* Run a selective backup (I'm in an airport, and know what I've changed).
* Easily rebuild my hard drive from all those sources (the whole point of backups)
* Manage all the above easily and centrally.

Lidless is a very simple CLI tool which does all this.

## Installation

Lidless only works on Linux/MacOS (Windows support is easy enough to add) and requires Python 3.6 or above.

#### Running Lidless

To run lidless just clone or download the repo and execute the **run.sh** inside it:

```bash
git clone git@github.com:slickworks/lidless.git
./lidless/run.sh
```

If you have Python 3.6 or above you don't need to do anything else. 

#### Python versions

If you don't have Python3, go ahead and install the latest version. If your OS comes Python3 which is older than 3.6 then you need to install a more recent version alongside it (never change your system Python) and I recommend using [pyenv](https://github.com/pyenv/pyenv) for that. Once you have installed a new Python version using pyenv, get the permanent path to it like so:

```bash
$ pyenv shell 3.10.4
$ pyenv which python
/home/me/.pyenv/versions/3.10.4/bin/python
```

The point the env var `LIDLESS_PYTHON` to it:

```bash
export LIDLESS_PYTHON=/home/andrew/.pyenv/versions/3.10.4/bin/python
```

This ensures lidless always runs using that exact version, regardless of any active virtual environment or system Python versions.

#### Aliases

You will most likely want to create an alias:

```bash
alias lidless="/path/to/lidless/run.sh"
```

You may also want aliases for the common permutations of arguments you will run, e.g:

```bash
alias backup-mega="lidless backup mega"
```

I highly recommend Turboshell for that.

#### User directory

By default lidless will save its config and cache files in a directory at **~/lidless** but you can change this with the `LIDLESS_USER_DIR`  environment variable:

```bash
export LIDLESS_USER_DIR=/some/other/directory
```

#### Summary

You will likely end up with something like this in your **~/.bashrc** or **~/.zshrc** file:

```bash
export LIDLESS_USER_DIR=/some/other/directory
export LIDLESS_PYTHON=/home/andrew/.pyenv/versions/3.10.4/bin/python
alias lidless="/path/to/lidless/run.sh"
alias backup="lidless backup mega"
```

Alternatively, put all this in a separate file (e.g. **~/lidless-config.sh**) and source that in your **~/.bashrc** or **~/.zshrc** file:

```bash
. ~/lidless-config.sh
```

Remember that changes to  **~/.bashrc** or **~/.zshrc** only affect new shell sessions. To load the changes in an open shell session you need to source the file:

```bash
source ~/.bashrc
```

## Usage

### Configuration

Lidless runs from an JSON file located at **~/lidless/config.json** (unless you specified otherwise) which looks like this:

```json
{
    "roots": {
        "/home/me": {...},
        "/projects/acme": {...}
    },
    "targets": {
        "mega": {...},
        "google-drive": {...}
    }
}
```

The **roots** define points in your filesystem you want to backup. The **targets** define backup strategies (where, what and how). For now you must edit this file manually.

#### Targets

Each target defines:

* A backup tool (such as rsync or rclone)
* A set of labels (to specify which nodes to include)
* Optional additional parameters

Here for example we define two targets. One for an external hard drive, another for [mega](https://mega.nz/) (a cloud storage provider):

```json
{
  "targets": {
    "my-hdd": {
      "tool": "rsync",
      "dest": "/mnt/ext-hd2"
    },
    "mega": {
      "tool": "rclone",
      "provider": "mega"
    }
  }
}
```

You can create as many of these as you like, each with different permutations.

#### Roots

Each top level entry in roots specifies a directory you wish to backup. For example:

```json
{
  "roots": {
    "/projects": {},
    "/home/andrew": {}
  }
}
```

These are treated as *absolute* paths and must start with **/** (anything else gets ignored).

If you have multiple top level entries, you must specify the destination on the remote:

```json
{
  "roots": {
    "/projects": {
      "dest": "projects",
    },
    "/home/andrew": {
      "dest": "home",
    }
  }
}
```

> Destinations must be unique (you'll be warned if they are not) as syncing two different sources to the same destination will result in one overwriting the other.

You can nest paths within other paths:

```json
{
  "roots": {
    "/projects": {
      "dest": "projects",
       "/project-1/code": {}
    }
  }
}
```

Here's what you need to know about nested paths:

1. They must start with **/** but are treated as relative to their enclosing path.
2. They are also excluded from the parent path's backup. 
3. They inherit the destination.

So the last example translates to these instructions:

```
backup /projects >> remote:projects --exclude /project-1/code
backup /project-1/code >> remote:projects/project-1/code
```

This example acheives nothing other than issuing two commands instead of one, the result of which would be identical. 

The point of nested paths is to override parent settings, most commonly: **tags**.

#### tags

You can add tags to paths, which lets you control which directories are included for which targets. Fex example:

```json
{
  "roots": {
    "/projects": {
      "tags": ["cloud"],
      "dest": "projects",
    },
    "/home/andrew": {
      "tags": ["cloud", "personal"],
      "dest": "home",
    }
  }
}
```

You can then tell targets which tags to include:

```json
{
  "targets": {
    "my-hdd": {
      "tool": "rsync",
      "dest": "/mnt/ext-hd2",
      "tags": ["personal"]
    },
    "mega": {
      "tool": "rclone",
      "provider": "mega",
      "tags": ["cloud"]
    }
  }
}
```

The target `mega` will include **/projects** and **/home/andrew** but the target `my-hdd` will only include **/home/andrew**.

Note that tags are not inherited by nested directories. The rationale being that the primary reason for creating a nested directory is to change tags.

If a target does not specify tags, it will include all directories in roots, so be careful. It is usually safer to set default label in settings, which is applied to all directories which do not specify tags:

```json
{
  "defaults": {
    "tags": ["cloud"]
  },
  "targets": {
    "mega": {
      "tool": "rclone",
      "provider": "mega",
      "tags": ["cloud"]
    }
  }
}
```

#### Putting it all together

Let's look at how default tags and nested directories interact to allow us to exclude a git repository from our backups, but include a nested directory inside it:

```json
{
  "roots": {
    "/projects": {
      "dest": "projects",
        "/project-1/code": {
          "tags": ["git"],
          "/settings": {}
        }
      }
    }
  }
}
```

This would result in the following logic:

| dir                      | tags  | dest                             |
| ------------------------ | ----- | -------------------------------- |
| /projects                | cloud | projects                         |
| /project-1/code          | git   | N/A                              |
| /project-1/code/settings | cloud | projects/project-1/code/settings |

Meaning that a target with tags "cloud" will ignore **/project-1/code** include **projects/project-1/code/settings**.

When restoring, the repo will be excluded and untouched, so if you restore the repository from git first then your files will be unaffected. Restoring from git without affecting **settings** is a bit more tricky.

#### Exclude

There are two ways to exclude files or directories in rsync/rclone:

1. Listed individually
2. From a file

A couple of points to remember with lidless:

* Each node gets its own command
* Nested node paths are automatically excluded.

You can add exclude patterns like so:

```json
{
  "roots": {
    "/projects": {
      "dest": "projects",
      "exclude": ["*.pyc"]
    }
  }
}
```

You can also set an exclude_from in defaults, in a target, or a node.

```
{
  "defaults": {
    "exclude_from": "path/to/file1"
  },
  "targets": {
    "mega": {
      "tool": "rclone",
      "provider": "mega",
      "tags": ["cloud"],
      "exclude_from": "path/to/file2"
    }
  },
  "roots": {
    "/projects": {
      "dest": "projects",
      "exclude_from": "path/to/file3"
    }
  }
}
```

The closest one will be used. You can use exclude_from and exclude together.

## Commands

### Target Commands

The two commands you can run on targets are `backup` and `restore`:

```
python -m lidless backup <target> [--no-prompt] [--diff-only] [--print-cmds]
python -m lidless restore <target> [--no-prompt] [--diff-only] [--print-cmds]
```

Both of these commands have the same options. With no options the behaviour is to show a summary of the changes and asks you whether to continue.

Note that the commands themselves are implemented by the backup tool specified in the target (e.g. **rsync**, **git**) and these may not implement all options. However the general structure is as follows:

##### No prompt

The `--no-promp` option skips the prompt and proceeds directly with the backup.

```
python -m lidless backup <target> --no-prompt
```

##### Diff only

The `--diff-only` option shows the changes.  This option disables the prompt, so `--no-prompt` has no effect if included.

```
python -m lidless backup <target> --diff-only
```

##### Just print the commands

The `--print-cmds` will print the runnable commands so you can inspect or run them. 

```
python -m lidless backup <target> --print-cmds
```

This option disables the prompt, so `--no-prompt` has no effect if included. If used in combination with `--diff` it will print the commands used to produce the diff.

Bear in mind that tools (including **rsync** and **rclone**) apply additional formatting to the diff returned by those commands, so running the printed commands independently will not produce the same output.

### Path commands

These commands update options in the config file for the current working directory. To be defined.

### Config commands

These commands work with other aspects of the config. To be defined.


## Development

Run tests with:

```bash
pytest
```

Run files through black and flake8.

