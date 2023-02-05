"""Utility functions for calculating summary statistics."""

def get_values(df):
    """Calculates the summary statistics for the given set of points

    Args:
        df (pd.DataFrame): A ``DataFrame`` with ``x`` and ``y`` columns

    Returns:
        list: ``[x-mean, y-mean, x-stdev, y-stdev, correlation]``
    """
    xm = df.x.mean()
    ym = df.y.mean()
    xsd = df.x.std()
    ysd = df.y.std()
    pc = df.corr().x.y

    return [xm, ym, xsd, ysd, pc]