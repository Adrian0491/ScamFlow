# ScamFlow - **Currently in a state of Work in Progress**

**ScamFlow** is an open-source reporting and monitoring toolkit designed to analyze, log, and report scam-related email activity. The tool aims to assist individuals, SOC teams, and cybersecurity enthusiasts in identifying, classifying, and submitting abuse reports against scam campaigns — with an eventual goal of visualizing trends through platforms like ElastiFlow, Grafana, or Kibana.

---

## 🎯 Project Objectives

- 🧪 Parse suspicious emails or `.eml` files to extract key metadata (headers, domains, links)
- 🌐 Perform IP/domain analysis (WHOIS, SPF/DKIM/DMARC, DNS)
- 🚨 Submit reports to known anti-abuse and anti-phishing platforms
- 📊 Log and format data to feed into ElastiFlow, SIEM, or threat intel dashboards
- 🛠️ Build an interactive CLI and optional Streamlit web dashboard

---

## 📦 Features (Planned & In Progress)

### ✔️ Initial Features
- [x] Raw email parser
- [x] Domain + IP extractor
- [x] WHOIS and AbuseIP lookups
- [x] Report generator (.json, .csv, .eml)

### 🚧 Upcoming
- [ ] Integration with [AbuseIPDB](https://www.abuseipdb.com/)
- [ ] Google Safe Browsing phishing report API
- [ ] Email campaign frequency tracking
- [ ] Streamlit dashboard or CLI `--report` output
- [ ] Export to Logstash-ready format for ElastiFlow ingestion

---

## 🖥️ How It Works (Overview)

## 🛠️ Installation

```bash
git clone https://github.com/yourusername/ScamFlow-Reporting.git
cd ScamFlow-Reporting
pip install -r requirements.txt

```
## **Usage**

```bash
python scamflow.py --file suspicious.eml --report --output json
python scamflow.py --paste-header
