# Security and privacy — legacy implementation

This legacy script parses PDFs and sends their extracted text to an Ollama server. It is not a sandbox or a document sanitizer. Process only documents you trust and are authorized to translate, and keep dependencies and Ollama updated within compatible versions.

For local inference, use your local Ollama server and downloaded `gemma2` model. The Python client honors `OLLAMA_HOST`; a remote host receives the submitted text. Review host, proxy, and server settings before processing sensitive documents. The script itself does not enforce localhost or control external software's logging.

Do not commit private documents, translated output, API keys, secrets, credentials, logs, personal data, or model files. Translation failure output includes original text and error details; tracebacks can reveal paths. The script overwrites the configured output filename without confirmation. Review output destinations and staged source configuration carefully.

Ignore rules are preventive only: they do not remove tracked files or redact source code. If a secret is exposed, revoke/rotate it and remove it from the material being shared. If it has already entered Git history, coordinate remediation with the repository owner before changing history.

Report security issues privately through GitHub's **Report a vulnerability** option if the owner enables it. Otherwise use an existing private contact method supplied by the owner. If neither exists, open only a minimal public request for a private reporting channel, with no exploit details, documents, credentials, or personal paths. No security email address or response-time commitment has been established.
