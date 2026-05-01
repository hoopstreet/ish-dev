#!/bin/bash
# Credential encryption/decryption for secure storage

ENCRYPT_DIR="/root/.hoopstreet/secure"
mkdir -p "$ENCRYPT_DIR"

encrypt_cred() {
    echo "$1" | openssl enc -aes-256-cbc -a -salt -pbkdf2 -pass pass:$2
}

decrypt_cred() {
    echo "$1" | openssl enc -aes-256-cbc -a -d -pbkdf2 -pass pass:$2
}

# Auto-backup encrypted credentials to Supabase
backup_secure() {
    tar -czf - "$ENCRYPT_DIR" | openssl enc -aes-256-cbc -out /tmp/secure_backup.enc
    # Upload to Supabase
}
