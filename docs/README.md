# Documentation Structure

This directory contains the documentation for the Mock GPS API, organized by security level.

## Directory Structure

```
docs/
├── public/          # Safe for public consumption
│   ├── README.md
│   └── API.md
├── internal/        # Internal documentation (in git)
│   └── DEPLOYMENT.md
└── secrets/         # Sensitive information (encrypted)
    └── api-keys.md
```

## Documentation Levels

### Public Documentation (`public/`)
- **Purpose**: Safe for public consumption, GitHub, sharing
- **Content**: 
  - General app features and capabilities
  - Installation instructions (without sensitive configs)
  - API documentation (without keys/endpoints)
  - User-facing features
- **Git Status**: Committed and pushed to repository

### Internal Documentation (`internal/`)
- **Purpose**: Team/internal use, version controlled but not public
- **Content**:
  - Configuration templates (with placeholder values)
  - Deployment procedures (with variable placeholders)
  - Troubleshooting guides
  - Architecture diagrams (anonymized)
- **Git Status**: Committed and pushed to repository

### Secret Documentation (`secrets/`)
- **Purpose**: Sensitive operational information
- **Content**:
  - Actual API keys and credentials
  - Specific machine configurations
  - Security configurations
  - Network topology
- **Git Status**: Encrypted with git-crypt, committed but encrypted

## Accessing Secret Documentation

The `secrets/` directory is encrypted using git-crypt. To access the sensitive information:

```bash
# Decrypt the secrets directory
git-crypt unlock

# View sensitive files
cat docs/secrets/api-keys.md

# Re-encrypt when done (automatic on commit)
git add docs/secrets/
git commit -m "Document restructure"
```

## Security Notes

- **Never commit unencrypted sensitive information**
- **Always use git-crypt for the secrets/ directory**
- **Keep API keys and IP addresses in the secrets/ directory only**
- **Use placeholder values in public and internal documentation**

## Contributing

When adding new documentation:

1. **Public docs**: Add to `public/` directory
2. **Internal docs**: Add to `internal/` directory with placeholder values
3. **Sensitive docs**: Add to `secrets/` directory (will be automatically encrypted)

## Backup Strategy

The secrets directory is encrypted in git, but should also be backed up securely:

1. **Git repository**: Contains encrypted secrets
2. **Local backup**: Regular backup of the entire repository
3. **Secure storage**: Encrypted backup of sensitive information
