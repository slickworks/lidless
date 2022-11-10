# Lidless

*A configurable backup system.*

## Overview

I want a backup strategy for my files that is:

* **Robust** - data backed up to multiple remotes.
* **Cheap** - make use of free plan allowances.
* **Kind** - lets me organise my directories as I please.

The barrier to achieving this is *granular control over subdirectories*. Lets use an example to see why.

### Example

I have a directory with all my  projects, and want to back up that up to an external drive using rsync, and to a cloud provider using rclone. 

But:

1. Some of my projects contain git repositories, which I want to exclude from the backup because they are large, and are source controlled anyway.
2. Some of those repositories contain files which are gitignored, which I *do* want to include in the backup.
3. Some of those file contain some sensitive data, so I only want to back those up to cloud, not my external drive.

```
/projects
  /project-1         # external & cloud
  /project-2         # external & cloud
    /notes           # external & cloud
    /code            # git repo: don't backup 
      /settings      # gitignored: cloud only
    db.sqlite3       # external & cloud 
```

Additionally, I want to be able to:

* Run backup to both remotes, or just one.
* Run backup only the current directory, or all.
* View which git repositories have unpushed commits.
* View changes before running backups.
* Easily change which directories ane included/ignored/tagged as repositories.

Lidess let me do all the above and more.

## Usage

Lidless runs from a configuration file written in JSON. You can edit it manually, or using the interactive shell commands (doesn't work yet).



1. Set up a remote
2. Test it
3. Set up nodes



With lidless I can configure all of this in a single JSON file:

```json
{
    "remotes": {
        "cloud": {
            "tool": "rclone",
            "provider": "mega"
        },
        "external": {
            "tool": "rsync",
            "dest": "/mnt/ext2/my-backups"
        }
    },
    "nodes": {
        "/projects": {
            "remotes": {
                "cloud": {},
                "external": {}
            },
            "/project-1/code": {
                "remotes": {
                    "git": {
                        "dest": "git@example.com/project-1.git"
                    }
                },
                "/settings": {
                    "remotes": {
                        "cloud": {}
                    }
                }
            }
        },
    }
}
```

Once in place:

1. 

## Development

Run tests with:

```bash
python -m unittest
```





