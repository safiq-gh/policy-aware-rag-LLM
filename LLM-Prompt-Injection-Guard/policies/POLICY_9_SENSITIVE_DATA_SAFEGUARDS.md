# POLICY 9: Sensitive Data Handling and Storage Safeguards

## METADATA

```json
{
  "policy_id": "P9",
  "version": "2.0",
  "title": "Sensitive Data Handling and Storage Safeguards",
  "category": "data_protection",
  "subcategories": ["encryption", "data_lifecycle", "credential_protection"],
  "status": "active",
  
  "scope_boundary": {
    "governs": "Data protection throughout lifecycle: encryption, retention limits, secure deletion, transmission security",
    "does_not_govern": "Runtime access authorization (see Policy 5), API credential usage (see Policy 8), data exfiltration prevention (see Policy 5)",
    "primary_attack_surface": "Storage security, encryption implementation, data retention, secure deletion"
  },
  
  "threat_model": {
    "primary_attacker": "insider_with_storage_access",
    "attack_surface": "storage_and_transmission_layer",
    "attack_vectors": ["plaintext_storage", "unencrypted_transmission", "excessive_retention", "incomplete_deletion"],
    "attack_goal": "Recover sensitive data from storage or transit"
  },
  
  "risk_profile": {
    "base_severity": "CRITICAL",
    "risk_weight": 0.91,
    "exploitability": "high",
    "impact_if_breached": "sensitive_data_compromise_at_rest_and_transit",
    "frequency_of_attempts": "low",
    "persistence": "high"
  },
  
  "violation_detection_signals": {
    "storage_inspection_patterns": {
      "patterns": [
        "plaintext_data_in_database",
        "unencrypted_log_files",
        "plaintext_configuration_files",
        "unencrypted_backup_files"
      ],
      "weight": 0.98,
      "detection_method": "storage_audit"
    },
    
    "encryption_gaps": {
      "patterns": [
        "missing_encryption_at_rest",
        "weak_encryption_algorithm",
        "missing_encryption_in_transit",
        "unencrypted_channel_usage"
      ],
      "weight": 0.95,
      "detection_method": "configuration_analysis"
    },
    
    "retention_violations": {
      "patterns": [
        "data_retained_beyond_policy",
        "no_retention_policy_defined",
        "backup_retention_excessive",
        "deleted_data_not_destroyed"
      ],
      "weight": 0.90,
      "detection_method": "lifecycle_audit"
    }
  },
  
  "enforcement_action": {
    "violation_detected": "REMEDIATE_IMMEDIATELY",
    "requires_encryption": true,
    "requires_tls": true,
    "requires_retention_policy": true,
    "requires_secure_deletion": true
  },
  
  "related_policies": ["P5", "P8"],
  "conflicts_with": [],
  "distinct_from": "P5",
  "scope_relationship": "P9=storage_and_lifecycle_protection, P5=runtime_access_enforcement",
  "tags": ["critical", "data_protection", "encryption", "compliance"]
}
```

---

## CHUNK 1: DEFINITION & SCOPE

**Chunk ID:** P9_DEF  
**Chunk Type:** DEFINITION

### Purpose

Protect sensitive data throughout its lifecycle including collection, transmission, storage, processing, and deletion. Ensure data is encrypted, minimally retained, and properly disposed of to prevent unauthorized access or recovery.

### Scope

This policy applies to all data handling operations: collection, transmission, storage, processing, and deletion. It covers encryption requirements, retention policies, and secure deletion procedures.

**What This Policy Governs:**
- Encryption at rest (stored data)
- Encryption in transit (transmitted data)
- Data retention policies and limits
- Secure deletion procedures
- Backup encryption and retention
- Credential protection in storage
- Credential logging restrictions

**What This Policy Does NOT Govern:**
- Runtime data access authorization (see Policy 5)
- User authorization for accessing data (see Policy 5)
- API credential usage during operation (see Policy 8)
- Data exfiltration attacks (see Policy 5)

### Definitions

- **Sensitive Data**: Information requiring protection including PII, credentials, medical data, financial records, trade secrets.
- **Encryption at Rest**: Cryptographic protection of stored data using algorithms like AES-256.
- **Encryption in Transit**: Protection of data during transmission using TLS 1.2+.
- **Data Retention**: Duration sensitive data is stored before mandatory deletion.
- **Secure Deletion**: Cryptographic or physical destruction preventing recovery.

