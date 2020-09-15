More and better explanation of output specifications is needed.

Add mirroring-style restore that deletes files that no longer belong. Probably
requires a mechanism for recording options used for saving an archive so that
exclusions, gitignore, etc. are handled properly. I.e. should only delete files
that are not in the archive to restore when they are not excluded by the
original options. One possible solution would be to pair a JSON or text file
with the archive that has the original option set. Could use a '.options'
extension perhaps.
