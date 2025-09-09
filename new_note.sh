#!/usr/bin/env bash

# Base directories
INBOX_DIR="$PWD/inbox"
PERMANENT_DIR="$PWD/permanent"
REFERENCES_DIR="$PWD/references"

# UUID for filenaame
UUID=$(uuidgen)
FILENAME="${INBOX_DIR}/${UUID}.adoc"

# Read Note Title
read -p "Title: " TITLE
TIMESTAMP=$(date +"%Y-%m-%dT%H:%M:%S")

# Add content (End with CTRL+D)
echo "Note Content (End with CTRL+D):"
USER_CONTENT=$(</dev/stdin)

# Generate document scaffold
cat >"$FILENAME" <<EOF
= ${TITLE}
:created: ${TIMESTAMP}
:id: ${UUID}
:tags: #Default

== Note

${USER_CONTENT}

== References

// Add references here
// xref:file.adoc[]

EOF

echo "New Inbox Note create: $FILENAME"
