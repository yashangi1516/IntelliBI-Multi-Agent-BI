"""Lightweight specialist agents used by the IntelliBI orchestrator."""
import pandas as pd

def _numeric_columns(df):
    return list(df.select_dtypes(include="number").columns)

def data_analyst_agent(df):
    return {
        "agent": "Data Analyst",
        "finding": f"The dataset contains {len(df):,} records and {len(df.columns)} fields.",
        "details": {
            "missing_values": int(df.isna().sum().sum()),
            "duplicate_rows": int(df.duplicated().sum()),
            "numeric_columns": _numeric_columns(df),
        },
    }

def sales_agent(df):
    numeric = _numeric_columns(df)
    revenue_col = next((c for c in numeric if "revenue" in str(c).lower() or "sales" in str(c).lower()), None)
    if revenue_col:
        total = float(df[revenue_col].fillna(0).sum())
        average = float(df[revenue_col].fillna(0).mean())
        finding = f"Total {revenue_col}: {total:,.2f}; average per row: {average:,.2f}."
    else:
        finding = "No obvious revenue or sales column was detected. Review numeric fields to identify a sales measure."
    return {"agent": "Sales Agent", "finding": finding}

def finance_agent(df):
    numeric = _numeric_columns(df)
    cost_col = next((c for c in numeric if "cost" in str(c).lower() or "expense" in str(c).lower()), None)
    revenue_col = next((c for c in numeric if "revenue" in str(c).lower() or "sales" in str(c).lower()), None)
    if cost_col and revenue_col:
        revenue = float(df[revenue_col].fillna(0).sum())
        cost = float(df[cost_col].fillna(0).sum())
        profit = revenue - cost
        finding = f"Estimated profit is {profit:,.2f} (revenue {revenue:,.2f} minus cost {cost:,.2f})."
    else:
        finding = "Revenue and cost columns were not both detected; profitability could not be estimated."
    return {"agent": "Financial Agent", "finding": finding}

def marketing_agent(df):
    categorical = [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c])]
    if categorical:
        col = categorical[0]
        top = df[col].astype(str).value_counts().head(3).to_dict()
        finding = f"Most frequent values in '{col}': " + ", ".join(f"{k} ({v})" for k, v in top.items())
    else:
        finding = "No categorical field was found for a basic segment overview."
    return {"agent": "Marketing Agent", "finding": finding}

def visualization_agent(df):
    numeric = _numeric_columns(df)
    return {
        "agent": "Visualization Agent",
        "finding": f"Suggested numeric measures for charts: {', '.join(map(str, numeric[:5])) or 'none detected'}.",
        "numeric_columns": numeric,
    }

def report_agent(results):
    return {
        "agent": "Report Agent",
        "finding": "The specialist agents completed a first-pass review. Validate column meanings and business context before acting.",
        "sections": [item["agent"] for item in results],
    }

def decision_agent(results):
    recommendations = [
        "Investigate missing and duplicate records before using the data for formal reporting.",
        "Compare performance across meaningful categories such as product, region, or month when those fields exist.",
        "Confirm that monetary fields use the same currency and time period before comparing totals.",
    ]
    return {"agent": "Decision Agent", "recommendations": recommendations}

def run_all_agents(df):
    results = [
        data_analyst_agent(df),
        sales_agent(df),
        finance_agent(df),
        marketing_agent(df),
        visualization_agent(df),
    ]
    results.append(report_agent(results))
    results.append(decision_agent(results))
    return {
        "orchestrator": "AI Orchestrator",
        "message": "All available specialist agents have completed their analysis.",
        "agents": results,
    }
