"""
                                        MINIMAL CODE SNIPPETS COLLECTOR

    This is a sublime helper plugin to  parse the  code blocks in the docs for rust-book in
    the readme files of the documentation based on some anchors specified by the file in the
    file-path in the code block

    i.e:  ```rust
            {{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-02-string-scope/src/main.rs:here}}
                        path -> ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        ```
    `here` is the anchor specified in original source file like this :

    fn main() {
        // ANCHOR: here
        {
            let s = String::from("hello"); // s is valid from this point forward

            // do stuff with s
        }                                  // this scope is now over, and s is no
                                           // longer valid
        // ANCHOR_END: here
    }

    now in the readme file it would be viewed as
    ```rust
        {
            let s = String::from("hello"); // s is valid from this point forward

            // do stuff with s
        }                                  // this scope is now over, and s is no
                                           // longer valid
    ```

"""

import os
import re

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
        try:
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
                            ferris_html
                            % (sublime.packages_path(), view.substr(ferris)),
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
        except Exception as e:
            pass


# ----------------------------------------------------------------------------------------------------------------------


def anchored_regions(view: sublime.View):
    try:
        regions = (
            [view.line(x.b + 1) for x in view.find_all(r"```rust,[\w+,\w+]*\n{{#")]
            + [view.line(x.b + 1) for x in view.find_all(r"```rust\n{{#")]
            + [view.line(x.b + 1) for x in view.find_all(r"```console\n{{#")]
            + [view.line(x.b + 1) for x in view.find_all(r"```text\n{{#")]
            + [view.line(x.b + 1) for x in view.find_all(r"```toml\n{{#")]
        )
        regions = sorted(
            regions, key=lambda x: x.a
        )  # found things were not sorted which may endup placing code at wrong spaces

        reg_path = r"[/\w+-.]+"
        reg_anchor = r":\w+"

        paths = [
            re.findall(reg_path, view.substr(x).split(" ")[1])[0].replace(
                "..", "Packages/rust-book"
            )
            for x in regions
        ]

        i = 0
        lames = []

        for x in regions:
            if len(view.substr(x).split(":")) != 3:
                res = re.findall(reg_anchor, view.substr(x).split(" ")[1])
                if len(res) == 0 or res == None:
                    lames.append("no_anchor")
                else:
                    lames.append(res[0].replace(":", ""))
            else:
                lames.append("no_anchor")

        final = list(zip(paths, lames))
        return regions, final

    except Exception:
        pass


def snip_anchors(path):
    # the thing which i am worried of is the punctuation since may not contain all the characters mainly the punctuation but that is fine.
    try:
        res = sublime.load_resource(path)
        regex = r"// ANCHOR: (\w+)\n+"
        main_ = re.findall(regex, res)
        lame = {}
        if len(main_) != 0:
            for x in main_:
                regex = r"""// ANCHOR: %s\n[\w+\s=:`;(){},./!$@#-^"'&*<+>|]+//\sANCHOR_END: %s\n""" % (  # @@@ punctuation
                    x,
                    x,
                )
                if len(re.findall(regex, res)) != 0:
                    main_con = (
                        re.findall(regex, res)[0]
                        .replace("// ANCHOR: %s" % (x), "")
                        .replace("// ANCHOR_END: %s" % (x), "")
                    )
                    lame[x] = main_con

        elif len(path.split(":")) == 3:
            """since usual paths are like `path:anchor` and some are like `path:a:b` from
            line a to line b which i dont wanna mess up with since it has only 1 implementation .
            """
            pass

        elif (
            len(main_) == 0
            or len(re.findall(regex, res)) == 0
            or len(path.split(":")) == 0
        ):
            lame["no_anchor"] = res

        return lame
    except Exception as e:
        pass


# ----------------------------------------------------------------------------------------------------------------------


class book(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        regions = anchored_regions(view)  # region
        try:
            while len(regions[0]) != 0:
                for path_and_anchor_val in regions[1]:
                    snippets = snip_anchors(path_and_anchor_val[0])
                    if len(snippets) != 0 or snippets != None:
                        if path_and_anchor_val[1] in list(snippets.keys()):
                            view.replace(
                                edit,
                                regions[0][0],
                                snippets[path_and_anchor_val[1]],
                            )
                            regions = anchored_regions(view)
                            break
                        elif (
                            path_and_anchor_val[1] == "no_anchor"
                            or len(path_and_anchor_val) == 1
                        ):
                            view.replace(
                                edit,
                                regions[0][0],
                                sublime.load_resource(path_and_anchor_val[0]),
                            )
                            regions = anchored_regions(view)
                            break
                    else:
                        view.replace(
                            edit,
                            regions[0][0],
                            sublime.load_resource(path_and_anchor_val[0]),
                        )
                        regions = anchored_regions(view)
                        pass
        except Exception as e:
            pass


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
                sublime.active_window().run_command("book")


class rust_book_panel(sublime_plugin.WindowCommand):  # quickpanel
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


class book_navigator_forward(
    sublime_plugin.WindowCommand
):  # todo implementing `clear_undo_stack`
    path = f"{sublime.packages_path()}/rust-book/src"

    def run(self):
        try:
            _dir = os.listdir(self.path)
            _dir.sort()
            cur_index = _dir.index(
                os.path.basename(sublime.active_window().active_view().file_name())
            )
            sublime.active_window().active_view().close()
            sublime.active_window().run_command(
                "open_file", {"file": f"{self.path}/{_dir[cur_index + 1]}"}
            )
        except Exception:
            pass


class book_navigator_backward(
    sublime_plugin.WindowCommand
):  # todo implementing `clear_undo_stack`
    path = f"{sublime.packages_path()}/rust-book/src"

    def run(self):
        try:
            _dir = os.listdir(self.path)
            _dir.sort()
            cur_index = _dir.index(
                os.path.basename(sublime.active_window().active_view().file_name())
            )
            sublime.active_window().active_view().close()
            sublime.active_window().run_command(
                "open_file", {"file": f"{self.path}/{_dir[cur_index - 1]}"}
            )
        except Exception:
            pass


"""
    author -> AYOUSH BADYAL
    github: https://github.com/ayoushbadyal

    i dont think of anyone using it but who knows ...
"""
