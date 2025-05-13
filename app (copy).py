Conclusion
Yes, data is being fetched directly from services (GAR, GeoAcct, GCCP).

No personally identifiable demographic data (name, email, DOB, address) is being fetched directly from services.

Enrollment.java is the only class with direct demographic-like fields, but it does not perform external service fetches.

Therefore, the application does interact with external services, but none of them return raw demographic data.

Classification remains: Impacted, due to indirect demographic indicators and sensitive identifiers.

Check: Is Any Data Fetched Directly from a Service?
Yes, AM Eligibility fetches data directly from the following sources/services:

GAR API

URL: https://gardc.aexp.com/gar-demographics-api...

Purpose: Account membership and card selection

Analysis: While this API is named “demographics”, the data fetched pertains to account type and membership, not personal demographic data (like name, DOB, email).

GeoAcct

Provides account type information for US/CA/UK.

Used to determine eligibility based on account classification (INDIVIDUAL, SMALL_BUSINESS).

GCCP

Provides corporate account information for US customers.
