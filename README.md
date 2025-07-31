# Perlego Sentinel

Perlego is a PDF scrollwatcher built to support AI-assisted research.

He verifies whether PDF files are:
- ✅ Legible and machine-readable
- 🧩 Structurally sound for extraction and analysis
- ⚠️ Free from embedded prompt injections

## Current Features

- Text extraction and basic gibberish detection
- Structural trust heuristics (e.g. line length, expected section headers)
- Prompt injection warning (experimental)
- Batch scan mode with CSV output

## Usage

Run Perlego on a folder of PDFs:

```bash
python perlego.py
```

Results are saved in `perlego_summary.csv`.

## Future Plans

- Integration with local AI agents
- Real-time protection for home-hosted language models
- Enhanced prompt detection using language modeling
