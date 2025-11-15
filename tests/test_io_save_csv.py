import pandas as pd
from modules.pipeline_manager import PipelineManager


def test_save_and_reload_csv(tmp_path):
    p = tmp_path / "sample.csv"
    # Create a simple dataframe similar to scrape file
    df = pd.DataFrame({"name": ["A,B"], "price": [100]})
    df.to_csv(p, index=False)

    pm = PipelineManager()
    # Build minimal pipeline: no steps
    pm.build_pipeline(core_keys=[], custom_keys=[])
    cleaned = df
    out = tmp_path / "out.csv"
    # Save like GUI/CLI/GUI would: with BOM and an Excel preamble to help Excel detect comma delimiter
    with open(out, "w", encoding="utf-8-sig", newline="") as f:
        f.write("sep=,\n")
        cleaned.to_csv(f, index=False)

    # Pandas won't automatically skip the Excel sep preamble; simulate reading by skipping preamble
    reloaded = pd.read_csv(out, skiprows=1)
    assert list(reloaded.columns) == ["name", "price"]

    # The GUI/CLI also writes an XLSX fallback - check it was created and round-trips
    from modules.save_to_excel import process as save_to_excel_process

    xlsx_path = out.with_suffix(".xlsx")
    save_to_excel_process(cleaned, output_file=str(xlsx_path))
    reloaded_xlsx = pd.read_excel(xlsx_path)
    assert list(reloaded_xlsx.columns) == ["name", "price"]
