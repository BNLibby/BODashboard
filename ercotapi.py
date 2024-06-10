
# Imports
from requests import post
from requests import get
from inspect import getargvalues, currentframe

# Test Username/Password/API Key
USERNAME = "subscription.p86l8@passmail.net"
PASSWORD = "wKcWp70t6EuJtqYxUGxWYKBuk4b6C1727YGqPf7Qtu0yCNA7bhtcsVzJFpdPa3jY"
API_KEY = "3a5ddfc6c73f4c51b487632c3bce762b"

class ERCOTAPI:
    def __init__(self, username:str, password:str, api_key:str):
        # ERCOTAPI Token Retrieval Parameters
        self.username:str = username
        self.password:str = password
        self.api_key:str = api_key
        self.token_link_start = "https://ercotb2c.b2clogin.com/ercotb2c.onmicrosoft.com/B2C_1_PUBAPI-ROPC-FLOW/oauth2/v2.0/token"
        self.token_link_end = "&grant_type=password&scope=openid+fec253ea-0d06-4272-a5e6-b478baeecd70+offline_access&client_id=fec253ea-0d06-4272-a5e6-b478baeecd70&response_type=id_token"

        # Retrieve Id Token/Set Generic Authentication Header
        self.access_token = self.get_access_token()
        self.authentication_header = {"authorization": "Bearer " + self.access_token, "Ocp-Apim-Subscription-Key": self.api_key}

        # Test API Connection
        if self.test_connection().status_code == 200:
            print("> Connected To API\n")
            return None
        else:
            print("> Not Connected To API: Check Username/Password/API Key\n")
            return None

    def test_connection(self):
        return get("https://api.ercot.com/api/public-reports/np4-190-cd/dam_stlmnt_pnt_prices?deliveryDateFrom=2024-01-01&deliveryDateTo=2024-01-02",
                   headers=self.authentication_header, verify=False)
    
    def get_json_dict(self, rq_data):
        return rq_data.json()
    
    def get_access_token(self):
        return post(self.token_link_start+"?username="+self.username+"&password="+self.password+self.token_link_end, verify=False).json()["id_token"]

    def get_json(self, link:str, params:dict):
        rq_link = link + "?"
        for param in params.keys():
            if params[param] != None:
                rq_link = rq_link + param + "=" + params[param] + "&"
        return get(rq_link[:-1], headers=self.authentication_header, verify=False)

    def get_dam_spp(self, deliveryDateFrom:str = None, deliveryDateTo:str = None, hourEnding:str = None, settlementPoint:str = None,
                    settlementPointPriceFrom:str = None, settlementPointPriceTo:str = None, DSTFlag:str = None):
        base_link:str = "https://api.ercot.com/api/public-reports/np4-190-cd/dam_stlmnt_pnt_prices"
        params = getargvalues(currentframe())[3]
        params.pop("self")
        params.pop("base_link")
        return self.get_json(base_link, params)
   
    def get_dam_shadow_prices(self, deliveryDateFrom:str = None, deliveryDateTo:str = None, hourEnding:str = None, constraintIdFrom:str = None,
                             constraintIdTo:str = None, constraintName:str = None, contingencyName:str = None, constraintLimitFrom:str = None,
                             constraintLimitTo:str = None, constraintValueFrom:str = None, constraintValueTo:str = None, violationAmountFrom:str = None,
                             violationAmountTo:str = None, shadowPriceFrom:str = None, shadowPriceTo:str = None, fromStation:str = None, toStation:str = None, fromStationkVFrom:str = None,
                             fromStationkVTo:str = None, toStationkVFrom:str = None, toStationkVTo:str = None, deliveryTimeFrom:str = None, deliveryTimeTo:str = None, DSTFlag:str = None):
        base_link:str = "https://api.ercot.com/api/public-reports/np4-191-cd/dam_shadow_prices"
        params = getargvalues(currentframe())[3]
        params.pop("self")
        params.pop("base_link")
        return self.get_json(base_link, params)
                        
    def get_dam_system_lambda(self, deliveryDateFrom:str = None, deliveryDateTo:str = None, hourEnding:str = None, systemLambdaFrom:str = None, systemLambdaTo:str = None, DSTFlag:str = None):
        base_link:str = "https://api.ercot.com/api/public-reports/np4-523-cd/dam_system_lambda"
        params = getargvalues(currentframe())[3]
        params.pop("self")
        params.pop("base_link")
        return self.get_json(base_link, params)
    
    def get_rtm_sced_shadow(self,fromStation:str = None,toStation:str = None,fromStationkVFrom:str = None,fromStationkVTo:str = None,toStationkVFrom:str = None,
                           toStationkVTo:str = None,CCTStatus:str = None,SCEDTimestampFrom:str = None,SCEDTimestampTo:str = None,repeatedHourFlag:str = None,
                           constraintIDFrom:str = None,constraintIDTo:str = None,constraintName:str = None,contingencyName:str = None,shadowPriceFrom:str = None,
                           shadowPriceTo:str = None,maxShadowPriceFrom:str = None,maxShadowPriceTo:str = None,limitFrom:str = None,limitTo:str = None,valueFrom:str = None,
                           valueTo:str = None,violatedMWFrom:str = None,violatedMWTo:str = None):
        base_link:str = "https://api.ercot.com/api/public-reports/np6-86-cd/shdw_prices_bnd_trns_const"
        params = getargvalues(currentframe())[3]
        params.pop("self")
        params.pop("base_link")
        return self.get_json(base_link, params)
    
    def get_rtm_sced_lambda(self, SCEDTimestampFrom:str = None, SCEDTimestampTo:str = None, repeatHourFlag:str = None, systemLambdaFrom:str = None, systemLambdaTo:str = None):
        base_link:str = "https://api.ercot.com/api/public-reports/np6-322-cd/sced_system_lambda"
        params = getargvalues(currentframe())[3]
        params.pop("self")
        params.pop("base_link")
        return self.get_json(base_link, params)
    
    def get_rtm_spp(self, deliveryDateFrom:str = None, deliveryDateTo:str = None, deliveryHourFrom:str = None, deliveryHourTo:str = None, deliveryIntervalFrom:str = None,
                   deliveryIntervalTo:str = None, settlementPoint:str = None, settlementPointType:str = None, settlementPointPriceFrom:str = None,
                   settlementPointPriceTo:str = None, DSTFlag:str = None):
        base_link:str = "https://api.ercot.com/api/public-reports/np6-905-cd/spp_node_zone_hub"
        params = getargvalues(currentframe())[3]
        params.pop("self")
        params.pop("base_link")
        return self.get_json(base_link, params)

    def get_7day_load_studyarea(self, deliveryDateFrom:str = None, deliveryDateTo:str = None, hourEnding:str = None, valleyFrom:str = None,
                               valleyTo:str = None, model:str = None, DSTFlag:str = None, postedDatetimeFrom:str = None, postedDatetimeTo:str = None):
        base_link:str = "https://api.ercot.com/api/public-reports/np3-566-cd/lf_by_model_study_area"
        params = getargvalues(currentframe())[3]
        params.pop("self")
        params.pop("base_link")
        return self.get_json(base_link, params)
    
    def get_7day_load_weatherzone(self, DSTFlag:str = None, deliveryDateFrom:str = None, deliveryDateTo:str = None, hourEnding:str = None, coastFrom:str = None, coastTo:str = None,
                                 eastFrom:str = None, eastTo:str = None, farWestFrom:str = None, farWestTo:str = None, northFrom:str = None, northTo:str = None, northCentralFrom:str = None, 
                                 northCentralTo:str = None, southCentralFrom:str = None, southCentralTo:str = None, southernFrom:str = None, southernTo:str = None, postedDatetimeFrom:str = None, 
                                 postedDatetimeTo:str = None, westFrom:str = None, westTo:str = None, systemTotalFrom:str = None, systemTotalTo:str = None, model:str = None, inUseFlag:str = None):
        base_link:str = "https://api.ercot.com/api/public-reports/np3-565-cd/lf_by_model_weather_zone"
        params = getargvalues(currentframe())[3]
        params.pop("self")
        params.pop("base_link")
        return self.get_json(base_link, params)

    def get_solar_production_geo(self, deliveryDateFrom:str = None, deliveryDateTo:str = None, postedDatetimeFrom:str = None, postedDatetimeTo:str = None, hourEndingFrom:str = None,
                                hourEndingTo:str = None, genSystemWideFrom:str = None, genSystemWideTo:str = None, COPHSLSystemWideFrom:str = None, COPHSLSystemWideTo:str = None,
                                STPPFSystemWideFrom:str = None, STPPFSystemWideTo:str = None, PVGRPPSystemWideTo:str = None, genCenterWestFrom:str = None, genCenterWestTo:str = None,
                                COPHSLCenterWestFrom:str = None, COPHSLCenterWestTo:str = None, STPPFCenterWestFrom:str = None, STPPFCenterWestTo:str = None, PVGRPPCenterWestFrom:str = None,
                                PVGRPPCenterWestTo:str = None, genNorthWestFrom:str = None, genNorthWestTo:str = None, COPHSLNorthWestFrom:str = None, COPHSLNorthWestTo:str = None,
                                STPPFNorthWestFrom:str = None, STPPFNorthWestTo:str = None, PVGRPPNorthWestFrom:str = None, PVGRPPNorthWestTo:str = None, genFarWestFrom:str = None,
                                genFarWestTo:str = None, COPHSLFarWestFrom:str = None, COPHSLFarWestTo:str = None, STPPFFarWestFrom:str = None, STPPFFarWestTo:str = None, PVGRPPFarWestFrom:str = None,
                                PVGRPPFarWestTo:str = None, genFarEastFrom:str = None, genFarEastTo:str = None, COPHSLFarEastFrom:str = None, COPHSLFarEastTo:str = None, STPPFFarEastFrom:str = None,
                                STPPFFarEastTo:str = None, PVGRPPFarEastFrom:str = None, PVGRPPFarEastTo:str = None, genSouthEastFrom:str = None, genSouthEastTo:str = None, COPHSLSouthEastFrom:str = None,
                                COPHSLSouthEastTo:str = None, STPPFSouthEastFrom:str = None, STPPFSouthEastTo:str = None, PVGRPPSouthEastFrom:str = None, PVGRPPSouthEastTo:str = None,
                                genCenterEastFrom:str = None, genCenterEastTo:str = None, COPHSLCenterEastFrom:str = None, COPHSLCenterEastTo:str = None, STPPFCenterEastFrom:str = None,
                                STPPFCenterEastTo:str = None, PVGRPPCenterEastFrom:str = None, PVGRPPCenterEastTo:str = None, DSTFlag:str = None):
        base_link:str = "https://api.ercot.com/api/public-reports/np4-745-cd/spp_hrly_actual_fcast_geo"
        params = getargvalues(currentframe())[3]
        params.pop("self")
        params.pop("base_link")
        return self.get_json(base_link, params)
    
    def get_wind_production_geo(self, deliveryDateFrom:str = None, deliveryDateTo:str = None, hourEndingFrom:str = None, hourEndingTo:str = None, actualSystemWideFrom:str = None, actualSystemWideTo:str = None,
                               COPHSLSystemWideFrom:str = None, COPHSLSystemWideTo:str = None, STWPFSystemWideFrom:str = None, STWPFSystemWideTo:str = None, WGRPPSystemWideFrom:str = None,
                               WGRPPSystemWideTo:str = None, actualPanhandleFrom:str = None, actualPanhandleTo:str = None, COPHSLPanhandleFrom:str = None, COPHSLPanhandleTo:str = None,
                               STWPFPanhandleFrom:str = None, STWPFPanhandleTo:str = None, WGRPPPanhandleFrom:str = None, WGRPPPanhandleTo:str = None, actualCoastalFrom:str = None, actualCoastalTo:str = None,
                               COPHSLCoastalFrom:str = None, COPHSLCoastalTo:str = None, STWPFCoastalFrom:str = None, STWPFCoastalTo:str = None, WGRPPCoastalFrom:str = None, WGRPPCoastalTo:str = None,
                               actualSouthFrom:str = None, actualSouthTo:str = None, COPHSLSouthFrom:str = None, COPHSLSouthTo:str = None, STWPFSouthFrom:str = None, STWPFSouthTo:str = None, WGRPPSouthFrom:str = None,
                               WGRPPSouthTo:str = None, actualWestFrom:str = None, actualWestTo:str = None, COPHSLWestFrom:str = None, COPHSLWestTo:str = None, STWPFWestFrom:str = None, STWPFWestTo:str = None,
                               WGRPPWestFrom:str = None, WGRPPWestTo:str = None, actualNorthFrom:str = None, actualNorthTo:str = None, COPHSLNorthFrom:str = None, COPHSLNorthTo:str = None, STWPFNorthFrom:str = None, STWPFNorthTo:str = None,
                               WGRPPNorthFrom:str = None, WGRPPNorthTo:str = None, DSTFlag:str = None, postedDatetimeFrom:str = None, postedDatetimeTo:str = None):
        base_link:str = "https://api.ercot.com/api/public-reports/np4-742-cd/wpp_hrly_actual_fcast_geo"
        params = getargvalues(currentframe())[3]
        params.pop("self")
        params.pop("base_link")
        return self.get_json(base_link, params)

    def get_solar_production_sys(self, STPPFSystemWideFrom:str = None, STPPFSystemWideTo:str = None, PVGRPPSystemWideFrom:str = None, PVGRPPSystemWideTo:str = None,
                                DSTFlag:str = None, deliveryDateFrom:str = None, deliveryDateTo:str = None, hourEndingFrom:str = None, hourEndingTo:str = None,
                                actualSystemWideFrom:str = None, actualSystemWideTo:str = None, COPHSLSystemWideFrom:str = None, COPHSLSystemWideTo:str = None,
                                postedDatetimeFrom:str = None, postedDatetimeTo:str = None):
        base_link:str = "https://api.ercot.com/api/public-reports/np4-737-cd/spp_hrly_avrg_actl_fcast"
        params = getargvalues(currentframe())[3]
        params.pop("self")
        params.pop("base_link")
        return self.get_json(base_link, params)

    def get_wind_production_sys(self, WGRPPLoadZoneNorthFrom:str = None, WGRPPLoadZoneNorthTo:str = None, DSTFlag:str = None, postedDatetimeFrom:str = None, postedDatetimeTo:str = None, 
                               deliveryDateFrom:str = None, deliveryDateTo:str = None, hourEndingFrom:str = None, hourEndingTo:str = None, actualSystemWideFrom:str = None, 
                               actualSystemWideTo:str = None, COPHSLSystemWideFrom:str = None, COPHSLSystemWideTo:str = None, STWPFSystemWideFrom:str = None, 
                               STWPFSystemWideTo:str = None, WGRPPSystemWideFrom:str = None, WGRPPSystemWideTo:str = None, actualLoadZoneSouthHoustonFrom:str = None, 
                               actualLoadZoneSouthHoustonTo:str = None, COPHSLLoadZoneSouthHoustonFrom:str = None, COPHSLLoadZoneSouthHoustonTo:str = None, 
                               STWPFLoadZoneSouthHoustonFrom:str = None, STWPFLoadZoneSouthHoustonTo:str = None, WGRPPLoadZoneSouthHoustonFrom:str = None, 
                               WGRPPLoadZoneSouthHoustonTo:str = None, actualLoadZoneWestFrom:str = None, actualLoadZoneWestTo:str = None, COPHSLLoadZoneWestFrom:str = None, 
                               COPHSLLoadZoneWestTo:str = None, STWPFLoadZoneWestFrom:str = None, STWPFLoadZoneWestTo:str = None, WGRPPLoadZoneWestFrom:str = None, WGRPPLoadZoneWestTo:str = None, 
                               actualLoadZoneNorthFrom:str = None, actualLoadZoneNorthTo:str = None, COPHSLLoadZoneNorthFrom:str = None, COPHSLLoadZoneNorthTo:str = None, 
                               STWPFLoadZoneNorthFrom:str = None, STWPFLoadZoneNorthTo:str = None):
        base_link:str = "https://api.ercot.com/api/public-reports/np4-732-cd/wpp_hrly_avrg_actl_fcast"
        params = getargvalues(currentframe())[3]
        params.pop("self")
        params.pop("base_link")
        return self.get_json(base_link, params)

    def set_api_connection(self):
        self.access_token = self.get_access_token()
        self.authentication_header = {"authorization": "Bearer " + self.access_token, "Ocp-Apim-Subscription-Key": self.api_key}
        
        # Test API Connection
        if self.test_connection().status_code == 200:
            print("> Connected To API\n")
            return True
        else:
            print("> Not Connected To API: Username/Password/API Key\n")
            return False