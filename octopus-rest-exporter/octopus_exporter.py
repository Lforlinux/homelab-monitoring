#!/usr/bin/env python3

import os
import time
import requests
import json
from datetime import datetime, timedelta
from prometheus_client import start_http_server, Gauge, Counter, Info
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prometheus metrics
electric_consumption = Gauge('octopus_electric_consumption_kwh', 'Electric consumption in kWh', ['meter_serial'])
gas_consumption = Gauge('octopus_gas_consumption_kwh', 'Gas consumption in kWh', ['meter_serial'])
electric_unit_rate = Gauge('octopus_electric_unit_rate_pence', 'Electric unit rate in pence per kWh')
gas_unit_rate = Gauge('octopus_gas_unit_rate_pence', 'Gas unit rate in pence per kWh')
electric_standing_charge = Gauge('octopus_electric_standing_charge_pence', 'Electric standing charge in pence per day')
gas_standing_charge = Gauge('octopus_gas_standing_charge_pence', 'Gas standing charge in pence per day')
tariff_info = Info('octopus_tariff', 'Current tariff information')

class OctopusExporter:
    def __init__(self):
        self.api_key = os.getenv('OCTOPUS_API_KEY')
        self.account_number = os.getenv('OCTOPUS_ACCOUNT_NUMBER')
        self.electric_mpan = os.getenv('OCTOPUS_ELECTRIC_MPAN')
        self.gas_mprn = os.getenv('OCTOPUS_GAS_MPRN')
        self.electric_serial = os.getenv('OCTOPUS_ELECTRIC_SERIAL')
        self.gas_serial = os.getenv('OCTOPUS_GAS_SERIAL')
        
        if not all([self.api_key, self.account_number]):
            raise ValueError("OCTOPUS_API_KEY and OCTOPUS_ACCOUNT_NUMBER are required")
        
        self.session = requests.Session()
        self.session.auth = (self.api_key, '')
    
    def get_account_info(self):
        """Get account information to find MPAN/MPRN if not provided"""
        try:
            url = f"https://api.octopus.energy/v1/accounts/{self.account_number}/"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get account info: {e}")
            return None
    
    def get_electric_consumption(self):
        """Get electric consumption data"""
        if not self.electric_mpan or not self.electric_serial:
            logger.warning("Electric MPAN or serial not provided, skipping electric consumption")
            return
        
        try:
            url = f"https://api.octopus.energy/v1/electricity-meter-points/{self.electric_mpan}/meters/{self.electric_serial}/consumption/"
            response = self.session.get(url, params={'page_size': 1})
            response.raise_for_status()
            data = response.json()
            
            if data['results']:
                latest = data['results'][0]
                consumption = latest['consumption']
                electric_consumption.labels(meter_serial=self.electric_serial).set(consumption)
                logger.info(f"Electric consumption: {consumption} kWh")
        except Exception as e:
            logger.error(f"Failed to get electric consumption: {e}")
    
    def get_gas_consumption(self):
        """Get gas consumption data"""
        if not self.gas_mprn or not self.gas_serial:
            logger.warning("Gas MPRN or serial not provided, skipping gas consumption")
            return
        
        try:
            url = f"https://api.octopus.energy/v1/gas-meter-points/{self.gas_mprn}/meters/{self.gas_serial}/consumption/"
            response = self.session.get(url, params={'page_size': 1})
            response.raise_for_status()
            data = response.json()
            
            if data['results']:
                latest = data['results'][0]
                consumption = latest['consumption']
                gas_consumption.labels(meter_serial=self.gas_serial).set(consumption)
                logger.info(f"Gas consumption: {consumption} kWh")
        except Exception as e:
            logger.error(f"Failed to get gas consumption: {e}")
    
    def get_tariff_rates(self):
        """Get current tariff rates"""
        try:
            # Get account info to find current tariffs
            account_info = self.get_account_info()
            if not account_info:
                return
            
            # Get electric tariff
            if 'electricity_supply_points' in account_info:
                for supply_point in account_info['electricity_supply_points']:
                    if 'tariff_code' in supply_point:
                        tariff_code = supply_point['tariff_code']
                        self.get_electric_tariff(tariff_code)
                        break
            
            # Get gas tariff
            if 'gas_supply_points' in account_info:
                for supply_point in account_info['gas_supply_points']:
                    if 'tariff_code' in supply_point:
                        tariff_code = supply_point['tariff_code']
                        self.get_gas_tariff(tariff_code)
                        break
                        
        except Exception as e:
            logger.error(f"Failed to get tariff rates: {e}")
    
    def get_electric_tariff(self, tariff_code):
        """Get electric tariff details"""
        try:
            url = f"https://api.octopus.energy/v1/products/{tariff_code}/electricity-tariffs/E-1R-{tariff_code}-E/standard-unit-rates/"
            response = self.session.get(url, params={'page_size': 1})
            response.raise_for_status()
            data = response.json()
            
            if data['results']:
                latest = data['results'][0]
                unit_rate = latest['value_inc_vat']
                electric_unit_rate.set(unit_rate)
                logger.info(f"Electric unit rate: {unit_rate} p/kWh")
            
            # Get standing charge
            url = f"https://api.octopus.energy/v1/products/{tariff_code}/electricity-tariffs/E-1R-{tariff_code}-E/standing-charges/"
            response = self.session.get(url, params={'page_size': 1})
            response.raise_for_status()
            data = response.json()
            
            if data['results']:
                latest = data['results'][0]
                standing_charge = latest['value_inc_vat']
                electric_standing_charge.set(standing_charge)
                logger.info(f"Electric standing charge: {standing_charge} p/day")
                
        except Exception as e:
            logger.error(f"Failed to get electric tariff: {e}")
    
    def get_gas_tariff(self, tariff_code):
        """Get gas tariff details"""
        try:
            url = f"https://api.octopus.energy/v1/products/{tariff_code}/gas-tariffs/G-1R-{tariff_code}-G/standard-unit-rates/"
            response = self.session.get(url, params={'page_size': 1})
            response.raise_for_status()
            data = response.json()
            
            if data['results']:
                latest = data['results'][0]
                unit_rate = latest['value_inc_vat']
                gas_unit_rate.set(unit_rate)
                logger.info(f"Gas unit rate: {unit_rate} p/kWh")
            
            # Get standing charge
            url = f"https://api.octopus.energy/v1/products/{tariff_code}/gas-tariffs/G-1R-{tariff_code}-G/standing-charges/"
            response = self.session.get(url, params={'page_size': 1})
            response.raise_for_status()
            data = response.json()
            
            if data['results']:
                latest = data['results'][0]
                standing_charge = latest['value_inc_vat']
                gas_standing_charge.set(standing_charge)
                logger.info(f"Gas standing charge: {standing_charge} p/day")
                
        except Exception as e:
            logger.error(f"Failed to get gas tariff: {e}")
    
    def collect_metrics(self):
        """Collect all metrics"""
        logger.info("Collecting Octopus Energy metrics...")
        self.get_electric_consumption()
        self.get_gas_consumption()
        self.get_tariff_rates()
        logger.info("Metrics collection complete")

def main():
    # Get configuration from environment
    port = int(os.getenv('PROM_PORT', 9120))
    interval = int(os.getenv('INTERVAL', 300))  # 5 minutes default
    
    # Start Prometheus metrics server
    start_http_server(port)
    logger.info(f"Started Prometheus metrics server on port {port}")
    
    # Initialize exporter
    try:
        exporter = OctopusExporter()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return
    
    # Main loop
    while True:
        try:
            exporter.collect_metrics()
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
        
        time.sleep(interval)

if __name__ == '__main__':
    main()
