# termux-gui-red

A reddit client for Termux using [Termux:GUI](https://github.com/termux/termux-gui).

Current features:
- Searching subreddits
- Viewing subreddits
  - Sort by new, hot and top
- View comments
- See image posts (only some formats)
- Vote on posts and comments
- Create posts (long press on the subreddit title)
- Create comments (long press on the post title or comment)

## Installing

Download a file from the releases, or just build it yourself, it only needs Python and Bash.


## Dependencies

- Python: Install with `pkg i python`
- For the release without bundled dependencies:
  - [Termux:GUI Python bindings](https://github.com/tareksander/termux-gui-python-bindings): Install with `pip install termuxgui`
  - praw: Install with `pip install praw`
  - requests: Install with `pip install requests`


## Building

````bash
git clone https://github.com/tareksander/termux-gui-red.git
cd termux-gui-red
./build.sh
````

`tgui-red` is build in the directory and can be run after that.


