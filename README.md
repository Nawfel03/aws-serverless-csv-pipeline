# ☁️ Event-Driven AWS Serverless File Processing & Monitoring Pipeline

An automated, event-driven data pipeline built entirely on **AWS**, within **Free Tier** limits. The architecture ingests CSV uploads, parses records through serverless compute, persists them to a NoSQL database, triggers real-time email alerts, and maintains full observability through logging and auditing.


## 📌 Overview

This project simulates a real-world cloud asset ingestion pipeline — the kind of automated workflow used by data teams to process incoming files without manual intervention. It was built as a hands-on portfolio project to demonstrate practical experience across compute, storage, database, networking, messaging, and security auditing services on AWS.

---

## 🏗️ Architecture Diagram

```
[ User / Admin EC2 ] ──> [ S3 Ingestion Bucket ]
                               │
                     (Object Created Trigger)
                               │
                               ▼
                    [ AWS Lambda Function ] (IAM Role)
                               │
         ┌─────────────────────┼─────────────────────┐
         ▼                     ▼                     ▼
 [ DynamoDB Table ]    [ Amazon SNS Alert ]  [ CloudWatch Logs ]
   (Data Storage)      (Email Notification)   (Metrics & Alarms)
         ▲                                           ▲
         └─────────────── [ CloudTrail ] ────────────┘
                       (Security Auditing)
```

---

## 🛠️ AWS Services Used (9 Total)

| Service | Purpose |
|---|---|
| **Amazon S3** | Ingestion bucket serving as the event source for new file uploads |
| **AWS Lambda** | Python serverless function that parses incoming CSV payloads |
| **Amazon DynamoDB** | NoSQL database storing parsed records with low-latency reads/writes |
| **Amazon SNS** | Notification topic delivering real-time email alerts on pipeline execution |
| **Amazon VPC** | Isolated network with public subnet and internet gateway for admin access |
| **Amazon EC2** | Amazon Linux 2023 instance inside the custom VPC for remote administration |
| **AWS IAM** | Execution role scoping Lambda's permissions to S3, DynamoDB, and SNS |
| **Amazon CloudWatch** | Centralized logging and metric alarms (e.g. error count thresholds) |
| **AWS CloudTrail** | Account-wide API activity trail for security and audit visibility |

---

## 🔄 How It Works

1. **Ingestion** — A user uploads a CSV file (`id, name, value`) to the S3 bucket.
2. **Trigger** — S3 emits an `s3:ObjectCreated:*` event that invokes the Lambda function.
3. **Transformation** — Lambda reads the file, parses each row, and writes items into DynamoDB.
4. **Notification** — Lambda publishes an execution summary to an SNS topic, alerting subscribers via email.
5. **Observability** — CloudWatch logs the Lambda execution while CloudTrail records the underlying API calls for auditing.

---

## 📄 Sample Input

`sample_data/test.csv`
```csv
id,name,value
101,Alpha,100
102,Beta,200
103,Gamma,300
```



## 💡 Key Takeaways

- **Event-driven automation** — decoupled ingestion from processing using native S3 event triggers, removing the need for polling or manual runs.
- **Scoped IAM permissions** — configured an execution role limited to the specific S3, DynamoDB, and SNS resources the function needs, rather than using broad managed policies.
- **End-to-end observability** — combined CloudWatch metric alarms with CloudTrail's audit trail so both operational errors and account-level API activity are tracked.

---

## 🚀 Future Improvements

- Tighten the IAM policy further into a fully least-privilege, resource-scoped JSON document.
- Add a Dead Letter Queue (SQS) for failed Lambda invocations.
- Add input validation and schema checks before writing to DynamoDB.
- Package infrastructure as code (Terraform / CloudFormation) for repeatable deployment.

---

## 👤 Author

**Nawfel**
Cloud/DevOps Engineer (Fresher) | AWS · Linux · Networking
[LinkedIn](https://www.linkedin.com/in/mohammed-nawfel-basha/) • [GitHub](https://github.com/Nawfel03)
