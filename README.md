# GreenShip - API
A service which accepts a VRM (Vehicle Registration Mark) and returns
the estimated impact of the vehicle to the environment by means of CO2
(Carbon Dioxide) production every year, whilst also recommending the offset.

## Environment Variables

The following environment variables must be defined when running this script:

### MOT_API_KEY
The key used to authenticated requests to MOT History API Service

https://dvsa.github.io/mot-history-api-documentation/

### MOT_API_URL
The API URL for MOT History. Most likely be:

```text
https://beta.check-mot.service.gov.uk/trade/vehicles/mot-tests
```

### DVLA_API_KEY
The key used to authenticate requests to DVLA Vehicle Enquiry Service API

https://developer-portal.driver-vehicle-licensing.api.gov.uk/apis/vehicle-enquiry-service/vehicle-enquiry-service-description.html

### DVLA_API_URL
The API URL for MOT History. Most likely be:

```text
https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles/
```
