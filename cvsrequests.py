import requests
from bs4 import BeautifulSoup

#STRING VARS
wr_url = 'https://cvs.com/vaccine/intake/store/cvd-schedule.html?icid=coronavirus-lp-vaccine-sd-statetool'
locdata_url = "https://www.cvs.com/Services/ICEAGPV1/immunization/1.0.0/getIMZStores"

payload="{\"requestMetaData\":{\"appName\":\"CVS_WEB\",\"lineOfBusiness\":\"RETAIL\",\"channelName\":\"WEB\",\"deviceType\":\"DESKTOP\",\"deviceToken\":\"7777\",\"apiKey\":\"a2ff75c6-2da7-4299-929d-d670d827ab4a\",\"source\":\"ICE_WEB\",\"securityType\":\"apiKey\",\"responseFormat\":\"JSON\",\"type\":\"cn-dep\"},\"requestPayloadData\":{\"selectedImmunization\":[\"CVD\"],\"distanceInMiles\":35,\"imzData\":[{\"imzType\":\"CVD\",\"ndc\":[\"59267100002\",\"59267100003\",\"59676058015\",\"80777027399\"],\"allocationType\":\"1\"}],\"searchCriteria\":{\"addressLine\":\"0\"}}}"
headers = {
  'authority': 'www.cvs.com',
  'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
  'accept': 'application/json',
  'sec-ch-ua-mobile': '?0',
  'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
  'content-type': 'application/json',
  'origin': 'https://www.cvs.com',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://www.cvs.com/vaccine/intake/store/cvd-store-select/first-dose-select',
  'accept-language': 'en-US,en;q=0.9',
  'cookie': 'aat1=on; adh_ps_pickup=on; sab_displayads=on; echomeln6=off-p0; flipp2=on; mc_home_new=off2-p0; mc_ui_ssr=off-p2; mc_videovisit=on; pivotal_forgot_password=off-p0; pivotal_sso=off-p0; ps=on; refill_chkbox_remove=off-p0; rxm=on; rxm_phone_dob=off-p1; s2c_akamaidigitizecoupon=on; s2c_beautyclub=off-p0; s2c_digitizecoupon=on; s2c_dmenrollment=off-p0; s2c_herotimer=off-p0; s2c_newcard=off-p0; s2c_papercoupon=on; s2c_persistEcCookie=on; s2c_smsenrollment=on; sftg=on; show_exception_status=on; mt.v=2.1921684230.1615660369396; _group1=quantum; gbi_visitorId=ckm82gxdz0001308ngmt1e6sd; _gcl_au=1.1.1709274272.1615660373; QuantumMetricUserID=6bb0c21a2dc40897db04972db224873e; CVPF=CT-USR; pe=p1; acctdel_v1=on; adh_new_ps=on; adh_ps_refill=on; buynow=off; dashboard_v1=off; db-show-allrx=on; disable-app-dynamics=on; disable-sac=on; dpp_cdc=off; dpp_drug_dir=off; dpp_sft=off; getcust_elastic=on; enable_imz=on; enable_imz_cvd=on; enable_imz_reschedule_instore=off; enable_imz_reschedule_clinic=off; gbi_cvs_coupons=true; ice-phr-offer=off; v3redirecton=false; mc_cloud_service=on; mc_hl7=on; memberlite=on; pauth_v1=on; pbmplaceorder=off; pbmrxhistory=on; rxdanshownba=off; rxdfixie=on; rxd_bnr=on; rxd_dot_bnr=on; rxdpromo=on; rxduan=on; rxlite=on; rxlitelob=off; rxm_demo_hide_LN=off; rxm_phdob_hide_LN=on; rxm_rx_challenge=on; s2cHero_lean6=on; sft_mfr_new=on; v2-dash-redirection=on; bm_sz=719B3A0E68A54A541CCCFA55684B4B28~YAAQZRDeFxGl7iJ4AQAA4o1nMgvdNq7glAoh9Vl2mFzporAWMlgfIT+sBflYkiTZtWAnCECBbeAHON33gqSjCpsTx6sBObGWeRz2l6JY9h+b/4/UEAjDZKeuJCudnYpMvDQlPHlp/b3xhMPdClvhvM3xlF/aTMqlxuczJDF9vfLO2iJyL1EmI2KC77ZO; gbi_sessionId=ckm9ltw7e0000308n7tmuh7x9; mt.sc=%7B%22i%22%3A1615753355724%2C%22d%22%3A%5B%5D%7D; AMCVS_06660D1556E030D17F000101%40AdobeOrg=1; AMCV_06660D1556E030D17F000101%40AdobeOrg=-330454231%7CMCIDTS%7C18700%7CMCMID%7C90407274455557336762186847061326101550%7CMCAAMLH-1616358156%7C7%7CMCAAMB-1616358156%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1615760556s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-18707%7CvVersion%7C3.1.2; s_cc=true; QuantumMetricSessionID=f7c5b5f7d3661423d5799dc9006ff259; QuantumMetricSessionLink=https://cvs.quantummetric.com/#/users/search?autoreplay=true&qmsessioncookie=f7c5b5f7d3661423d5799dc9006ff259&ts=1615710158-1615796558; akavpau_vp_www_cvs_com_vaccine_covid19=1615754384~id=6a9dab6bbb04fd3582f22cf249362c21; DG_IID=5B10E715-FC39-3636-8DF6-FF3B8EF5EA59; DG_UID=690708E5-237E-3885-97A9-2B3621D47C89; DG_ZID=CFB52D0E-5C02-38DA-976A-05046A329F56; DG_ZUID=14415988-5068-38F6-A3E3-B56EB83B6BE8; DG_HID=F60AF63C-F587-33D5-B336-7F1057A7A608; DG_SID=34.86.224.46:hSJqKoGv+M+T6oFtQkOU93qhgH7NoPHhGNjgRsXUb5s; _4c_mc_=b47c7b8d-6f3d-4273-aed9-0d9f06dda4b5; mt.cem=210201-Rx-Immunization-COVIDvax - A-Iteration; mt.mbsh=%7B%22fs%22%3A1615753357834%2C%22sf%22%3A1%2C%22lf%22%3A1615753818418%7D; akavpau_vp_www_cvs_com_vaccine=1615754467~id=545721522f6988599f72d2cb698feed9; s_sq=%5B%5BB%5D%5D; gpv_e5=cvs%7Cdweb%7Cvaccine%7Cintake%7Cstore%7Ccvd-store-select%7Crx%3A%20immunizations%3A%20first%20dose%20scheduler; gpv_p10=www.cvs.com%2Fvaccine%2Fintake%2Fstore%2Fcvd-store-select%2Ffirst-dose-select; RT="z=1&dm=cvs.com&si=c48d7a8e-882d-4b4d-9b1a-b8d4264c4103&ss=km9lts5h&sl=j&tt=wf0&bcn=%2F%2F173c5b0e.akstat.io%2F"; akavpau_www_cvs_com_general=1615754715~id=43deddbcfbdafc795d30f93ef8a97515; _abck=0865ABB7638EAD1DC9BB1ABA184B1679~0~YAAQihEgF81CXRt4AQAAlgJ2MgXeX6UHf4WVl64rVrsZMa/w8koBV0gXNPLBihhp4icsYlKTVUrL5P7VIGT6HokTkGbPQhRdVGBDJv8a6JZwfLkitCTucehLlRQsU8ao62frQI8S19kzXH2yFksP4QiVBxywWcC4I9dbK7A33+VOSvZJo1woO5KJJ2ZfBQVmW3F22F5j8niDHEKE4XNA2mQtEskJxR6XTUsvwMxcdKzjAZExXgEge6dzyzPnAUDQ7bZibuhesx/73L9K3FrQRdFW/32IaEVMUvS2MRsBkG20AFQYPEGiBR5mVb2uxR1bwxkfgEv1P3CiQTx5Ww9ziZp6KnyvkpDIUAWd1kZqzolnQ2eMaNmig/IqQk/axW76dBX/08L8oeMFrvtDy/p2ak88BoY=~-1~-1~-1; qmexp=1615756155335; utag_main=v_id:01782cdcc918001377cc60d4b13503068001406000b2a$_sn:3$_ss:0$_st:1615756155463$vapi_domain:cvs.com$_pn:6%3Bexp-session$ses_id:1615753353348%3Bexp-session; _abck=0865ABB7638EAD1DC9BB1ABA184B1679~-1~YAAQihEgF/hdXRt4AQAAgaB7MgWoDFARNLqfTWQQZa6V2Ddckeyx1XC3C+CVGzvTHHF4Wvykzy2hl03uoJYDTzQo7JgjIaburPfEd0xDng5K+cF82pjUwhe+u5TYudG7r3ODOWA/wz45J8S6vLcdxGXwAJLK18IixMSYPQZtO6RVkgKLv/1ZR9IDqT1VmirgZ8+9jMHwJMuvpYiwjKsEPzLOUemCtkR3eIRzwfbmF8q1Qx6ejNfcUPDaDs7Tsx6VR10YNI3sVO5cykVGA+jSN0v6evQFN+TVSw6tEs0OdJA5jswkJpOow5+OYgHV3G9mt6rubfe6C/giiZPiURluTYI72leAuHKux5yylhZry3po2cDac0uR9ByQH4Em2hGGPryJgzFFeSqbwKVJe/Oj9svaC4w=~0~-1~-1; bm_sz=A707328BA370A397728BDE781BC6F986~YAAQihEgF85dXRt4AQAA3JB7MgtwWOE7ZJTMuz74G0ASrbXMbVmP2SEofnpImnNXHsjiYnXnFE5ehT0uUHnpWRpv8XIiMLD2G9wWQu4Ssbqrn6hn16VN9cpNxRhMvwi5LzmA3WCMkdkj+HpWHJDHZ2Ig6oqkybvVqs1vJdDxRdwFYJMuclfhmN//noFA; pe=p1'
}
class CVSrequester:
    def __init__(self):
        self.wr_url = 'https://cvs.com/vaccine/intake/store/cvd-schedule.html?icid=coronavirus-lp-vaccine-sd-statetool'
        self.locdata_url = "https://www.cvs.com/Services/ICEAGPV1/immunization/1.0.0/getIMZStores"
        self.payload="{\"requestMetaData\":{\"appName\":\"CVS_WEB\",\"lineOfBusiness\":\"RETAIL\",\"channelName\":\"WEB\",\"deviceType\":\"DESKTOP\",\"deviceToken\":\"7777\",\"apiKey\":\"a2ff75c6-2da7-4299-929d-d670d827ab4a\",\"source\":\"ICE_WEB\",\"securityType\":\"apiKey\",\"responseFormat\":\"JSON\",\"type\":\"cn-dep\"},\"requestPayloadData\":{\"selectedImmunization\":[\"CVD\"],\"distanceInMiles\":35,\"imzData\":[{\"imzType\":\"CVD\",\"ndc\":[\"59267100002\",\"59267100003\",\"59676058015\",\"80777027399\"],\"allocationType\":\"1\"}],\"searchCriteria\":{\"addressLine\":\"0\"}}}"
        self.headers = {
            'authority': 'www.cvs.com',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'accept': 'application/json',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
            'content-type': 'application/json',
            'origin': 'https://www.cvs.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.cvs.com/vaccine/intake/store/cvd-store-select/first-dose-select',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': 'aat1=on; adh_ps_pickup=on; sab_displayads=on; echomeln6=off-p0; flipp2=on; mc_home_new=off2-p0; mc_ui_ssr=off-p2; mc_videovisit=on; pivotal_forgot_password=off-p0; pivotal_sso=off-p0; ps=on; refill_chkbox_remove=off-p0; rxm=on; rxm_phone_dob=off-p1; s2c_akamaidigitizecoupon=on; s2c_beautyclub=off-p0; s2c_digitizecoupon=on; s2c_dmenrollment=off-p0; s2c_herotimer=off-p0; s2c_newcard=off-p0; s2c_papercoupon=on; s2c_persistEcCookie=on; s2c_smsenrollment=on; sftg=on; show_exception_status=on; mt.v=2.1921684230.1615660369396; _group1=quantum; gbi_visitorId=ckm82gxdz0001308ngmt1e6sd; _gcl_au=1.1.1709274272.1615660373; QuantumMetricUserID=6bb0c21a2dc40897db04972db224873e; CVPF=CT-USR; pe=p1; acctdel_v1=on; adh_new_ps=on; adh_ps_refill=on; buynow=off; dashboard_v1=off; db-show-allrx=on; disable-app-dynamics=on; disable-sac=on; dpp_cdc=off; dpp_drug_dir=off; dpp_sft=off; getcust_elastic=on; enable_imz=on; enable_imz_cvd=on; enable_imz_reschedule_instore=off; enable_imz_reschedule_clinic=off; gbi_cvs_coupons=true; ice-phr-offer=off; v3redirecton=false; mc_cloud_service=on; mc_hl7=on; memberlite=on; pauth_v1=on; pbmplaceorder=off; pbmrxhistory=on; rxdanshownba=off; rxdfixie=on; rxd_bnr=on; rxd_dot_bnr=on; rxdpromo=on; rxduan=on; rxlite=on; rxlitelob=off; rxm_demo_hide_LN=off; rxm_phdob_hide_LN=on; rxm_rx_challenge=on; s2cHero_lean6=on; sft_mfr_new=on; v2-dash-redirection=on; bm_sz=719B3A0E68A54A541CCCFA55684B4B28~YAAQZRDeFxGl7iJ4AQAA4o1nMgvdNq7glAoh9Vl2mFzporAWMlgfIT+sBflYkiTZtWAnCECBbeAHON33gqSjCpsTx6sBObGWeRz2l6JY9h+b/4/UEAjDZKeuJCudnYpMvDQlPHlp/b3xhMPdClvhvM3xlF/aTMqlxuczJDF9vfLO2iJyL1EmI2KC77ZO; gbi_sessionId=ckm9ltw7e0000308n7tmuh7x9; mt.sc=%7B%22i%22%3A1615753355724%2C%22d%22%3A%5B%5D%7D; AMCVS_06660D1556E030D17F000101%40AdobeOrg=1; AMCV_06660D1556E030D17F000101%40AdobeOrg=-330454231%7CMCIDTS%7C18700%7CMCMID%7C90407274455557336762186847061326101550%7CMCAAMLH-1616358156%7C7%7CMCAAMB-1616358156%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1615760556s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-18707%7CvVersion%7C3.1.2; s_cc=true; QuantumMetricSessionID=f7c5b5f7d3661423d5799dc9006ff259; QuantumMetricSessionLink=https://cvs.quantummetric.com/#/users/search?autoreplay=true&qmsessioncookie=f7c5b5f7d3661423d5799dc9006ff259&ts=1615710158-1615796558; akavpau_vp_www_cvs_com_vaccine_covid19=1615754384~id=6a9dab6bbb04fd3582f22cf249362c21; DG_IID=5B10E715-FC39-3636-8DF6-FF3B8EF5EA59; DG_UID=690708E5-237E-3885-97A9-2B3621D47C89; DG_ZID=CFB52D0E-5C02-38DA-976A-05046A329F56; DG_ZUID=14415988-5068-38F6-A3E3-B56EB83B6BE8; DG_HID=F60AF63C-F587-33D5-B336-7F1057A7A608; DG_SID=34.86.224.46:hSJqKoGv+M+T6oFtQkOU93qhgH7NoPHhGNjgRsXUb5s; _4c_mc_=b47c7b8d-6f3d-4273-aed9-0d9f06dda4b5; mt.cem=210201-Rx-Immunization-COVIDvax - A-Iteration; mt.mbsh=%7B%22fs%22%3A1615753357834%2C%22sf%22%3A1%2C%22lf%22%3A1615753818418%7D; akavpau_vp_www_cvs_com_vaccine=1615754467~id=545721522f6988599f72d2cb698feed9; s_sq=%5B%5BB%5D%5D; gpv_e5=cvs%7Cdweb%7Cvaccine%7Cintake%7Cstore%7Ccvd-store-select%7Crx%3A%20immunizations%3A%20first%20dose%20scheduler; gpv_p10=www.cvs.com%2Fvaccine%2Fintake%2Fstore%2Fcvd-store-select%2Ffirst-dose-select; RT="z=1&dm=cvs.com&si=c48d7a8e-882d-4b4d-9b1a-b8d4264c4103&ss=km9lts5h&sl=j&tt=wf0&bcn=%2F%2F173c5b0e.akstat.io%2F"; akavpau_www_cvs_com_general=1615754715~id=43deddbcfbdafc795d30f93ef8a97515; _abck=0865ABB7638EAD1DC9BB1ABA184B1679~0~YAAQihEgF81CXRt4AQAAlgJ2MgXeX6UHf4WVl64rVrsZMa/w8koBV0gXNPLBihhp4icsYlKTVUrL5P7VIGT6HokTkGbPQhRdVGBDJv8a6JZwfLkitCTucehLlRQsU8ao62frQI8S19kzXH2yFksP4QiVBxywWcC4I9dbK7A33+VOSvZJo1woO5KJJ2ZfBQVmW3F22F5j8niDHEKE4XNA2mQtEskJxR6XTUsvwMxcdKzjAZExXgEge6dzyzPnAUDQ7bZibuhesx/73L9K3FrQRdFW/32IaEVMUvS2MRsBkG20AFQYPEGiBR5mVb2uxR1bwxkfgEv1P3CiQTx5Ww9ziZp6KnyvkpDIUAWd1kZqzolnQ2eMaNmig/IqQk/axW76dBX/08L8oeMFrvtDy/p2ak88BoY=~-1~-1~-1; qmexp=1615756155335; utag_main=v_id:01782cdcc918001377cc60d4b13503068001406000b2a$_sn:3$_ss:0$_st:1615756155463$vapi_domain:cvs.com$_pn:6%3Bexp-session$ses_id:1615753353348%3Bexp-session; _abck=0865ABB7638EAD1DC9BB1ABA184B1679~-1~YAAQihEgF/hdXRt4AQAAgaB7MgWoDFARNLqfTWQQZa6V2Ddckeyx1XC3C+CVGzvTHHF4Wvykzy2hl03uoJYDTzQo7JgjIaburPfEd0xDng5K+cF82pjUwhe+u5TYudG7r3ODOWA/wz45J8S6vLcdxGXwAJLK18IixMSYPQZtO6RVkgKLv/1ZR9IDqT1VmirgZ8+9jMHwJMuvpYiwjKsEPzLOUemCtkR3eIRzwfbmF8q1Qx6ejNfcUPDaDs7Tsx6VR10YNI3sVO5cykVGA+jSN0v6evQFN+TVSw6tEs0OdJA5jswkJpOow5+OYgHV3G9mt6rubfe6C/giiZPiURluTYI72leAuHKux5yylhZry3po2cDac0uR9ByQH4Em2hGGPryJgzFFeSqbwKVJe/Oj9svaC4w=~0~-1~-1; bm_sz=A707328BA370A397728BDE781BC6F986~YAAQihEgF85dXRt4AQAA3JB7MgtwWOE7ZJTMuz74G0ASrbXMbVmP2SEofnpImnNXHsjiYnXnFE5ehT0uUHnpWRpv8XIiMLD2G9wWQu4Ssbqrn6hn16VN9cpNxRhMvwi5LzmA3WCMkdkj+HpWHJDHZ2Ig6oqkybvVqs1vJdDxRdwFYJMuclfhmN//noFA; pe=p1'
            }

    def get_locations(self):
        response = requests.request("POST", url=self.locdata_url, headers=self.headers, data=self.payload)
        try:
            data = dict(response.json())
        except ValueError:
            return dict()
        success = data['responseMetaData']['statusCode'] == '0000'
        
        if success:
            location_data = dict()
            for location in data['responsePayloadData']['locations']:
                if location['addressState'] == 'MA':
                    if location['addressCityDescriptionText'] in location_data:
                        location_data[location['addressCityDescriptionText']].append(location['mfrName'])
                    else:
                        location_data[location['addressCityDescriptionText']] = [location['mfrName']]
            for location in location_data:
                location_data[location] = ', '.join(x for x in list(set(location_data[location])))   
            print(location_data)
            return location_data
        else:
            return dict()

    def get_wr_status(self):
        response = requests.get(self.wr_url)
        soup = BeautifulSoup(response._content, 'html.parser')
        title = soup.find('title').string
        if title == 'Immunization intake form':
            status = 'DISABLED'
        else:
            status = 'ENABLED'
        return status

        
    
 

