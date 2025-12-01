Get ready for a new Day:

`cp -r DayTemplate <year>/day<number>`

## Elixir Setup (via asdf)

This repo includes some solutions in Elixir. To run them, install Elixir using [asdf](https://asdf-vm.com/).

1. **Install asdf** (if not already installed)

   Follow the asdf docs for your OS:
   ```bash
   git clone [https://github.com/asdf-vm/asdf.git](https://github.com/asdf-vm/asdf.git) ~/.asdf --branch v0.14.0
   echo '. "$HOME/.asdf/asdf.sh"' >> ~/.bashrc    # or ~/.zshrc, etc.
   echo '. "$HOME/.asdf/completions/asdf.bash"' >> ~/.bashrc
   exec $SHELL