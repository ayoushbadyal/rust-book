import os
import sublime
import sublime_plugin

scope = "text.html.markdown markup.raw.code-fence.rust.markdown-gfm \
            source.rust meta.block.rust meta.block.rust"


def plugin_loaded():
    pass


class snippet_collector(sublime_plugin.EventListener):
    def on_load_async(self, view):
        window = sublime.active_window()
        if "/".join(view.file_name().split("/")[:-3]) == sublime.packages_path():
            view.run_command("book")
            view.run_command("save")
            view.set_read_only(True)

    def on_hover(
        self, view, point, hover_zone
    ):  # shows images if the user have installed `inkscape`
        if os.path.exists(
            "/".join(sublime.packages_path().split("/")[:-2]) + "/inkscape"
        ):
            a = view.expand_by_class(
                point,
                sublime.CLASS_WORD_START
                | sublime.CLASS_WORD_END & sublime.CLASS_SUB_WORD_START,
            )

            image_name = view.substr(sublime.Region(a.a, a.b + 2))
            # ---------------------------------------- for the referal images ----------------------------------------------
            contents = """
            <body>
            <style>
                img{
                    height: 450px;
                    width: 550px;
                    background-color: powderblue;
                }
            </style>

            <img src= "file://%s/rust-book/src/img/%s.png">
            </body>
            """
            ###-------------------------------------------- showing the code result ( ferris )------------------------------
            ferris = view.expand_by_class(
                point,
                sublime.CLASS_PUNCTUATION_END
                | sublime.CLASS_PUNCTUATION_START
                | sublime.CLASS_LINE_END
                | sublime.CLASS_PUNCTUATION_END,
            )
            ferris_html = """
            <body>
            <style>
                img{
                    height: 110px;
                    width: 230px;
                    background-color: powderblue;
                }
            </style>
            <img src= "file://%s/rust-book/src/img/ferris/%s.png">
            </body>"""

            if (
                "/".join(view.file_name().split("/")[:-2])
                == sublime.packages_path() + "/rust-book"
            ):
                if image_name + ".png" in os.listdir(
                    sublime.packages_path() + "/rust-book/src/img"
                ):
                    view.show_popup(
                        contents % (sublime.packages_path(), image_name),
                        # flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY,
                        flags=(
                            sublime.HIDE_ON_MOUSE_MOVE_AWAY
                            | sublime.HIDE_ON_CHARACTER_EVENT
                        ),
                        max_width=500,
                        max_height=500,
                        location=point,
                    )
                elif view.substr(ferris) + ".png" in os.listdir(
                    sublime.packages_path() + "/rust-book/src/img/ferris"
                ):
                    view.show_popup(
                        ferris_html % (sublime.packages_path(), view.substr(ferris)),
                        # flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY,
                        flags=(
                            sublime.HIDE_ON_MOUSE_MOVE_AWAY
                            | sublime.HIDE_ON_CHARACTER_EVENT
                            | sublime.KEEP_ON_SELECTION_MODIFIED
                        ),
                        max_width=500,
                        max_height=500,
                        location=point,
                    )
        else:
            pass


class book(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
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

        while len(regions) != 0:
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
                main_path = "src/{}".format(os.path.basename(x))
                sublime.active_window().run_command("open_file", {"file": main_path})
                # sublime.active_window().run_command("book")


class rust_book_panel(sublime_plugin.WindowCommand):
    path = f"{sublime.packages_path()}/rust-book/src"

    def run(self):
        contents = os.listdir(self.path)
        contents.sort()

        self.window.show_quick_panel(
            items=contents, on_select=lambda idx: self.select_item(contents, idx)
        )

    def select_item(self, items, idx):
        if idx >= 0:
            self.window.run_command(
                "open_file",
                {"file": f"{self.path}/" + items[idx]},
            )
