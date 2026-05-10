import pandas as pd


class RiskCalculator:
    """
    Computes key credit risk metrics used in credit modeling.

    This class provides methods to estimate:
    - Probability of Default (PD)
    - Loss Given Default (LGD)
    - Exposure at Default (EAD)
    - Expected Loss (EL)

    These metrics are fundamental for risk assessment,
    pricing, and portfolio management.
    """

    def __init__(self, lgd: float = 0.45):
        """
        Initialize the RiskCalculator.

        Parameters
        ----------
        lgd : float, default=0.45
            Assumed Loss Given Default.
            Represents the proportion of exposure lost if a default occurs.
        """
        self.lgd = lgd

    def calculate_pd(self, model, X: pd.DataFrame) -> pd.Series:
        """
        Estimate the Probability of Default (PD) using a trained model.

        Parameters
        ----------
        model : object
            Trained classification model with a `predict_proba` method
            (e.g., Logistic Regression, Random Forest, XGBoost).
        X : pd.DataFrame
            Feature matrix used for prediction.

        Returns
        -------
        pd.Series
            Estimated PD values for each observation.

        Notes
        -----
        - Assumes that the model outputs probabilities where column 1
          corresponds to the probability of default.
        - Typically, PD = model.predict_proba(X)[:, 1]
        """
        return model.predict_proba(X)

    def calculate_ead(self, data: pd.DataFrame) -> pd.Series:
        """
        Estimate Exposure at Default (EAD).

        Parameters
        ----------
        data : pd.DataFrame
            Dataset containing credit-related variables.

        Returns
        -------
        pd.Series
            Estimated exposure at default.

        Notes
        -----
        - Uses the proposed monthly installment as a proxy
        for credit exposure.
        - Exposure is annualized using a 12-month horizon.
        """

        return data["pa_cuota_propuesta_mxn"] * 12

    def calculate_lgd(self, data: pd.DataFrame) -> pd.Series:
        """
        Estimate Loss Given Default (LGD).

        Parameters
        ----------
        data : pd.DataFrame
            Dataset (not directly used in this implementation).

        Returns
        -------
        pd.Series
            LGD values for each observation.

        Notes
        -----
        - This implementation assumes a constant LGD.
        - In practice, LGD may depend on collateral, seniority, or recovery rates.
        """
        return pd.Series(self.lgd, index=data.index)

    def calculate_expected_loss(self, pd: pd.Series, lgd: pd.Series, ead: pd.Series) -> pd.Series:
        """
        Compute Expected Loss (EL).

        Parameters
        ----------
        pd : pd.Series
            Probability of Default.
        lgd : pd.Series
            Loss Given Default.
        ead : pd.Series
            Exposure at Default.

        Returns
        -------
        pd.Series
            Expected Loss for each observation.

        Notes
        -----
        Expected Loss is defined as:

            EL = PD × LGD × EAD

        This metric is widely used in:
        - Credit pricing
        - Risk provisioning (e.g., IFRS 9)
        - Capital allocation (Basel framework)
        """
        return pd * lgd * ead