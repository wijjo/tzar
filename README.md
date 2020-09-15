# Tzar

Simplified compressed archive management.

## Features

* Minimal CLI options/arguments required for backup operations.
* Generate archive names based on working folder and time.
* Use faster compression programs and multiple cores, when available.
* Save location-specific defaults in configuration file.

## Tzar input specification

For simplicity and consistency `tzar` does not take a source file/folder
specification. It operates solely on the working folder. It can be optionally
tweaked to exclude files and folders.

## Tzar output specification

Tzar creates an archive file or populates a target folder based on a containing
folder, a name suffix temple, and an extension when it is an archive file.

### Target base folder

The target base folder can be a relative or absolute path.

Special shell symbols like "~" for the home folder and ".." for the parent
folder ar expanded.

A folder path ending with "/**" indicates that the source folder should be added
to the output folder path as a relative sub-folder. In effect, this allows the
backup structure to mirror a source folder tree.

### Target name suffix

The name suffix template can include normal characters and `time.strftime()`
format codes for date/time-based names.

An ending '#' character appends a unique counter to the file name, based on the
maximum counter value plus one. Please note that the '#' character only has
special meaning as the last character, and when date/time `%` codes are not
being used for unique name generation.

### Target path post-processing

"$<NAME>" environment variables in the final output path are expanded.

## Commands

Tzar command names select different archival methods.

* `tzar gz` creates `.tar.gz` compressed archives.
* `tzar xz` creates `.tar.xz` compressed archives.
* `tzar zip` creates `.zip` compressed archives.
* `tzar sync` performs folder synchronization using `rsync`.

## Configuration

For now `tzar` has no configuration. When the Jiig core supports aliases that
feature will allow operations to be captured, and they will be scope-able to
particular locations.

## Install (runnable source).

### 1) Clone Tzar to a local folder.

* See: https://github.com/wijjo/tzar

### 2) Clone Jiig to a local folder.

* See: https://github.com/wijjo/jiig

Jiig is a framework for building multi-command CLI tools. Tzar uses Jiig to
implement command line parsing and task execution.

### 3) Add the Jiig root folder to the system path.

### 4) Add the Tzar command to the system PATH.

#### Option 1: Add the Tzar folder to the shell `PATH`.

Update the `PATH` environment variable to include the root Tzar local repository
folder, e.g. in `~/.bashrc`.

#### Option 2: Symlink the `tzar` script to a folder that is already in the path.

The following example assumes `~/bin` exists and is already in the system
`PATH`. Adjust based on the actual Tzar local repository location.

```bash
$ cd ~/bin
$ ln -s /path/to/tzar/tzar .
```

### 4) Create the Tzar Python virtual environment.

Run the `tzar` command. The first run builds a virtual environment. At this
point it's ready to use.