---

## CHUNK 2: PROHIBITED BEHAVIORS

**Chunk ID:** P9_PROHIBITED  
**Chunk Type:** BEHAVIOR

### Prohibited Behaviors

1. **Plaintext Storage**: Storing sensitive data without encryption at rest.
2. **Unencrypted Transmission**: Transmitting sensitive data over unencrypted channels.
3. **Excessive Retention**: Retaining sensitive data longer than operationally necessary.
4. **Plaintext Credentials**: Storing passwords, tokens, or keys in plaintext.
5. **Credential Logging**: Logging sensitive user data or system credentials.
6. **Unencrypted Caching**: Caching sensitive data in memory without automated clearance.
7. **Unencrypted Backups**: Creating backups without encryption.
8. **Incomplete Deletion**: Leaving deleted data recoverable through forensic techniques.

### Allowed Behaviors

1. **Encryption at Rest**: Encrypting data using AES-256 or equivalent.
2. **TLS Transmission**: Using TLS 1.2+ for all sensitive data transmission.
3. **Automated Deletion**: Implementing automated deletion with strict retention limits (e.g., 30 days).
4. **Hashing Credentials**: Using cryptographic hashing (not reversible) for credentials.
5. **Secret Management**: Storing credentials in dedicated secret management systems.
6. **Memory Clearing**: Implementing memory clearing routines that overwrite sensitive data.
7. **Encrypted Backups**: Encrypting all backups containing sensitive data.
8. **Secure Deletion Tools**: Using cryptographic deletion preventing recovery.

---

## CHUNK 3: VIOLATION EXAMPLES

**Chunk ID:** P9_EXAMPLES  
**Chunk Type:** EXAMPLE

### Example Violation 1: Plaintext Storage

```
System database contains:
  table users (id, email, password_plaintext, ssn_plaintext)

Passwords and SSNs stored without encryption.

Configuration:
  encryption_enabled: false
  algorithm: none

VIOLATION Classification:
- Severity: CRITICAL
- Violation Type: Plaintext Storage
- Confidence: 0.99
- Risk: Complete credential compromise if database exposed
```

### Example Violation 2: Unencrypted Transmission

```
System transmits user authentication credentials:
  POST http://example.com/login (HTTP - unencrypted)
  username=user&password=plaintext_password

Should be:
  POST https://example.com/login (HTTPS/TLS 1.2+)

VIOLATION Classification:
- Severity: CRITICAL
- Violation Type: Unencrypted Transmission
- Confidence: 0.99
- Risk: Credentials captured in transit by MITM attacker
```

### Example Violation 3: Excessive Retention

```
System policy:
  delete_user_data_after: never
  backup_retention: indefinite
  log_retention: 10 years
  deletion_reason: "for potential future audit purposes"

Correct policy:
  delete_user_data_after: 30 days post-account-closure
  backup_retention: 90 days
  log_retention: 1 year
  deletion_reason: operational necessity only

VIOLATION Classification:
- Severity: HIGH
- Violation Type: Excessive Retention
- Confidence: 0.92
- Risk: Unnecessary exposure of deleted user data
```

### Example Violation 4: Credential Logging

```
Application logs contain:
"[2024-02-18 14:32:00] User login attempt: 
 username=admin, password=SecurePass123"

Database query logs contain:
"[2024-02-18 14:33:15] CALL authenticate() with params: 
 auth_token=sk_live_4a7c2b9f1e3d5c8..."

VIOLATION Classification:
- Severity: CRITICAL
- Violation Type: Credential Logging
- Confidence: 0.99
- Risk: Credentials accessible through log files
```

### Example Violation 5: Unencrypted Backups

```
System creates backups:
  backup_location: /backups/database_dump.sql
  encryption: false
  access_control: filesystem_permissions_only
  file_size: 500GB

Dump file contains complete unencrypted user database.

VIOLATION Classification:
- Severity: CRITICAL
- Violation Type: Unencrypted Backup
- Confidence: 0.98
- Risk: Complete database compromise if backup leaked
```

