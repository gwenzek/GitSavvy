from sublime_plugin import WindowCommand, TextCommand
import re

from ..git_command import GitCommand

SHOW_COMMIT_TITLE = "COMMIT: {}"
COMMIT_REGEX = re.compile(r"[A-fa-f0-9]{6,}")


class GsShowCommitCommand(WindowCommand, GitCommand):

    def run(self, commit_hash):
        repo_path = self.repo_path
        view = self.window.new_file()
        init_commit_view(view, commit_hash, repo_path)
        update_commit_view(view)


class GsShowCommitInitializeView(TextCommand, GitCommand):

    def run(self, edit):
        commit_hash = self.view.settings().get("git_savvy.show_commit_view.commit")
        content = self.git("show","--no-color", commit_hash)
        self.view.run_command("gs_replace_view_text", {"text": content, "nuke_cursors": True})


class GsShowCommitUnderCursor(TextCommand, GitCommand):

    def run(self, edit, commit_hash=''):
        print("hello")
        print(edit, commit_hash)

        view = self.view

        if not commit_hash:
            region = self.view.sel()[0]

            if region.begin() == region.end():
                region = view.word(region)
            commit_hash = view.substr(region)

        if not COMMIT_REGEX.match(commit_hash):
            print("%s isn't a valid commit hash" % commit_hash)
            return

        commit_view = view.window().new_file()
        init_commit_view(commit_view, commit_hash, self.repo_path)
        update_commit_view(commit_view)


def init_commit_view(view, commit_hash, repo_path):
    view.set_syntax_file("Packages/GitSavvy/syntax/show_commit.sublime-syntax")
    view.settings().set("git_savvy.show_commit_view", True)
    view.settings().set("git_savvy.show_commit_view.commit", commit_hash)
    view.settings().set("git_savvy.repo_path", repo_path)
    view.settings().set("word_wrap", False)
    view.settings().set("line_numbers", False)
    view.set_name(SHOW_COMMIT_TITLE.format(commit_hash[:7]))
    view.set_scratch(True)

    return view


def update_commit_view(view):
    view.run_command("gs_show_commit_initialize_view")
