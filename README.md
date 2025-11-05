## phone_data_analysis

phone_data_analysis is a small Python project for exploring and analyzing mobile phone data. It contains data preprocessing, trend analysis, visualization, and simple prediction utilities built around cleaned and raw mobile device datasets.

### Project layout

- `data/`
	- `raw/` — original raw CSV(s) (e.g., `mobile.csv`)
	- `preprocess/` — cleaned and intermediate CSV files (e.g., `mobile_cleaned.csv`, `mobile_final_cleaned.csv`, `mobile_launched.csv`, `mobile_upcoming_rumored.csv`)
	- `processed/` — outputs of analysis including trend and ranking CSVs (e.g., `brand_family_trends.csv`, `top_upcoming_brands_by_spec_score.csv`)
	- `figures/` — generated charts and figures

- `src/` — primary Python modules
	- `preprocess.py` — data cleaning and transformation steps
	- `data_process.py` — feature engineering and dataset preparation for analysis
	- `visualization.py` — plotting and figure creation
	- `mobile_prediction.py` — simple predictive modeling or scoring utilities

- Project root files:
	- `main.py` — project entry point / pipeline orchestrator
	- `pyproject.toml` — project metadata and dependencies

### Quick start

Run the typical pipeline (preprocess → analyze → visualize):

```powershell
python .\main.py
```

Outputs are written to `data/processed/` (CSV) and `data/figures/` (charts).

### Notes

- The repository organizes a clear pipeline from raw data to visual artifacts and lightweight predictions.
- Consider adding a short example or a minimal usage section with expected runtime and sample outputs.
