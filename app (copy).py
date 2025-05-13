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


Conclusion
Yes, data is being fetched directly from services (GAR, GeoAcct, GCCP).

No personally identifiable demographic data (name, email, DOB, address) is being fetched directly from services.

Enrollment.java is the only class with direct demographic-like fields, but it does not perform external service fetches.

Therefore, the application does interact with external services, but none of them return raw demographic data.

Classification remains: Impacted, due to indirect demographic indicators and sensitive identifiers.

2. What Details Are Considered and Analyzed

The following files and service modules were reviewed for data sensitivity and demographic relevance:
- AutopayWorker.java
- Arrangement.java
- AutopayIntracycleDAO.java
- Enrollment.java
- Payment.java
- PaymentArrangementServiceImpl.java
- PaymentInstrumentServiceImpl.java
- PymtEligibilityReqVldtr.java
- PymtArrangementListImpl.java

Also reviewed:
- SQL scripts and service API endpoints (GAR, GeoAcct, GCCP)
- Demographic data field types as per the provided data group (Name, DOB, Email, Phone, Address, etc.)

3. What Are the Impacts of Demographic Data in the Application

The application includes several classes and fields that could potentially process or store demographic or sensitive data:
- **Direct Demographic Data**: Found in Enrollment.java (`country_code`, `national_id`), potentially aligning with country or identity details.
- **Indirect Demographic Data**: Seen in fields such as `currency_code`, and owner type in PaymentInstrumentServiceImpl.java (`INDIVIDUAL`, `SMALL_BUSINESS`), which could indicate demographic characteristics.
- **Sensitive Identifiers**: Found in fields like `acctNo`, `CUST_ACCT_NO`, and `AM_ENROLL_ID`, which are processed in multiple classes.
- **Model classes** like Payment.java structure data for payer name, bank account, and payment card details—none of which include direct name, address, or email, but are still sensitive.

4. Demographics Data Presence in the Application and Its Impact

No direct demographic fields such as legal name, address, email, phone number, or DOB were identified that match the exact demographic data group list (see appendix).
However, some fields (country code, national ID, etc.) could be considered **demographic-relevant** under broader classifications.

Thus, the application may not process exact demographic fields but handles **indirect and sensitive identifiers** that could potentially relate to individuals.
Hence, the application is classified as **Impacted** from a demographic data consideration perspective.

