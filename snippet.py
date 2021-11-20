#!/usr/bin/env python 3.8
import os
import sublime
import sublime_plugin

scope = "text.html.markdown markup.raw.code-fence.rust.markdown-gfm source.rust meta.block.rust meta.block.rust"


def plugin_loaded():
    pass


class parse_code_blocks(sublime_plugin.EventListener):
    def on_load_async(
        self,
        view,
    ):
        window = sublime.active_window()
        if (
            os.path.dirname(os.path.dirname(os.path.dirname(view.file_name())))
            == sublime.packages_path()
        ):
            view.run_command("book")
            view.run_command("save")


class book(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        print("path")
        regions = (
            [view.line(x.b + 1) for x in view.find_all(r"```rust,[\w+,\w+]*\n{{#")]
            + [view.line(x.b + 1) for x in view.find_all(r"```rust\n{{#")]
            + [view.line(x.b + 1) for x in view.find_all(r"```console\n{{#")]
            + [view.line(x.b + 1) for x in view.find_all(r"```text\n{{#")]
        )
        i = 0

        paths = [
            view.substr(x)
            .split(" ")[1]
            .split(":")[0]
            .replace("}}", "")  # .replace("}", "")
            .replace("..", "Packages/rust-book")
            for x in regions
        ]

        print(paths)

        while len(regions) != 0:
            print(regions)
            view.replace(
                edit,
                regions[0],
                sublime.load_resource(paths[i]),
            )

            regions = (
                [view.line(x.b + 1) for x in view.find_all(r"```rust,[\w+,\w+]*\n{{#")]
                + [view.line(x.b + 1) for x in view.find_all(r"```rust\n{{#")]
                + [view.line(x.b + 1) for x in view.find_all(r"```console\n{{#")]
                + [view.line(x.b + 1) for x in view.find_all(r"```text\n{{#")]
            )
            i += 1


class doc_opener(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        file_name = (
            view.substr(view.line(view.sel()[0].b)).replace("├──", "").replace(" ", "")
        )
        path = "{}/rust-book/src".format(sublime.packages_path())
        for x in os.listdir(path):
            if x == file_name:
                print(x)
                main_path = "src/{}".format(os.path.basename(x))
                sublime.active_window().run_command("open_file", {"file": main_path})
                sublime.active_window().run_command("book")
