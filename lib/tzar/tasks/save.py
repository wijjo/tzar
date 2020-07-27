import os

from jiig.task import map_task, TaskRunner


@map_task(
    'save',
    help='save an archive of the working folder',
    options={
        ('-e', '--exclude'): {
            'dest': 'EXCLUDE',
            'nargs': '*',
            'help': 'exclusion pattern(s), including unix-style wildcards'},
        ('-g', '--gitignore'): {
            'dest': 'GITIGNORE',
            'action': 'store_true',
            'help': 'use .gitignore exclusions, if available'},
        ('-m', '--method'): {
            'dest': 'METHOD',
            'choices': ['gz', 'xz', 'zip', 'sync'],
            'help': 'archive method'},
        ('-t', '--target'): {
            'dest': 'TARGET',
            'help': 'target folder and name specification'},
    },
    arguments=[
        {'dest': 'SOURCE_FOLDER',
         'nargs': '*',
         'help': 'source folder(s) (default: working folder)'},
    ],
)
def task_gz(runner: TaskRunner):
    target_folders = runner.args.TARGET
    if not target_folders:
        target_folders.append(os.getcwd())
    for target_folder in target_folders:
        create_folder_archive(runner.args.SOURCE_FOLDER,
                              runner.args.EXCLUDE,
                              runner.args.GITIGNORE,
                              runner.args.METHOD,
                              runner.args.TARGET)
