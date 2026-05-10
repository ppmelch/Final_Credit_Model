import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


class GeospatialRisk:
    """
    Class responsible for generating municipality-level
    geospatial risk analytics for frontend visualization.

    This class aggregates model outputs such as:
    - Predicted probability of default (PD)
    - Expected Loss (EL)
    - Approval rate

    Results are exported as a JSON file to be consumed
    by the frontend geospatial dashboard.
    """

    def build_municipality_risk(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate credit risk metrics by municipality and
        export results to a frontend JSON file.

        Parameters
        ----------
        data : pd.DataFrame
            Dataset containing municipality information,
            predicted PDs, and expected loss metrics.

        Returns
        -------
        pd.DataFrame
            Municipality-level aggregated risk metrics.
        """

        municipality_risk = data.groupby("municipio").agg({
            "predicted_pd": "mean",
            "expected_loss": "sum"
        }).reset_index()

        municipality_risk["approval_rate"] = (
            1 - municipality_risk["predicted_pd"]
        )

        output_path = FRONTEND_DIR / "risk_data.json"

        municipality_risk.to_json(
            output_path,
            orient="records",
            force_ascii=False
        )
        
        print(BASE_DIR)
        print(FRONTEND_DIR)

        return municipality_risk