1. Application Name
Arrangement Manager - AM Main
2. What Details Are Considered and Analyzed

The analysis focused on identifying whether demographic or personal data is being processed or fetched by the application. 
The following Java files were reviewed:
- PaymentManagement.java
- EnrollmentManagement.java and EnrollmentManagementV2.java
- GetPaymentEligibilityManagement.java
- ActivityLogAction.java
- ReturnRuleAction.java
- UserAction.java

Additionally, the batch file structure from Triumph was reviewed for data elements related to customer demographics.
Modules such as am-core, am-config, and am-service were also inspected for business logic and integration points.

3. What Are the Impacts of Demographic Data in the Application

There is no direct impact identified in terms of processing or fetching demographic data from legacy tables.
The application uses batch uploads to C360 for demographic information from Triumph (US and CA). 
No real-time demographic data is processed or exposed through the Java classes or service modules.

4. Demographics Data Presence in the Application and Its Impact

Across all reviewed files and modules, no demographic data is processed directly or fetched dynamically. 
All demographic updates are managed via batch files mapped to C360.
Hence, the application is classified as **Non-Impacted** under the demographic data handling scope.

