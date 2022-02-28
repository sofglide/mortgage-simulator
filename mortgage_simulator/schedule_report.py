"""
report generation
"""
from typing import Any, Dict, List

from terminaltables import DoubleTable


class ScheduleReport:
    """
    Simulation report generator
    """

    def __init__(self, data: Dict[str, List[Any]]):
        self.data = _reformat_data(data)

    def get_report(self) -> str:
        """
        Get report
        :return:
        """

        rows = [list(self.data.keys())]
        for i in range(len(self.data["month"])):
            rows.append([self.data[k][i] for k in rows[0]])
        report_table = DoubleTable(rows)

        for i in range(1, len(rows)):
            report_table.justify_columns[i] = "right"

        return report_table.table


def _reformat_data(data: Dict[str, Any]) -> Dict[str, List[str]]:
    data_f = dict()
    data_f["year"] = [f"{y:-2}" for y in data["year"]]
    data_f["month"] = [f"{m:-2}" for m in data["month"]]
    data_f["debt ratio"] = [f"{r:.2f} %" for r in data["debt ratio"]]
    data_f["month interest"] = [f"{round(mi):,}" for mi in data["month interest"]]
    data_f["month amortization"] = [f"{round(mi):,}" for mi in data["month amortization"]]
    data_f["remaining loan"] = [f"{round(r):,}" for r in data["remaining loan"]]
    data_f["total paid"] = [f"{round(t):,}" for t in data["total paid"]]
    data_f["total interest paid"] = [f"{round(i):,}" for i in data["total interest paid"]]
    data_f["total amortized"] = [f"{round(t):,}" for t in data["total amortized"]]
    data_f["total tax return"] = [f"{round(t):,}" for t in data["total tax return"]]
    return data_f