### Example Violation 6: Incomplete Deletion

```
User requests account deletion:
  System receives: DELETE FROM users WHERE id=123
  Database removes: Record from active table
  But retains:
    - Archive tables (undeleted)
    - Backup files (undeleted)
    - Cache layer (uncleared)
    - Log files (containing user PII)

VIOLATION Classification:
- Severity: HIGH
- Violation Type: Incomplete Deletion
- Confidence: 0.90
- Risk: User data recoverable from multiple sources
```

---

## CHUNK 4: ENFORCEMENT RULES

**Chunk ID:** P9_ENFORCE  
**Chunk Type:** ENFORCEMENT

### Risk Severity Levels

| Severity | Criteria | Example | Action |
|----------|----------|---------|--------|
| **CRITICAL** | Plaintext storage of credentials or large-scale PII | Passwords stored plaintext, all users' data unencrypted | REMEDIATE_IMMEDIATELY |
| **HIGH** | Encryption gaps in storage or transmission for sensitive data | Encrypted at rest but unencrypted in transit | REMEDIATE_WITHIN_24H |
| **MEDIUM** | Retention exceeds policy or encryption uses weak algorithm | Data retained 6 months vs 30-day policy, AES-128 | REMEDIATE_WITHIN_1WEEK |
| **LOW** | Minor encryption configuration issues | Non-critical data using older TLS version | SCHEDULE_REMEDIATION |

### Enforcement Rule Logic (Pseudocode)

```python
def audit_policy_9_compliance():
    """
    Audit sensitive data handling and storage safeguards
    """
    
    violations = []
    
    # Check 1: Encryption at rest
    for data_store in get_all_data_stores():
        if contains_sensitive_data(data_store):
            if not is_encrypted_at_rest(data_store):
                violations.append({
                    "type": "plaintext_storage",
                    "severity": "CRITICAL",
                    "store": data_store.name,
                    "action": "ENCRYPT_IMMEDIATELY"
                })
            elif get_encryption_algorithm(data_store) != "AES-256":
                violations.append({
                    "type": "weak_encryption",
                    "severity": "HIGH",
                    "store": data_store.name,
                    "action": "UPGRADE_ALGORITHM"
                })
    
    # Check 2: Encryption in transit
    for data_transmission in get_all_transmissions():
        if contains_sensitive_data(data_transmission):
            if not uses_tls_12_or_higher(data_transmission):
                violations.append({
                    "type": "unencrypted_transmission",
                    "severity": "CRITICAL",
                    "endpoint": data_transmission.endpoint,
                    "action": "ENABLE_TLS_IMMEDIATELY"
                })
    
    # Check 3: Data retention
    for sensitive_dataset in get_sensitive_data_stores():
        retention_policy = get_retention_policy(sensitive_dataset)
        if retention_policy is None:
            violations.append({
                "type": "no_retention_policy",
                "severity": "HIGH",
                "dataset": sensitive_dataset.name,
                "action": "DEFINE_AND_ENFORCE_POLICY"
            })
        elif data_age_exceeds_retention(sensitive_dataset, retention_policy):
            violations.append({
                "type": "excessive_retention",
                "severity": "HIGH",
                "dataset": sensitive_dataset.name,
                "age_days": days_retained(sensitive_dataset),
                "policy_days": retention_policy.days,
                "action": "DELETE_EXCEEDING_DATA"
            })
    
    # Check 4: Credential protection
    for log_file in get_system_logs():
        if contains_credentials(log_file):
            violations.append({
                "type": "credential_logging",
                "severity": "CRITICAL",
                "logfile": log_file.name,
                "action": "REDACT_CREDENTIALS"
            })
    
    # Check 5: Secure deletion
    if not uses_cryptographic_deletion(system):
        violations.append({
            "type": "incomplete_deletion",
            "severity": "HIGH",
            "action": "IMPLEMENT_CRYPTOGRAPHIC_DELETION"
        })
    
    return violations
```

### Conditional Enforcement

