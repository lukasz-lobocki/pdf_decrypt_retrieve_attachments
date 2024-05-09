#!/usr/bin/env bash

echo "
*** STARTING post-consumption ${TASK_ID} ***

A document with an ID of ${DOCUMENT_ID} was just consumed.

Filename of original document: ${DOCUMENT_ORIGINAL_FILENAME}
Generated file name: ${DOCUMENT_FILE_NAME}

Archive path: ${DOCUMENT_ARCHIVE_PATH}
Source path: ${DOCUMENT_SOURCE_PATH}
Thumbnail path: ${DOCUMENT_THUMBNAIL_PATH}

Created: ${DOCUMENT_CREATED}
Added: ${DOCUMENT_ADDED}
Modified: ${DOCUMENT_MODIFIED}

Download URL: ${DOCUMENT_DOWNLOAD_URL}
Thumbnail URL: ${DOCUMENT_THUMBNAIL_URL}

Correspondent: ${DOCUMENT_CORRESPONDENT}
Tags: ${DOCUMENT_TAGS}

=== STOPPING post-consumption ${TASK_ID} ===
"
