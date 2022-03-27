from constants import *

def ZScore(financia_data:dict) -> float:

    """
    CurrentAssets: Value of currently available assets (Liquid assets)
    CurrentLiabilities: Value of currently available Liabilities
    TotalLiabilities: Value of total Liabilities
    EBIT: Earnings before interest and taxes
    TotalAssets: Value of total Assets
    NetSales: Total Value earned from Sales
    RetainedEarnings: Earnings retained from the Earnings
    BookValueOfEquity: Cash after sale of the company's assets - existing liabilities
    """
    print(f"Calling {ZScore.__name__}")
    A = (financia_data["EBIT"]/financia_data["TotalAsset"]) * WEIGHTS[financia_data["Company"]]["EBIT_TotalAsset_Ratio"]
    B = (financia_data["NetSales"]/financia_data["TotalAsset"]) *  WEIGHTS[financia_data["Company"]]["NetSales_TotalAsset_Ratio"]
    C = (financia_data["MarketValueEquity"]/financia_data["TotalLiabilities"]) * WEIGHTS[financia_data["Company"]]["MarketValueEquity_TotalLiablility_Ratio"]
    D = ((financia_data["CurrentAssets"]-financia_data["CurrentLiabilities"])/financia_data["TotalAsset"]) * WEIGHTS[financia_data["Company"]]["WorkingCapital_TotalAsset_Ratio"]
    E = (financia_data["RetainedEarnings"]/financia_data["TotalAsset"]) * WEIGHTS[financia_data["Company"]]["RetainedEarning_TotalAsset_Ratio"]
    z_score = A + B + C + D +E
    ZScore_calculation = {
            "EBIT_TotalAsset_Ratio": A,
            "MarketValueEquity_TotalLiablility_Ratio": B,
            "NetSales_TotalAsset_Ratio": C,
            "RetainedEarning_TotalAsset_Ratio": D,
            "WorkingCapital_TotalAsset_Ratio": E,
            "ZScore" : z_score
        }
    print(A in range(-4,8))
    finance_data = {"financial_data": {"EBIT_TotalAsset_Ratio": (A.__gt__(-4) and A.__lt__(8)), "NetSales_TotalAsset_Ratio": (B.__gt__(-4) and B.__lt__(8)),
     "MarketValueEquity_TotalLiablility_Ratio": (C.__gt__(-4) and C.__lt__(8)), "WorkingCapital_TotalAsset_Ratio": (D.__gt__(-4) and D.__lt__(8)),
     "RetainedEarning_TotalAsset_Ratio": (E.__gt__(-4) and E.__lt__(8))},"credit_worth": z_score.__ge__(2.7)}
    data = {"ZScore_calculation":ZScore_calculation, "finance_data":finance_data}
    return  data