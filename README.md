# Tzar

Simplified compressed archive management.

## Features

* Minimal CLI options/arguments are required for basic backup operations.
* Automatically generated archive names based on the working folder and time.
* Use faster compression programs and multiple cores, when available.
* Save location-specific options as tzar aliases.
* Full command line help using the `help` sub-command.

## Tzar command line overview

For simplicity, `tzar` does not normally need to have a source file/folder
specified. By default it operates on the working folder, but can also be pointed
at anything from anywhere. Options are also available to exclude files and
folders. Complex option sets can be saved as aliases.

Also for simplicity, Tzar defaults to automatically naming saved archives using
the source folder name and a timestamp. It place archives in a `../tzarchive`
folder relative to the source location. It uses standard compressed archive
naming conventions for the file extensions.

For example, the `tzar save` command creates a timestamped `gzip` archive of the
working folder in `../tzarchive`. To use `xz` compression instead of `gzip`, add
the `-m xz` option.

### Target archive names

Target archive names use the source name plus a suffix. The default suffix
format can be overridden with a template that accepts normal characters and
`time.strftime()` format codes for date/time-based names. 

The suffix also supports converting an ending '#' character to a unique counter
to avoid base file name collisions.

Please note that the '#' character only has special meaning as the last
character, and only has an effect when date/time `%` codes are not being used
for unique name generation.

### Target path post-processing

"$NAME" environment variables are expanded in the final output path.

## Command overview

The commands below are commonly used. Please browse the `tzar` command line help
system for more information about available sub-commands.

* `tzar help` or `tzar help COMMAND ...` provides top level or sub-command help.
* `tzar save` creates a timestamped `gzip` archive of the working folder in
  `../tzarchive`.
* `tzar save -m zip` and `tzar save -m xz` archives the working folder using
  `zip` or `xz` compression.
* `tzar save -m files` uses `rsync` to copy files into a `../tzarchive`
  sub-folder.
* `tzar catalog` lists timestamps of existing archives of the working folder.
* `tzar catalog -l` lists timestamps and file names of existing archives of the
  working folder.
* `tzar delete` and `tzar prune` support clearing out excess saved archives.

## Configuration and aliases

For now `tzar` has no configuration file. The Jiig core supports aliases that
allow operations and options to be captured and used. Aliases can be scoped to
particular locations, but can also apply globally.

### Alias example: creation

The example below demonstrates alias creation with different options for
different locations. Each location has its own compression method and
exclusions. But the alias name represents a single logical command.

```shell
$ cd /my/project1
$ tzar alias set .bkp save -m gz -e __cache__
$ cd /my/project2
$ tzar alias set .bkp save -m zip -e dist -e build 
```

### Alias example: usage

The example below demonstrates using a named alias with per-location
customizations. It is based on the creation example above.

```shell
$ cd /my/project1
$ tzar .bkp
$ cd /my/project2
$ tzar .bkp 
```

## Installation (to run from local source repository).

The following examples place Tzar and Jiig under `/usr/local` and create
symlinks in `/usr/local/bin`, assuming that folder is in the shell execution
path.

Alternatively, you can place Tzar and Jiig under your home folder and create
symlinks in `~/bin`, assuming it is in your shell execution path.

### 1) Clone Jiig to a local folder and add the `jiig` command to the path.

Jiig is a framework for building multi-command CLI tools. Tzar uses Jiig to
implement command line parsing, task execution, and alias management.

* See: https://github.com/wijjo/jiig

```shell
$ cd /usr/local
$ git clone https://github.com/wijjo/jiig.git
$ ln -s /usr/local/jiig/bin/jiig /usr/local/bin
```

### 2) Clone Tzar to a local folder and add the `tzar` command to the path.

* See: https://github.com/wijjo/tzar

```shell
$ cd /usr/local
$ git clone https://github.com/wijjo/tzar.git
$ ln -s /usr/local/tzar/bin/tzar /usr/local/bin
```

### 3) Create the Tzar Python virtual environment.

Run the `tzar` command. The first run builds a virtual environment. At this
point it's ready to use.
