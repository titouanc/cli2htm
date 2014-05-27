# CLI2HTM
Convert terminal output to HTML

## Installation and usage

Python2 or 3 required. For use-only: go somewhere in your `$PATH`, then

	wget https://raw.githubusercontent.com/titouanc/cli2htm/master/cli2htm.py
	chmod +x cli2htm.py

For development, clone this repo, `cd` into it; then

	virtualenv --distribute ve
	source ve/bin/activate
	pip install -r requirements.txt
	py.test --cov cli2htm --flakes test_cli2htm.py

## Options

* `-h/--help` List all options
* `-c/--context` Wrap output in minimal HTML document
* '-I/--inline' Inline style (ex: `<span style="color:#f00;">` instead of `<span class="cli30">`)
