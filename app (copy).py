Here is the final updated document for AM Payment Instrument, now including:

Demographic data usage

Source/destination info (UK, JP, BG)

C360 integration

Japan-specific class analysis

API references for AccountInfoService v4.1 & v6.1


                                  AM-Payment API References
The following Account Information Service endpoints are used:

https://garisldp.aexp.com/ICS/AccountInfoService/v4.1

https://garisldp.aexp.com/ICS/AccountInfoService/v6.1

                                  1. Application Name
Arrangement Manager - AM Payment Instrument

2. What Details Are Considered and Analyzed?
Java classes analyzed:

IntentCreater.java, GetRelationshipDetails.java, Enrollment.java, BankAccountDetails.java, DirectDebitInfoComparator.java

Services/API calls examined:

C360Inquiry (used in Japan and UK markets)

Japan-specific comparator for payment instruments (bank metadata only)

Demographic fields tracked:

first_name, last_name, middle_name, DOB, postal_code, national_id, organization_name, address, embossed_name

3. What Are the Impacts of Demographic Data in the Application?
The application processes sensitive demographic data in some regions, especially Japan, where the data is pulled from C360Inquiry and encrypted for use.

In the UK, demographic data is also retrieved via C360, but the integration is already complete, and no new processing or enhancements are needed.

In the US, no demographic data is fetched or handled — the application primarily works with account metadata.


                                                      Only the Japan market workflow within the AM Payment Instrument app is Impacted by demographic data processing.
UK and US flows are Non-Impacted — UK is already integrated with C360, and US does not process demographic data.
