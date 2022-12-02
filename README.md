# Lidless

*A backup tool for devs.*

## Overview

As a developer I want the ability to:

* Backup my files to multiple remote locations using rsync or rclone.
* Exclude git repos (as they are already backed up).
* Include some files from repos (e.g. gitignored config).
* Tell if any repos are not fully backed up (unpushed commits).
* Run a selective backup (I'm in an airport, and know what I've changed).
* Easily rebuild my hard drive from all those sources (the whole point of backups)
* Manage all that from one file.

Lidless is a simple tool that lets you do all that.

## Usage

### Installation

Run the installation script (not working yet)

You will need to create your own aliases, for which I highly recommend turboshell.

### Configuration

Lidless runs from a configuration file written in JSON which you edit manually (for now).

The config object has 3 sections: **targets**, **roots** and **defaults**.

#### Targets

Targets define:

* A backup tool (such as rsync or rclone)
* Options (such as the destination)
* Filters (more on this later)

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

