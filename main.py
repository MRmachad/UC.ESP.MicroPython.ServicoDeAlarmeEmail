from acessWifi_alr import AcessWifi_alr
from acessServe_alr import AcessServe_alr

from machine import Pin, ADC, I2C
import json

import time



ADC_SENSOR = ADC(Pin(36))

ADC_SENSOR.atten(ADC.ATTN_11DB)                           # 0 - 3.3V 16bits

ADDR_ADC = 0x48


R_DATA_ADC_Conversion_register = 0
R_DATA_ADC_Config_register = 1
R_DATA_ADC_Lo_thresh_register = 2 
R_DATA_ADC_Hi_thresh_register = 3

adcEsp_InputRange = 3.3
ads_InputRange = 6.144
ADC_16BIT_MAX  = 65536
ADCESP_16BIT_MAX  = 4096

Faixa_de_amp = 2.5
range_de_temperatura = 100


adcEsp_bit_Voltage = (adcEsp_InputRange) / (ADCESP_16BIT_MAX - 1)
ads_bit_Voltage = (ads_InputRange * 2) / (ADC_16BIT_MAX - 1)
Voltage_Temp = range_de_temperatura/Faixa_de_amp


TX_RX_SERIAL_ADC = I2C( sda=Pin(12), scl=Pin(13), freq=5000)

def config(dataMSB, dataLSB):
    
    print(dataMSB, dataLSB)
    
    vector_bytes = [bytes([R_DATA_ADC_Config_register]),bytes([dataMSB]),bytes([dataLSB])]
    
    TX_RX_SERIAL_ADC.writevto(ADDR_ADC, vector_bytes) 
    
    
    auxData = TX_RX_SERIAL_ADC.readfrom_mem(ADDR_ADC, R_DATA_ADC_Config_register, 3)
    dado_enviado = auxData[0] << 8 | auxData[1]
    print(auxData[0], auxData[1], auxData[2])
    print("config", dado_enviado)
    
def twos_comp(val):
        bits = 16
        if (val & (1 << (bits - 1))) != 0:
            val = val - (1 << bits)
        return val

##X100 0000 1000 0011 = 283h = 131   fundo em 6.144


if __name__ == '__main__':
    
    config(112, 131)
    
    print("COMEÇOU")
    
    ob_acessWifi = AcessWifi_alr(sd = "acess", passw = "12345678")
    
    ob_acessWifi.do_connect_STA()
    
    ob_acessServe = AcessServe_alr(host = "192.168.76.227")
    
    temp_Alerta = 1000
    
    aux = {}
    DataACC = {}
    
    ##Sinal vindo de 0 a 2.5
    while(1):

        time.sleep(1)
        auxData = TX_RX_SERIAL_ADC.readfrom_mem(ADDR_ADC, R_DATA_ADC_Conversion_register, 2)
        
        AD_DS = (twos_comp(auxData[0] << 8 | auxData[1]) * ads_bit_Voltage) 
        AD_esp = (ADC_SENSOR.read() * adcEsp_bit_Voltage) 
        print("VOLT DS: ", AD_DS)
        print("VOLT ES: ", AD_esp)
        
        temp_esp = AD_esp * Voltage_Temp
        temp_ds = AD_DS * Voltage_Temp
        print("\n","TEMP DS: ", temp_ds)
        print("TEMP ES: ", temp_esp, "\n")
        
        
        ##################
        guard_esp = open(("Tensão_esp"+".csv"), 'a')
        guard_ad = open(("Tensão_ad"+".csv"), 'a')
        
        guard_esp.write( str(AD_esp).replace(".",",") + "\n")
        guard_ad.write( str(AD_DS).replace(".",",") + "\n")
        
        guard_esp.close()
        guard_ad.close()
        ##################
        
        
        if (temp_ds) > temp_Alerta:
            
            aux = { "AD_DS" : str(AD_DS)}
            DataACC.update(aux)

            aux = { "AD_esp" : str(AD_esp)}
            DataACC.update(aux)
            
            print(json.dumps(DataACC))
            
            ob_acessServe.envia_servico(json.dumps(DataACC))
            
            
            

                                
        
   

