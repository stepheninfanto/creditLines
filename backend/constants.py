REQUIRED_PARAMETER_LIST =  ["CompanyName","Company","EBIT","NetSales" ,"CurrentAssets",
                            "CurrentLiabilities","TotalLiabilities","TotalAsset","MarketValueEquity",
                           "RetainedEarnings"]

WEIGHTS ={
   "PRIVATE":{
      "EBIT_TotalAsset_Ratio":3.107,
      "NetSales_TotalAsset_Ratio":0.998,
      "MarketValueEquity_TotalLiablility_Ratio":0.42,
      "WorkingCapital_TotalAsset_Ratio":0.717,
      "RetainedEarning_TotalAsset_Ratio":0.847
   },
"PUBLIC":{
      "EBIT_TotalAsset_Ratio":3.3,
      "NetSales_TotalAsset_Ratio":0.999,
      "MarketValueEquity_TotalLiablility_Ratio":0.6,
      "WorkingCapital_TotalAsset_Ratio":1.2,
      "RetainedEarning_TotalAsset_Ratio":1.4
   }
}


