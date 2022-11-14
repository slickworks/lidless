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

Run the installation script. 

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

The point of nested paths is to override parent settings, most commonly: **labels**.

#### Labels

You can add labels to paths, which lets you control which directories are included for which targets. Fex example:

```json
{
  "roots": {
    "/projects": {
      "labels": ["cloud"],
      "dest": "projects",
    },
    "/home/andrew": {
      "labels": ["cloud", "personal"],
      "dest": "home",
    }
  }
}
```

You can then tell targets which labels to include:

```json
{
  "targets": {
    "my-hdd": {
      "tool": "rsync",
      "dest": "/mnt/ext-hd2",
      "labels": ["personal"]
    },
    "mega": {
      "tool": "rclone",
      "provider": "mega",
      "labels": ["cloud"]
    }
  }
}
```

The target `mega` will include **/projects** and **/home/andrew** but the target `my-hdd` will only include **/home/andrew**.

Note that labels are not inherited by nested directories. The rationale being that the primary reason for creating a nested directory is to change labels.

If a target does not specify labels, it will include all directories in roots, so be careful. It is usually safer to set default label in settings, which is applied to all directories which do not specify labels:

```json
{
  "defaults": {
    "labels": ["cloud"]
  },
  "targets": {
    "mega": {
      "tool": "rclone",
      "provider": "mega",
      "labels": ["cloud"]
    }
  }
}
```

#### Putting it all together

Let's look at how default labels and nested directories interact to allow us to exclude a git repository from our backups, but include a nested directory inside it:

```json
{
  "roots": {
    "/projects": {
      "dest": "projects",
        "/project-1/code": {
          "labels": ["git"],
          "/settings": {}
        }
      }
    }
  }
}
```

This would result in the following logic:

| dir                      | labels | dest                             |
| ------------------------ | ------ | -------------------------------- |
| /projects                | cloud  | projects                         |
| /project-1/code          | git    | N/A                              |
| /project-1/code/settings | cloud  | projects/project-1/code/settings |

Meaning that a target with labels "cloud" will ignore **/project-1/code** include **projects/project-1/code/settings**.

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
        "exclude": [
        	"tmp"
        ]
      }
    }
  }
}
```

You can also set a default exclude_from. 

```
{
  "defaults": {
    "exclude_from": "/path/to/file1"
  },
  "targets": {
    "mega": {
      "tool": "rclone",
      "provider": "mega",
      "labels": ["cloud"],
      "exclude_from": "/path/to/file2"
    }
  }
}
```





### Commands

* print/show labels
* backup
* restore
* check



```json
{
  "roots": {
    "/projects": {
        "dest": "projects",
        "label": "files",
        "/project-1/code": {
            "label": "git",
            "/settings": {
                "label": "files",
            },
            "/db.sqlite3": {
                 "label": "files",
            }
        }
    }
  },
  "settings": {
    "default_tags": ["dir"]
  },
  "targets": {
    "ext": {
      "tool": "rsync",
      "dest": "/other/tmp"
    }
  }
}
```

Tga

```json
{
  "roots": {
    "a": {}
  },
  "settings": {
    "default_tags": ["dir"]
  },
  "targets": {
    "ext": {
      "tool": "rsync",
      "dest": "/other/tmp"
    }
  }
}
```






1. Set up a remote
2. Test it
3. Set up nodes


## Development

Run tests with:

```bash
pytest
```





