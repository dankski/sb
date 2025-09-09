# Second Brain 

## Overview

Second Brain is a personal knowledge management system designed to help you organize, capture, and retrieve information efficiently.

## Features

- Note-taking and organization
- Tagging and search functionality
- Integration with external tools
- Easy backup and restore

Folder organization:

inbox/ → quick notes, not yet sorted

permanent/ → fully developed notes (permanent zettels)

literature/ → notes with literature excerpts or sources

archive/ → old or no longer relevant notes

## Installation

Clone the repository:

```bash
git clone https://github.com/sb/second-brain.git
cd second-brain
```

Install dependencies:

```bash
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

You also need to install **asciidoctor**. Please refer to [Install and Update](https://docs.asciidoctor.org/asciidoctor/latest/install/)

## Usage

To write a new note simply start shell script:

```bash
./new_note.sh
```

When you run the script, you will be prompted to enter a title for your note. After pressing Enter, you can type the note text. To finish and save the note, press <CTRL+D>.
The new note will be saved in the `inbox` folder, where you can review and edit it later.

If you are satisfied with your note, you can move it from the `inbox` folder to the `permanent` folder for long-term storage and organization.

Start the graph:

```bash
./note_graph.py
```

This opens automatically a browser window.

## Contributing

Contributions are welcome! Please open issues or submit pull requests.

## License

This project is licensed under the MIT License.