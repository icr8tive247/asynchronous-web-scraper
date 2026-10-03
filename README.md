# High-Throughput Asynchronous Web Extraction Pipeline

A robust, enterprise-grade data engineering script written in Python. This project showcases optimal architectures for web scraping, asynchronous DOM parsing, dynamic JavaScript execution, and data serialization pipelines.

Designed explicitly to demonstrate production-ready engineering patterns when handling non-trivial, client-side rendered web targets.

## 🚀 Architectural & Engineering Highlights

*   **Asynchronous I/O Core Engine:** Implemented utilizing Python’s native `asyncio` loop coupled with the **Playwright Async API**. This setup ensures non-blocking networking operations and optimized I/O multiplexing, making it significantly faster and lighter than thread-bound frameworks like Selenium.
*   **Dynamic Client-Side Execution:** Engineered to handle single-page applications (SPAs), asynchronous AJAX payloads, and dynamic DOM mutations by waiting explicitly for a `networkidle` state before extraction initialization.
*   **Header Spoofing & Anti-Fingerprinting:** Utilizes context-isolated browser instances injected with deterministic browser user-agents. This minimizes footprint detection and mitigates early-stage anti-bot blocking mechanics.
*   **Robust Fault Tolerance:** Employs precise, isolated try/except error boundaries on iterative data nodes. This pattern prevents single-node processing failures or DOM structure updates from breaking the execution flow of the broader batch.
*   **Multi-Schema Data Serialization:** Incorporates dual-paradigm storage pipelines. It leverages **Pandas** to enforce relational schema consistency and export to tabular CSV formats, while simultaneously dumping data into nested, validation-ready hierarchical JSON arrays.
*   **Production-Grade Logging Structure:** Replaces raw print operations with a standardized `logging` abstraction layer tracking processing footprints, system warnings, and pipeline runtimes.

---

## 🛠️ System Prerequisites & Installation

Ensure you have Python 3.8+ installed on your local runtime environment.

1. Provision required library dependencies via pip:
```bash
pip install playwright pandas
```

2. Initialize system binaries for the underlying headless Chromium browser runtime:
```bash
playwright install
```

---

## 💻 Execution Flow

To run the automated data extraction pipeline layer, execute the core python script:

```bash
python scraper.py
```

### Output Schema Structure
Upon processing conclusion, the pipeline generates two distinct, sanitized data layers in your root directory:
*   `normalized_web_extraction.json`: Structured, nested document model detailing ingestion timestamps and accurate structural tracking values.
*   `normalized_web_extraction.csv`: Flat, relational database-ready tabular matrix.