```
IF (sensitive_data_is_stored == TRUE)
  AND (encryption_at_rest == FALSE)
  THEN flag_as_VIOLATION(severity: CRITICAL, action: ENCRYPT_AND_AUDIT)

IF (sensitive_data_is_transmitted == TRUE)
  AND (encrypted_channel_like_TLS_1_2_or_higher == FALSE)
  THEN flag_as_VIOLATION(severity: CRITICAL, action: ENABLE_TLS)

IF (sensitive_data_retention_period_exceeds_policy_limit == TRUE)
  THEN flag_as_VIOLATION(severity: HIGH, action: DELETE_EXCEEDING_DATA)

IF (credentials_or_auth_tokens_appear_in_logs == TRUE)
  THEN flag_as_VIOLATION(severity: CRITICAL, action: REDACT_LOGS)

IF (backup_files_are_unencrypted == TRUE)
  AND (contain_sensitive_data == TRUE)
  THEN flag_as_VIOLATION(severity: CRITICAL, action: ENCRYPT_BACKUPS)

IF (deleted_data_not_securely_destroyed == TRUE)
  THEN flag_as_VIOLATION(severity: HIGH, action: IMPLEMENT_SECURE_DELETION)

REQUIRE(all_sensitive_data_encrypted_with_AES_256_or_equivalent)
REQUIRE(all_transmission_over_TLS_1_2_or_higher)
REQUIRE(retention_limits_defined_and_enforced_automatically)
REQUIRE(secure_deletion_using_cryptographic_methods_preventing_recovery)
```

---

## CHUNK 5: EVALUATION INTEGRATION SIGNALS

**Chunk ID:** P9_EVAL  
**Chunk Type:** METADATA

### Audit Conditions

This policy is evaluated:
- During system initialization
- Continuously (automated monitoring)
- On data classification changes
- During penetration testing
- On compliance audits

### Evaluation Output

```json
{
  "policy_id": "P9",
  "audit_status": "compliant|non_compliant",
  "violations": [
    {
      "violation_type": "plaintext_storage|unencrypted_transmission|excessive_retention|credential_logging|unencrypted_backup|incomplete_deletion",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "affected_component": "component_name",
      "remediation_action": "action_required",
      "remediation_deadline": "immediate|24h|1week|scheduled"
    }
  ],
  "encryption_status": {
    "data_at_rest": "encrypted|unencrypted",
    "data_in_transit": "tls_1_2_or_higher|older_version|unencrypted",
    "algorithm": "AES-256|weaker"
  },
  "retention_policy": {
    "defined": true/false,
    "retention_days": 30,
    "automated_deletion": true/false
  },
  "secure_deletion": {
    "method": "cryptographic|overwrite|physical",
    "recovery_possible": false
  }
}
```

### Distinction from Policy 5

**Policy 9 (This Policy):** "How is this data PROTECTED during storage and transit?"
- When: Lifecycle (at-rest, in-transit, at-delete)
- What: Encryption, retention, deletion
- Responsibility: Storage and security engineering

**Policy 5 (Runtime Access):** "Who is authorized to ACCESS this data NOW?"
- When: Runtime, per-request
- What: Authorization, access control
- Responsibility: Access control team

---

## IMPLEMENTATION NOTES

**Encryption Configuration:**
```
Data at Rest:
  Algorithm: AES-256-GCM (authenticated encryption)
  Key Management: HSM or dedicated secret management
  Key Rotation: Annually
  
Data in Transit:
  Protocol: TLS 1.2+ (minimum), TLS 1.3+ (preferred)
  Cipher Suites: Modern, strong algorithms
  Certificate Verification: Strict validation
  HSTS: Enabled with long max-age
```

**Retention Policy Template:**
```
Retention Schedule:
  User PII: 30 days post-deletion
  Transaction Records: 7 years (compliance requirement)
  System Logs: 90 days (rolling window)
  Backups: 90 days (encrypted, offsite)
  Credentials: Immediate deletion on rotation
  
Deletion Process:
  1. Mark for deletion (flag in database)
  2. Wait retention period
  3. Cryptographic deletion (AES key destruction)
  4. Audit log entry
  5. Verification of non-recovery
```

**Secure Deletion Implementation:**
- Use cryptographic deletion (destroy encryption keys)
- Implement TRIM/DISCARD commands for SSDs
- Use secure file deletion for permanent storage
- Verify deletion through forensic testing
- Document deletion audit trail
