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
    # Save like GUI/CLI would
    cleaned.to_csv(out, index=False, encoding="utf-8-sig")
    reloaded = pd.read_csv(out)
    assert list(reloaded.columns) == ["name", "price"]
