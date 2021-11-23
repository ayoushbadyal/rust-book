# rust-book


this is a minimal sublime plugin to make a rust documentation of book right in sublime text using the `readme` files of
the rust book

## instructions

1. clone `https://github.com/ayoushbadyal/rust-book.git` in `~/.config/sublime_text/Packages/ `
2. clone the repo `https://github.com/rust-lang/book.git` in desktop
3. run command on the terminal and `cd` into the cloned folder named `book` on desktop and run command
	`cp -r listings/ src/ ~/.config/sublime-text/Packages/rust-book`


** follow these right as the functionality of plugin is based on it and u are good to go **


5. open `command-pallete (ctrl+shift+p)` and type `rust-book: open document ` and use
	 `ctrl+shift+j` on the chapter to open the corresponding chapter u wanna open of the rust book
	or simply type `rust-book panel: open chapter list` in `command-pallete` to get all the chapter list and open then by clicking them

## others
1. if u want to see the image on hover run the bash file `converter.sh` `to convert svg to png`
2. in order to do this make sure u have `inkscape` installed
		and if not run command `sudo apt install inkscape`
3. after words hover over the image name and u woulkd be seeing the popup of the few images on hovering over them