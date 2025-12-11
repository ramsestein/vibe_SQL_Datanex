[[\_TOC\_]]
# 1. Introduction
DataNex is the relational database of the Hospital Clínic of Barcelona. You can access DataNex in different ways but \*\*always from a corporate computer within the hospital network\*\* or with VDI connextion if outside the hospital network:
- Datascope: it is the DataNex database straight connection; the database connection can be accomplished by:
- \*\*Metabase\*\* (recommended and supported): it offers a graphical user interface to query the database; you can also use SQL (\_Structured Query Language\_, the programming language used to query the database).
- \*\*MySQL Workbench\*\*: requires SQL knowledge.
- \*\*R\*\*: requires SQL.
- \*\*Python\*\*: requires SQL.
- \*\*Power BI\*\*: it is an interactive data visualization software product.
# 2. Datascope
Datascope has a database credential generator which you should interact with before accesing the data. You can access from a corporate computer within the hospital network. Datascope has two options:
- Manager:
- Enter the [Datascope webpage](https://dsc.clinic.cat/) and sign in with your institutional email and password, select "Manager", select the time you need to explore the database and then you obtain the database access credentials:
![image](uploads/8468b1a9a1c48f6ca05f8a2842b8fb22/image.png){width="500"}
 
- Researcher:
- Before you enter the Datascope webpage, it is necessary to obtain approval from the [CEIm](https://www.clinicbarcelona.org/ca/ceim/requisits#revisio-dhistories-cliniques-recollida-retrospectiva-de-dades), which will provide you with an identifier.
- Once you have your CEIm identifier, you must register it on the [CHRS webpage](https://chris.clinic.cat/) as shown in the image below (click on it to make it bigger): ![image](uploads/aaaf57d752b25c19e26ea5f391e1d36e/image.png){width="1000"}
- There are two possibilities on the CHRS website:
- Inputting the medical record numbers for your study: this will generate an identified database with the information available in DataNex for the entered medical record numbers;
- Not inputting any medical record number: this will grant you access to all Datanex data (though pseudonymized).
- When you have already registered your CEIm identifier on the CHRS webpage, you can enter the [Datascope webpage](https://dsc.clinic.cat/) and sign in with your institutional email and password, select "Researcher", fill the field "Identificador CEIm" with your CEIm identifier, select the time you need to explore the database and then you obtain the database access credentials:
![image](uploads/83ab4ec0f19547f91028c52f6f57ca8b/image.png){width="500"}
 
Once you have obtained your Datascope credentials, choose you preferred software (Metabase, MySQL Workbench, R, Python, Power BI), sign in with your new credentials (procedure explained in the following subsections) and connect to the database (click on the visual summary below to make it bigger):
![image](uploads/28110ecf50161ea5cf9113d2dd13ce8a/image.png)
---
# The g\_administrations table
The `g\_administrations` table contains the administered pharmaceuticals (drugs) for each episode. The `treatment\_ref` field serves as a foreign key that links the `g\_prescriptions`, `g\_administrations` and `g\_perfusions` tables.
The `g\_administrations` table:
&nbsp;
| Attribute | Data type | Key | Definition |
|-------|--------------|-------|------------|
| patient\_ref | INT | fk | pseudonymized number that identifies a patient |
| episode\_ref | INT | fk | pseudonymized number that identifies an episode |
| treatment\_ref | INT | | code that identifies a treatment prescription |
| administration\_date | DATE | | date of administration |
| route\_ref | INT | fk | administration route reference |
| route\_descr | CHAR | | description of route\_ref |
| prn | CHAR | | null value or "X"; the "X" indicates that this drug is administered only if needed |
| given | CHAR | | null value or "X"; the "X" indicates that this drug has not been administered |
| not\_given\_reason\_ref | INT | | number that indicates the reason for non-administration |
| drug\_ref | CHAR | fk | medical product identifier |
| drug\_descr | CHAR | | description of the drug\_ref field |
| atc\_ref | CHAR | | ATC code |
| atc\_descr | CHAR | | description of the ATC code |
| enum | INT | | role of the drug in the prescription (see complementary descriptions [\*\*here\*\*](https://gitlab.com/dsc-clinic/datascope/-/wikis/Prescriptions#complementary-descriptions), where `enum` equals `drug\_type\_ref`) |
| quantity | INT | | dose actually administred to the patient|
| quantity\_planing | INT | | planned dose |
| quantity\_unit | CHAR | fk | dose unit (see complementary descriptions [\*\*here\*\*](https://gitlab.com/dsc-clinic/datascope/-/wikis/Prescriptions#complementary-descriptions)) |
| load\_date | DATETIME | | date of update |
| care\_level\_ref | INT | fk | unique identifier that groups care levels (ICU, WARD, etc) if they are consecutive and belong to the same level |
&nbsp;
---
# The g\_adm\_disch table
The `g\_adm\_disch` table holds the reasons for admission and discharge per episode:
&nbsp;
| Attribute | Data type | Key | Definition |
| ----------- | ----------- | --- | ----------------------------------------------------------------------------------------- |
| patient\_ref | INT | fk | pseudonymized number that identifies a patient |
| episode\_ref | INT | fk | pseudonymized number that identifies an episode |
| mot\_ref | INT | fk | reason for admission or discharge (numeric) |
| mot\_descr | CHAR(32) | | description of the mot\_ref |
| mot\_type | VARCHAR(45) | | it indicates if it is the starting motive (ST) or the ending motive (END) of the episode |
| load\_date | DATETIME | | update date |
&nbsp;
---
# The g\_antibiograms table
The `g\_antibiograms` table contains the antibiograms for each episode:
&nbsp;
| Attribute | Data type | Key | Definition |
|-------|--------------|-------|------------|
| patient\_ref | INT | fk | pseudonymized number that identifies a patient |
| episode\_ref | INT | fk | pseudonymized number that identifies an episode |
| extrac\_date | DATETIME | | date and time the sample was extracted |
| result\_date | DATETIME | | date and time the result was obtained |
| sample\_ref | CHAR | | code that identifies the type or origin of the sample |
| sample\_descr | CHAR | | description of the type or origin of the sample; it provides a general classification of the sample |
| antibiogram\_ref | INT | | unique identifier for the antibiogram |
| micro\_ref | CHAR | | code that identifies the microorganism |
| micro\_descr | CHAR | | scientific name of the microorganism |
| antibiotic\_ref | CHAR | | code of the antibiotic used in the sensitivity testing |
| antibiotic\_descr | CHAR | | full name of the antibiotic |
| result | CHAR | | the result of the antibiotic sensitivity test; the value represents the minimum inhibitory concentration (MIC) required to inhibit the growth of the bacteria |
| sensitivity | CHAR | | sensitivity (S) or resistance (R) of the bacteria to the antibiotic tested |
| load\_date | DATETIME | | date of update |
| care\_level\_ref | INT | fk | unique identifier that groups care levels (intensive care unit, conventional hospitalization, etc.) if they are consecutive and belong to the same level |
&nbsp;
---
# The g\_rc table
The `g\_rc` table contains the clinical records for each episode (currently, the fields `episode\_ref` and `care\_level\_ref` are empty but they will be filled soon):
&nbsp;
| Attribute | Data type | Key | Definition |
|-------|--------------|-------|------------|
| patient\_ref | INT | fk | pseudonymized number that identifies a patient |
| episode\_ref | INT | fk | pseudonymized number that identifies an episode |
| result\_date | DATETIME | | date and time of the measurement |
| meas\_type\_ref | CHAR(1) | | 0 (manual input), 1 (from machine, result not validated), 2 (from machine, result validated) |
| load\_date | DATETIME | | date of update |
| ou\_loc\_ref | CHAR(8) | fk | physical hospitalization unit; this cell is filled if the clinical registry is manually collected but it is left empty if the clinical registry is automatically collected |
| ou\_med\_ref | CHAR(8) | fk | medical organizational unit; this cell is filled if the clinical registry is manually collected but it is left empty if the clinical registry is automatically collected |
| rc\_sap\_ref | CHAR(16) | | SAP clinical record reference |
| rc\_descr | CHAR(32) | | description of the SAP clinical record reference |
| result\_num | FLOAT | | numerical result of the clinical record |
| result\_txt | VARCHAR(128) | | text result from the DataNex clinical record reference; check its [\*\*<ins>dictionary</ins>\*\*](https://dsc-clinic.gitlab.io/datascope/rc\_result\_txt\_dic.html) |
| units | CHAR(8) | | units |
| care\_level\_ref | INT | fk | unique identifier that groups care levels (intensive care unit, conventional hospitalization, etc.) if they are consecutive and belong to the same level |
&nbsp;
---
[[\_TOC\_]]
# Help and support
DataNex is an initiative of Medical Direction developed by a multidisciplinary team from the Clinical Informatics and Information Systems departments of the Hospital Clínic.
We have limited resources and cannot provide individual support in all cases.
---
# The g\_demographics table
The `g\_demographics` table contains demographic information for each patient:
&nbsp;
| Attribute | Data type | Key | Definition |
|-------|--------------|-------|------------|
| patient\_ref | INT | PK | pseudonymized number that identifies a patient |
| birth\_date | DATE | | date of birth |
| sex | INT | | -1 (not reported in SAP), 1 (male), 2 (female), 3 (other) |
| natio\_ref | CHAR(8) | fk | reference code for nationality |
| natio\_descr | CHAR(512) | | description of the country code according to ISO:3 |
| health\_area | CHAR | | health area |
| postcode | CHAR | | postal code |
| load\_date | DATETIME | | date of update |
&nbsp;
---
---
title: Diagnostics and DRG
---
The `g\_diagnostics` and `g\_diagnostic\_related\_groups` tables contain information about the diagnostics and the diagnostic-related group (DRG) for each episode, respectively.
For each episode, we have the set of diagnostics that have occurred during that episode. The diagnostics are not related to any specific care level or movement. For example, if a patient is admitted to the ICU for a severe traumatic brain injury, develops pneumonia while in the ICU and suffers a urinary tract infection when in the conventional hospitalization room, we will have two care levels (ICU and WARD) and three diagnostics (severe traumatic brain injury, pneumonia and urinary tract infection), but we will not be able to know which diagnostic occurred in each care level.
The `diag\_date`, which is an attribute from the `g\_diagnostics` table and represents the diagnosis date, follows the next rules: in hospital episodes (care levels WARD, ICU, SPEC or SHORT) and home hospitalization episodes (care level HAH), the `diag\_date` of the diagnosis corresponds to the start date of the episode; in outpatient episodes (care level OUT), the `diag\_date` is the day of the visit; in emergency episodes (care level EM), the `diag\_date` could be any day within the emergency episode.
Diagnostics are codified using International Classification of Diseases (ICD) version 9 until 2017 (included) and ICD-10 since 2018 (included). You can look up for the codes related to specific conditions in the next websites.
\* ICD-10: [https://icd10cmtool.cdc.gov](https://icd10cmtool.cdc.gov/?fy=FY2024) (Official CDC website)
\* ICD-9: [https://www.aapc.com/codes/icd9-codes](https://www.aapc.com/codes/icd9-codes/379.25)
\* MDC categories: https://en.wikipedia.org/wiki/Major\_Diagnostic\_Category
The tables:
[[\_TOC\_]]
 
# A. The g\_diagnostics table
| Attribute | Data type | Key | Definition |
| --- | --- | --- | --- |
| patient\_ref | INT | fk | pseudonymized number that identifies a patient |
| episode\_ref | INT | fk | pseudonymized number that identifies an episode |
| diag\_date | DATETIME |  | diagnostic code registration date |
| diag\_ref | INT | fk | DataNex own diagnosis reference number |
| catalog | INT |  | catalog to which the 'code' belongs. \* 1 is CIE9 MC (until 2017) \* 2 is MDC \* 3 is CIE9 Emergencies \* 4 is ACR \* 5 is SNOMED \* 7 is MDC-AP \* 8 is SNOMEDCT \* 9 is Subset ANP SNOMED CT \* 10 is Subset ANP SNOMED ID \* 11 is CIE9 in Outpatients \* 12 is CIE10 MC \* 13 is CIE10 Outpatients |
| code | CHAR(8) |  | ICD-9 or ICD-10 code for each diagnosis |
| diag\_descr | CHAR(32) |  | description of the diagnosis |
| class | CHAR(2) |  | \* \*\*P\*\* (code for primary diagnosis in hospitalization episodes validated by the documentalist) \* \*\*S\*\* (code for secondary diagnosis in hospitalization episodes validated by the documentalist) \* \*\*H\*\* (code for diagnosis in hospitalization episodes not validated by the documentalist) \* \*\*E\*\* (code for diagnosis in emergency episodes) and \* \*\*A\*\* (code for diagnosis in outpatient episodes) A hospitalization episode has only one P diagnosis and zero or more S or H diagnoses |
| poa | CHAR(2) |  | the Present on Admission (POA) indicator indicates whether the condition was present at admission (a comorbidity) or whether it arose during the hospitalization (a complication); options: \* \*\*Y\*\* (Yes, present at the time of inpatient admission) \* \*\*N\*\* (No, not present at the time of inpatient admission) \* \*\*U\*\* (Unknown, documentation is insufficient to determine if condition is present on admission) \* \*\*W\*\* (Clinically undetermined, provider is unable to clinically determine whether condition was present on admission or not) \* \*\*E\*\* (Exempt) \* \*\*-\*\* (Unreported, it means that the documentalist has not registered the diagnostic code) |
| load\_date | DATETIME |  | date of update |
 
# B. The g\_diagnostic\_related\_groups table
In this table are recorded the [Diagnosis-Related-Groups](https://en.wikipedia.org/wiki/Diagnosis-related\_group) (DRG). DRG is a concept used to categorize hospital cases into groups according to diagnosis, procedures, age, comorbidities and other factors. These DRG are used mainly for administrative purposes, billing and resource allocation. DRG are further classified in Major Diagnostic Categories (MDC).
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| patient\_ref | INT | fk | pseudonymized number that identifies a patient |
| episode\_ref | INT | fk | pseudonymized number that identifies an episode |
| weight | FLOAT | | drg cost weight, meaning the relative resource consumption for that group compared to others |
| drg\_ref | INT | fk | drg (diagnosis-related group) reference |
| severity\_ref | CHAR(2) | fk | soi (Severity of Illness) reference: a metric to evaluate how sick a patient is |
| severity\_descr | CHAR(128) | | description of the soi reference |
| mortality\_risk\_ref | CHAR(2) | fk | rom (Risk of Mortality) reference: a metric to evaluate the likelihood of a patient dying |
| mortality\_risk\_descr | CHAR(128) | | description of the rom reference |
| mdc\_ref | INT | fk | mdc (Major Diagnostic Categories) reference: those are broad categories used to group DRG based on similar clinical conditions or body systems |
| load\_date | DATETIME | | date of update |
---
The dictionary tables in Datanex:
[[\_TOC\_]]
# A. The dic\_diagnostic table
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| diag\_ref | INT | fk | Datanex own diagnosis reference number |
| catalog | INT | | catalog to which the diagnostic code belongs. 1 is CIE-9 (until 2017, included), while 11, 12 and 13 are CIE-10 (since 2018, included) |
| code | CHAR(45) | | ICD-9 or ICD-10 code for each diagnostic |
| diag\_descr | CHAR(256) | | description of the diagnosis |
&nbsp;
# B. The dic\_lab table
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| lab\_sap\_ref | CHAR(16) | fk | SAP laboratory parameter reference |
| lab\_descr | CHAR(256) | | lab\_sap\_ref description |
| units | CHAR(32) | | units |
| lab\_ref | INT | | Datanex laboratory parameter reference |
&nbsp;
# C. The dic\_ou\_loc table
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| ou\_loc\_ref | CHAR(16) | fk | physical hospitalization unit reference |
| ou\_loc\_descr | CHAR(256) | | description of the physical hospitalization unit reference |
| care\_level\_type\_ref | CHAR(16) | fk | care level (ICU, HAH, etc.) |
| facility\_ref | INT | | facility reference |
| facility\_descr | CHAR(32) | | description of the facility reference |
&nbsp;
# D. The dic\_ou\_med table
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| ou\_med\_ref | CHAR(8) | fk | medical organizational unit reference |
| ou\_med\_descr | CHAR(32) | | description of the medical organizational unit reference |
&nbsp;
# E. The dic\_rc table
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| rc\_sap\_ref | CHAR(16) | fk | SAP clinical record reference |
| rc\_descr | CHAR(256) | | description of the SAP clinical record reference |
| units | CHAR(32) | | units |
| rc\_ref | INT | | Datanex clinical record reference |
&nbsp;
# F. The dic\_rc\_text table
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| rc\_sap\_ref | CHAR(16) | fk | SAP clinical record reference |
| result\_txt | CHAR(36) | | text result from the `rc\_sap\_ref` field |
| descr | CHAR(191) | | description of the `result\_txt` field |
&nbsp;
---
Index:
[[\_TOC\_]]
# The g\_dynamic\_forms table
Dynamic forms collect clinical data in a structured manner. All of this data is recorded in the `g\_dynamic\_forms` table, where each dynamic form and its characteristics appear as many times as the form was saved in SAP. This is reflected in the `form\_date` variable, which stores the date or dates when the form was saved.
The `g\_dynamic\_forms` table:
&nbsp;
| Attribute | Data type | Key | Definition |
| - | - | - | - |
| patient\_ref | INT | fk | Pseudonymized number that identifies a patient. |
| episode\_ref | INT | fk | Pseudonymized number that identifies an episode. |
| ou\_loc\_ref | CHAR(8) | fk | Physical hospitalization unit reference. |
| ou\_med\_ref | CHAR(8) | fk | Medical organizational unit reference. |
| status | CHAR(3) | | Record status:<br>• \*\*CO\*\*: completed;<br>• \*\*EC\*\*: in process. |
| form\_ref | CHAR(8) | | Form name identifier. |
| form\_descr | CHAR | | Form description. |
| tab\_ref | CHAR(10) | | Form tab (group) identifier. |
| tab\_descr | CHAR | | Tab description. |
| section\_ref | CHAR(10) | | Form section (parameter) identifier. |
| section\_descr | CHAR | | Section description. |
| type\_ref | CHAR(8) | | Form question (characteristic) identifier. |
| type\_descr | CHAR | | Characteristic description. |
| class\_ref | CHAR(3) | | Assessment class:<br>• \*\*CC\*\*: structured clinical course forms;<br>• \*\*EF\*\*: physical examination forms;<br>• \*\*ES\*\*: scale forms;<br>• \*\*RG\*\*: record or report forms;<br>• \*\*RE\*\*: special record forms;<br>• \*\*VA\*\*: assessment forms;<br>• \*\*TS\*\*: social work forms. |
| class\_descr | CHAR | | Class description. |
| value\_num | FLOAT | | Numeric value inserted. |
| value\_text | CHAR(255) | | Text value inserted. |
| value\_date | DATETIME | | Datetime value inserted. |
| form\_date | DATETIME | | Date when the form was saved. |
| load\_date | DATETIME | | Date of update. |
&nbsp;
# Descriptions for form, tab, section and type concepts
The following schema specifies the components of the dynamic forms:
![FD2](uploads/ef9debd2c52ac0109a0fd481dd2bb839/FD2.PNG)
&nbsp;
---
# The g\_encounters table
An encounter refers to a punctual event in which detailed information is recorded about a medical interaction or procedure involving a patient (for instance a chest radiograph, an outpatient visit, etc).
The dictionaries of the `encounter\_type`, `agen\_ref` and `act\_type\_ref` fields will be available in the next updates.
The `g\_encounters` table contains the encounters for each episode:
 
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| patient\_ref | INT | fk | pseudonymized number that identifies a patient |
| episode\_ref | INT | fk | pseudonymized number that identifies an episode |
| date | DATETIME | | date of the encounter event |
| load\_date | DATETIME | | update date |
| ou\_med\_ref | CHAR(8) | fk | medical organizational unit reference; points to the ou\_med\_dic table |
| ou\_loc\_ref | CHAR(8) | fk | physical hospitalization unit reference; points to the ou\_loc\_dic table |
| encounter\_type | CHAR(8) | fk | encounter type |
| agen\_ref | CHAR | fk | code that identifies the encounter |
| act\_type\_ref | CHAR(8) | fk | activity type |
&nbsp;
The dictionary for encounter\_type is:
| Code | Description |
|--------|---------------------|
| 2O | 2ª opinión |
| AD | Hosp. día domic. |
| BO | Blog. obstétrico |
| CA | Cirugía mayor A |
| CM | Cirugía menor A |
| CU | Cura |
| DH | Derivación hosp |
| DI | Der. otros serv. |
| DU | Derivación urg. |
| EI | Entrega ICML |
| HD | Hospital de día |
| IC | Interconsulta |
| IH | Servicio final |
| IQ | Interv. quir. |
| LT | Llamada telef. |
| MA | Copia mater. |
| MO | Morgue |
| NE | Necropsia |
| PA | Preanestesia |
| PD | Posible donante |
| PF | Pompas fúnebres |
| PP | Previa prueba |
| PR | Prueba |
| PV | Primera vista |
| RE | Recetas |
| SM | Sec. multicentro |
| TR | Tratamiento |
| UD | Urg. hosp. día |
| UR | Urgencias |
| VD | Vis. domicilio |
| VE | V. Enf. Hospital |
| VU | Vista URPA |
| VS | Vista sucesiva |
| VU | Vista urgencias |
---
The three central tables (the `g\_episodes`, `g\_care\_levels` and `g\_movements` tables) follow a hierarchy: episodes (in the `g\_episodes` table) hold care levels (in the `g\_care\_levels` table) and care levels hold movements (in the `g\_movements` table). This idea could be represented as \*\*episodes \> care levels \> movements\*\*.
In order to link these tables:
- Use the common field `episode\_ref` to join `g\_episodes` and `g\_care\_levels`.
- Use the common field `care\_level\_ref` to join `g\_care\_levels` and `g\_movements`.
Patients are loaded into Datanex following this logic: an index date is chosen, for instance 1/1/2022, and all the new episodes and movements from 1/1/2022 to 1/3/2024 are loaded into Datanex. If a patient has an opened outpatient episode that began before the index date, information about movements (visits) after the index date will NOT appear in Datanex.
The tables:
[[\_TOC\_]]
# A. The g\_episodes table
Episodes are medical events experienced by a patient: an admission (planned or from the emergency department), an assessment in the emergency department, a set of visits for a medical specialty in outpatients, etc. Episodes are composed by care levels (see below). The `g\_episodes` table stores these episodes.
The `g\_episodes` table:
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| episode\_ref | INT | PK | pseudonymized number that identifies an episode |
| patient\_ref | INT | fk | pseudonymized number that identifies a patient |
| episode\_type\_ref | CHAR(8) | | it indicates the episode typology, which can be AM (outpatient episode), EM (emergency episode), DON (Donor), HOSP\_IQ (hospitalization episode for surgery), HOSP\_RN (hospitalization episode for healthy newborn), HOSP (hospitalization episode different from HOSP\_IQ and HOSP\_RN), EXT\_SAMP (external sample), HAH (hospital at home or home hospitalization) |
| start\_date | DATETIME | | start date and time of the episode |
| end\_date | DATETIME | | end date and time of the episode; in AM episodes (outpatient episodes), the end\_date does not signify the end of the episode but rather the date of the patient's last visit |
| load\_date | DATETIME | | update date |
 
# B. The g\_care\_levels table
Care level refers to the intensity of healthcare needs that a patient requires. Inside an episode, a care level groups different movements (movements are changes in the patient's location, see below) that share the same intensity of healthcare needs.
Only EM, HAH and all HOSP (HOSP, HOSP\_RN and HOSP\_IQ) episode types have care levels.
For the same patient, each new care level is uniquely identified by a number, that is, if in the same admission the patient goes from level WARD to level ICU and then to level WARD, they would have three different numeric identifiers, one for each new level.
The `g\_care\_levels` table stores the care levels for each episode:
 
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| patient\_ref | INT | fk | pseudonymized number that identifies a patient |
| episode\_ref | INT | fk | pseudonymized number that identifies an episode |
| care\_level\_ref | INT | PK | unique identifier that groups consecutive care levels (ICU, WARD, etc) if they belong to the same level |
| start\_date | DATETIME | | start date and time of the admission |
| end\_date | DATETIME | | end date and time of the admission |
| load\_date | DATETIME | | update date |
| care\_level\_type\_ref | CHAR(8) | fk | care level, which can be WARD (conventional hospitalization), ICU (intensive care unit), EM (emergency episode), SPEC (special episode), HAH (hospital at home or home hospitalization), PEND. CLAS (pending classification), SHORT (short stay) |
 
# C. The g\_movements table
Movements are changes in the patient's location; for example, a movement could be that a patient is transferred from hospitalization room A to hospitalization room B.
Patient discharge and exitus are also considered movements; in both cases, start date and end date are identical.
All movements have a `care\_level\_ref`.
Only EM, HAH and all HOSP (HOSP, HOSP\_RN and HOSP\_IQ) episode types have movements.
The `g\_movements` table stores the movements for each care level:
 
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| patient\_ref | INT | fk | pseudonymized number that identifies a patient |
| episode\_ref | INT | fk | pseudonymized number that identifies an episode |
| start\_date | DATETIME | | date and time of the start of the movement |
| end\_date | DATETIME | | date and time of the end of the movement |
| place\_ref | INT | | encrypted reference for the patient's room and bed |
| ou\_med\_ref | CHAR(8) | fk | medical organizational unit reference |
| ou\_med\_descr | CHAR(32) | | description of the medical organizational unit reference |
| ou\_loc\_ref | CHAR(8) | fk | physical hospitalization unit reference |
| ou\_loc\_descr | CHAR(32) | | description of the physical hospitalization unit reference |
| care\_level\_type\_ref | CHAR(8) | fk | care level (ICU, HAH, etc.) |
| facility | CHAR(32) | | description of the facility reference |
| load\_date | DATETIME | | date of update |
| care\_level\_ref | INT | fk | unique identifier that groups care levels (intensive care unit, conventional hospitalization, etc.) if they are consecutive and belong to the same level |
---
# The g\_exitus table
The `g\_exitus` table contains the date of death for each patient:
&nbsp;
| Attribute | Data type | Key | Definition |
|-------|--------------|-------|------------|
| patient\_ref | INT | PK | pseudonymized number that identifies a patient |
| exitus\_date | DATE | | date of death |
| load\_date | DATETIME | | date and time of update |
---
[[\_TOC\_]]
# Error Code: 2013. Lost connection to MySQL server during query
If you find this error, you can solve it by: open MySQL Workbench > Edit > Preferences > SQL Editor > set DBMS connection read timeout interval (in seconds) to 0 > OK > close MySQL Workbench program and open it again. See the image below:
![image](uploads/07fc76fcc8a13c728546b24011e31a11/image.png)
---
---
title: Health problems
---
# The g\_health\_issues table
The `g\_health\_issues` table contains information about all the health problems related to a patient. Health problems are SNOMED-CT (Systematized Nomenclature of Medicine Clinical Terms) codified health problems that a patient may present. SNOMED is a comprehensive multilingual clinical terminology used worlwide in healthcare. Those health problems are codified by the doctors taking care of the patients, thus expanding and enriching the codification possibilities.
Health problems have a start date, indicating when they were first recorded by the clinician, and may also have an end date, marking when the clinician determined the health problem was no longer active. The `end\_motive` field records the reason for the change in this status.
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| patient\_ref | INT | fk | pseudonymized number that identifies a patient |
| episode\_ref | INT | fk | pseudonymized number that identifies an episode |
| snomed\_ref | INT | | SNOMED code for a health problem |
| snomed\_descr | CHAR(255) | | description of the SNOMED code |
| ou\_med\_ref | CHAR(8) | fk | medical organizational unit reference |
| start\_date | DATE | | start date of the health problem |
| end\_date | DATE | | end date of the health problem (not mandatory) |
| end\_motive | INT | | reason for the change (not mandatory) |
| load\_date | DATETIME | | date of update |
---
Do you have any good idea to make use of clinical data from DataNex or directly from SAP system and need some support to get these data?
That is great! All data requests in our center are centralized in Finestra Clínic Digital:
https://intranet.clinic.cat/finestra-clinic-digital
Thanks for your interest!! We'll reach you as soon as possible.
---
# The g\_labs table
The `g\_labs` table contains the laboratory tests for each episode:
&nbsp;
| Attribute | Data type | Key | Definition |
|-------|--------------|-------|------------|
| patient\_ref | INT | fk | pseudonymized number that identifies a patient |
| episode\_ref | INT | fk | pseudonymized number that identifies an episode |
| extrac\_date | DATETIME | | date and time the sample was extracted |
| result\_date | DATETIME | | date and time the result was obtained |
| load\_date | DATETIME | | date of update |
| ou\_med\_ref | CHAR(8) | fk | medical organizational unit |
| care\_level\_ref | INT | fk | unique identifier that groups care levels (ICU, WARD, etc) if they are consecutive and belong to the same level; the care\_level\_ref is absent if the lab test is requested after the end of the episode in EM, HOSP and HAH episodes |
| lab\_sap\_ref | CHAR(16) | fk | SAP laboratory parameter reference |
| lab\_descr | CHAR(32) | | lab\_sap\_ref description |
| result\_num | FLOAT | | numerical result of the laboratory test |
| result\_txt | VARCHAR(128) | | text result from the DataNex laboratory reference |
| units | CHAR(32) | | units |
| lab\_group\_ref | INT | | reference for grouped laboratory parameters |
&nbsp;
---
See [SQL tutorial with DataNex examples - INTRODUCTION](https://gitlab.com/dsc-clinic/datascope/-/wikis/SQL-Tutorial-with-DataNex-Examples#introduction) to know how to display the query results.
Page contents:
[[\_TOC\_]]
&nbsp;
---
In this section you will find how to enter Metabase and how to use it. These are the contents:
[[\_TOC\_]]
&nbsp;
Warning:
![image](uploads/44ef2c49f360735b3056e6d87b62a536/image.png){width=800 height=150}
&nbsp;
# 1. Enter Metabase through a web browser
If you are using a corporate computer within the hospital network, then you can enter the [Metabase webpage](https://metabase.clinic.cat/). Get your credentials [here](https://dsc.clinic.cat/). For more information, visit [this section](https://gitlab.com/dsc-clinic/datascope/-/wikis/Access-Instructions#datascope-access).
&nbsp;
# 2. Example of Metabase use
Use g\_episodes and g\_diagnostics (joined on episode\_ref), select rows with the diagnostic code M81.0, group by type\_episode and count the distinct episode\_refs in each type\_episode group:
![image](uploads/5425f49cbc0e10a92301536eda2cb5c0/image.png){width=648 height=596}
&nbsp;
![image](uploads/60fdade682074bf54b19a253916a866d/image.png){width=617 height=209}
&nbsp;
# 3. Metabase custom expressions
Metabase custom expressions allow you to manage data beyond the Metabase graphical user interface. In other words, custom expressions provide greater flexibility than the graphical interface.
For instance, when using conditions, they are internally separated by 'AND' in the graphical interface. How can you separate these conditions with 'OR'? You need custom expressions:
| Writing a custom expression | Result in the query editor |
| ------ | ------ |
| ![image](uploads/fe4f42b3daba9190960fe2f4fb496d53/image.png){width=417 height=204} | ![image](uploads/00ba3e963c430c0a2ca52df4178f6c2c/image.png){width=350 height=87} |
&nbsp;
You may also need custom expressions when managing dates:
| Writing a custom expression | Result in the query editor |
| ------ | ------ |
| ![image](uploads/5953784f2f5acec663b40df391b6bae7/image.png){width=400 height=247} | ![image](uploads/c1df16ba18bdbc61af9647916c9a2cd8/image.png){width=395 height=88} |
&nbsp;
To learn more about custom expressions, use the links from Metabase:
- [Custom expressions documentation](https://www.metabase.com/docs/latest/questions/query-builder/expressions)
- [List of custom expressions](https://www.metabase.com/docs/latest/questions/query-builder/expressions-list)
&nbsp;
# 4. Metabase local setup
If you want, you can install Metabase locally and start it:
- Download and install the latest java version from
https://www.oracle.com/es/java/technologies/downloads/ (after the installation, you
may need to reboot your system).
- Create a folder called 'metabase'.
- Download the metabase.jar file (get it from https://www.metabase.com/start/oss/jar)
and move it to the folder called 'metabase'.
- Double click on the metabase.jar file.
- Visit http://localhost:3000 through your preferred web browser; after a few seconds,
you will have all Metabase software visible.
&nbsp;
The first time you visit the metabase site, you will have to set up your database configuration:
![image](uploads/5b66e042cb08b32dfee50ce5d233b8c7/image.png)
![image](uploads/d4264881498c5de0ae35404a6c813911/image.png)
- Select MySQL:
![image](uploads/c9cd2bff575e7add851cc1b3697db5db/image.png)
- Enter the host, port and database name (they may change over time, so check our [quick reference](https://gitlab.com/dsc-clinic/datascope/-/wikis/Quick-reference)); enter your database username
and password (obtained from https://dsc.clinic.cat/) as well:
![image](uploads/d783a70e26011f82062b3ea2fa358558/image.png)
![image](uploads/ef4d0ffdcfffae003d677907979ae106/image.png)
- You are free to give your email at the last step:
![image](uploads/85e87e50ce0b7efac67f5728bd0dc014/image.png)
&nbsp;
The next time you enter Metabase (always by double clicking on the metabase.jar file
and then visiting http://localhost:3000 at your web browser), you will reach this page:
![image](uploads/94c14e0a7f8e277144dbc517a050160b/image.png)
- Enter your mail and the password you created the first time you used Metabase.
- Update your database user and password:
1. Go to settings (top right):
![image](uploads/a2caf5cdd9bd2de739693fdf4b578293/image.png)
2. Admin settings:
![image](uploads/314b50bcefb8a4f0e2e8bf669b1ac06d/image.png)
3. Databases:
![image](uploads/e7b83c1c24c131f17f0a96ad833ec4ba/image.png)
4. Update your database user and password.
5. Exit admin:
![image](uploads/6f345c90c6d5f5d6ad99a10269c3ccf7/image.png)
---
# The g\_micro table
The `g\_micro` table contains the microbiology results for each episode:
&nbsp;
| Attribute | Data type | Key | Definition |
|-------|--------------|-------|------------|
| patient\_ref | INT | fk | pseudonymized number that identifies a patient |
| episode\_ref | INT | fk | pseudonymized number that identifies an episode |
| extrac\_date | DATETIME | | date and time the sample was extracted |
| res\_date | DATETIME | | date and time the result was obtained |
| ou\_med\_ref | CHAR(8) | fk | medical organizational unit |
| mue\_ref | CHAR | | code that identifies the type or origin of the sample |
| mue\_descr | CHAR | | description of the type or origin of the sample; it provides a general classification of the sample |
| method\_descr | CHAR | | detailed description of the sample itself or the method used to process the sample; it includes specific procedures and tests performed |
| positive | CHAR | | 'X' means that a microorganism has been detected in the sample |
| antibiogram\_ref | INT | | unique identifier for the antibiogram |
| micro\_ref | CHAR | | code that identifies the microorganism |
| micro\_descr | CHAR | | scientific name of the microorganism |
| num\_micro | INT | | a number that starts at 1 for the first identified microbe and increments by 1 unit for each newly identified microbe in the sample |
| result\_text | VARCHAR(128) | | text result from the microbiology sample |
| load\_date | DATETIME | | date of update |
| care\_level\_ref | INT | fk | unique identifier that groups care levels (intensive care unit, conventional hospitalization, etc.) if they are consecutive and belong to the same level |
&nbsp;
---
# 1. Natlang2sql
In order to help clinicians to obtain more richness from the Datanex database, our data engineering team has developed a generative artificial intelligence tool that translates natural language questions to SQL queries called \*\*Natlang2sql\*\*:
![image](uploads/654b1e03bb4b31d7834943a612d9910e/image.png){width=609 height=232}
# 2. How to use it
First, you should enter the [Datascope webpage](https://dsc.clinic.cat/) and introduce your corporative credentials (institutional mail and password).
Second, with an active session in Datascope, you now can enter [Natlang2sql](https://dsc.clinic.cat/natlang2sql).
And finally, write your natural language question to Datanex, translate it to SQL authomatically by clicking "Generate SQL", copy your new SQL query and paste it on Metabase (or your preferred software to retrieve data from Datanex).
Keep in mind that that \*\*Natlang2sql can make mistakes (it is still being tested)\*\*.
---
---
title: News
---
This page serves to announce news and document changes in the DataNex database.
# News
| Concept | Expected date | Description if needed |
|---------|---------------|-----------------------|
| Dynamic forms | 11/2025 | Table under maintenance. Data from 2007 to 2025 is being uploaded. |
| Special records | 11/2025 | Table under maintenance. This table is also known as 'nursing records'. |
| Laboratory | 11/2025 | Data from 2007 to 2025 is being uploaded. |
| Surgical procedures | 2025 | Creating table. |
| Provisions | 12/2025 | The table on healthcare provisions ('Prestaciones') is being uploaded with all data from 2007 to 2025. |
| Treatment tables | Unknown | Treatment tables (administrations, prescriptions and perfusions) under maintenance from 10 November 2025 due to some bugs. Data may be inconsistent until the issues are resolved. |
&nbsp;
# History
| Concept | Date | Description | Affected table(s) if applicable |
|---------|------|-------------|---------------------------------|
| Table modification | 02/12/2023 | The laboratory already includes variables that are text; the following have been excluded from the upload: Cancel.lat, En curs, Gràfica, Fet en laboratori extern, Veure comentari, Veure resultats mostra sang fetal. | g\_labs |
| Table modification | 02/12/2023 | The diagnoses that have CIE code but have not been validated by the documentalist are labeled with 'A' in the 'class' column. | g\_diagnostics |
| Table modification | 14/01/2024 | The Present on Admission (POA) indicator has been entered; if the POA is not registered, it is set to '-'. | g\_diagnostics |
| New data | 06/02/2024 | Publication of the dictionary for the result\_txt variable from the g\_rc table | g\_rc |
| General update begins | 06/05/2024 | Updating Datanex. Connection errors may occur and data inconsistencies may be present because not all tables are completed yet. We apologize for the inconvenience. | All tables |
| New tables | 09/05/2024 | | Prescription tables |
| Access problems | 31/05/2024 | Users who do not have an '@clinic.cat' email address cannot enter Datascope; we are working to fix this issue | |
| Access problems | 07/06/2024 | Solved | |
| General update ends | 01/07/2024 | | All tables |
| New tables | 01/07/2024 | | Administered treatment, microbiology, antibiogram and perfusion tables |
| Data upload strategy | 01/07/2024 | The database is filled with data for each month sequentially (month by month). This means that all episodes from the month being completed are uploaded, along with all their patients’ episodes from both before and after the loaded month. We started with February 2021 and will continue by completing consecutive months. | All tables |
| New tables | 15/09/2024 | | Table of dynamic forms |
| New tables | 15/09/2024 | | Table of health issues |
| General update | 26/10/2024 | | All tables |
| General update | 17/12/2024 | | All tables |
| Server migration | 24/02/2025 | Datanex will be unavailable from 25 to 28 february 2025 | All infrastructure |
| Procedures table added | 04/03/2025 | The procedures table is now available to query! | |
| General update | 10/10/2025 | | All tables |
---
# Overview
---
# The g\_perfusions table
The `g\_perfusions` table contains data about the administered drug perfusions for each episode. The `treatment\_ref` field serves as a foreign key that links the `g\_prescriptions`, `g\_administrations` and `g\_perfusions` tables.
The `g\_perfusions` table:
 
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| patient\_ref | INT | fk | pseudonymized number that identifies a patient |
| episode\_ref | INT | fk | pseudonymized number that identifies an episode |
| treatment\_ref | INT | | code that identifies a treatment prescription. Points to the `treatment\_ref` in the `g\_administrations` and `g\_prescriptions` tables |
| infusion\_rate | INT | | rate in ml/h |
| rate\_change\_counter | INT | | perfusion rate change counter: starts at 1 (first rate) and increments by one unit with each change (each new rate) |
| start\_date | DATETIME | | start date of the perfusion |
| end\_date | DATETIME | | end date of the perfusion |
| load\_date | DATETIME | | date of update |
| care\_level\_ref | INT | fk | unique identifier that groups care levels (ICU, WARD, etc) if they are consecutive and belong to the same level |
---
[[\_TOC\_]]
&nbsp;
# The g\_prescriptions table
The `g\_prescriptions` table contains the prescribed medical products, which are pharmaceuticals (drugs) and medical devices, for each episode. A treatment prescription (identified by `treatment\_ref`) may be composed by one or more medical products so this table will show as many rows as prescribed medical products per treatment prescription. The `treatment\_ref` field serves as a foreign key that links the `g\_prescriptions`, `g\_administrations` and `g\_perfusions` tables.
The `g\_prescriptions` table:
&nbsp;
| Attribute | Data type | Key | Definition |
|-------|--------------|-------|------------|
| patient\_ref | INT | fk | pseudonymized number that identifies a patient |
| episode\_ref | INT | fk | pseudonymized number that identifies an episode |
| treatment\_ref | INT | | code that identifies a treatment prescription |
| prn | CHAR | | null value or "X"; the "X" indicates that this drug is administered only if needed |
| freq\_ref | CHAR | fk | administration frequency code |
| phform\_ref | INT | fk | pharmaceutical form identifier |
| phform\_descr | CHAR | | description of phform\_ref |
| prescr\_env\_ref | INT | fk | healthcare setting where the prescription was generated (complementary descriptions below) |
| adm\_route\_ref | INT | fk | administration route reference |
| route\_descr | CHAR | | description of adm\_route\_ref |
| atc\_ref | CHAR | | ATC code |
| atc\_descr | CHAR | | description of the ATC code |
| ou\_loc\_ref | CHAR(8) | fk | physical hospitalization unit |
| ou\_med\_ref | CHAR(8) | fk | medical organizational unit |
| start\_drug\_date | DATETIME | | start date of prescription validity |
| end\_drug\_date | DATETIME | | end date of prescription validity |
| load\_date | DATETIME | | date of update |
| drug\_ref | CHAR | fk | medical product identifier |
| drug\_descr | CHAR | | description of the drug\_ref field |
| enum | INT | | role of the drug in the prescription (complementary descriptions below, where `enum` equals `drug\_type\_ref`) |
| dose | INT | | prescribed dose |
| unit | CHAR | fk | dose unit (complementary descriptions below) |
| care\_level\_ref | INT | fk | unique identifier that groups care levels (ICU, WARD, etc) if they are consecutive and belong to the same level |
&nbsp;
# Complementary descriptions
The table is complemented by:
---
# The g\_procedimientos table
The `g\_procedimientos` table contains all procedures per episode:
&nbsp;
| Attribute | Data type | Key | Definition |
|-------|--------------|-------|------------|
| patient\_ref | INT | fk | pseudonymized number that identifies a patient |
| episode\_ref | INT | fk | pseudonymized number that identifies an episode |
| ou\_loc\_ref | CHAR(8) | fk | physical hospitalization unit |
| ou\_med\_ref | CHAR(8) | fk | medical organizational unit |
| catalog | CHAR(10) | | 1 is ICD9; 12 is ICD10 |
| code | CHAR(10) | | procedure code |
| descr | CHAR(255) | | procedure description |
| text | CHAR(255) | | details about the procedure |
| place | CHAR(2) | | it specifies the location of the procedure: \*\*1\*\* (Bloque quirúrgico), \*\*2\*\* (Gabinete diagnóstico y terapéutico), \*\*3\*\* (Cirugía menor), \*\*4\*\* (Radiología intervencionista o medicina nuclear), \*\*5\*\* (Sala de no intervención), \*\*6\*\* (Bloque obstétrico), \*\*EX\*\* (Procedimiento externo) |
| class | CHAR(2) | | P (primary procedure), S (secondary procedure) |
| start\_date | DATETIME | | start date of the procedure |
| end\_date | DATETIME | | end date of the procedure |
| load\_date | DATETIME | | date and time of update |
---
# The g\_provisions table
Provisions are healthcare benefits. They are usually categorized into three levels: each level 1 class contains its own level 2 classes, and each level 2 class contains its own level 3 classes. However, this structure is not mandatory, so some provisions may not have any levels at all. In any case, each provision always has a code (prov\_ref) that identifies it.
The `g\_provisions` table contains the provisions for each episode:
 
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| patient\_ref | INT | fk | Pseudonymized number that identifies a patient. |
| episode\_ref | INT | fk | Pseudonymized number that identifies an episode. |
| ou\_med\_ref\_order | VARCHAR(8) | fk | Medical organizational unit that requests the provision; points to the dic\_ou\_med table. |
| prov\_ref | VARCHAR(32) | | Code that identifies the healthcare provision. |
| prov\_descr | VARCHAR(255) | | Description of the provision code. |
| level\_1\_ref | VARCHAR(16) | | Level 1 code; it may end with '\_inferido', which indicates that this level was not recorded in SAP but has been inferred from the context in SAP tables. |
| level\_1\_descr | VARCHAR(45) | | Level 1 code description. |
| level\_2\_ref | VARCHAR(3) | | Level 2 code. |
| level\_2\_descr | VARCHAR(55) | | Level 2 code description. |
| level\_3\_ref | VARCHAR(3) | | Level 3 code. |
| level\_3\_descr | VARCHAR(50) | | Level 3 code description. |
| category | INT | | Class of the provision:<br>• \*\*2\*\*: generic provisions;<br>• \*\*6\*\*: imaging diagnostic provisions. |
| start\_date | DATETIME | | Start date of the provision. |
| end\_date | DATETIME | | End date of the provision. |
| accession\_number | VARCHAR(10) | PK | The accession number is a unique identifier for each patient provision. For example, if a patient undergoes two ECGs on the same day, this will result in two separate provisions, each with its own accession number. This field links to the XNAT data repository. |
| ou\_med\_ref\_exec | VARCHAR(8) | fk | Medical organizational unit that executes the provision; points to the dic\_ou\_med table. |
| start\_date\_plan | DATETIME | | Scheduled start date of the provision. |
| end\_date\_plan | DATETIME | | Scheduled end date of the provision. |
---
# Credential generator
https://dsc.clinic.cat/
# Metabase
https://metabase.clinic.cat/
# Database connection
- database name: datascope4
- host / server: 172.26.6.27
- port: 3306
# Clinical History Retrieval System (CHRIS)
https://chris.clinic.cat
# Natural language querying (under development)
https://dsc.clinic.cat/natlang2sql
# Issues
https://gitlab.com/dsc-clinic/datascope/-/issues
# Download links
- MySQL Workbench: https://dev.mysql.com/downloads/workbench/
- R: https://ftp.cixug.es/CRAN/
- RStudio: https://posit.co/download/rstudio-desktop/
- Python: https://www.python.org/downloads/
 
# SAU tickets
https://gestiotiquets.clinic.cat/
---
[[\_TOC\_]]
# Tables
Tables are data structures organized by rows (each row is a record) and columns (each column is a feature of the record; columns are also called fields, variables or attributes).
![image](uploads/e6e4660b0c81ff3493026da0def40ef0/image.png)
A relational database is made up of several tables that are related to each other. Every table stores its own kind of information.
# Primary key
Each table has a primary key (PK), which is a field that uniquely identifies each row, so that the primary key cannot have repeated values or null values.
The image below represents a table (called g\_episodes) with its fields (episode\_ref, patient\_ref...); the primary key is highlighted:
<img src="uploads/eb64d9859c0a498949b0cd7a295d5642/image.png" width="130">
# Foreign key
Tables also contain foreign keys (fk), which are fields that reference another table (the foreign key of the referencing table holds the same domain as the field or column of the referenced table).
The image below represents two tables (g\_episodes and g\_demographics) with their fields (episode\_ref, patient\_ref...); a foreign key is highlighted:
<img src="uploads/66faf18e1eee785a733ac9c9b305722e/image.png" width="260">
A primary key can be simultaneously a foreign key if it refers to another table.
# Join
To join tables we use foreign keys. If field A1 (e.g., \_identity card number\_) in table A refers to field B1 (also \_identity card number\_) in table B, we can join these two tables by its common field (\_identity card number\_). This generates a new table, called \_joined table\_, where each row in the joined table represents a unique combination of data from the two tables based on the values in the common field, so if a value in the common field appears multiple times in one or both tables, the resulting joined table will include a row for each combination of the matching rows.
Main join types:
- Inner Join: only the rows with matching values in both tables are returned (for more technical details, see [SQL Tutorial with DataNex Examples, INNER JOIN](https://gitlab.com/dsc-clinic/datascope/-/wikis/SQL-Tutorial-with-DataNex-Examples#inner-join)).
- Left Join: returns all the rows from the left table and the matching rows from the right table (if there are any) and if there are no matching rows in the right table, the result set will contain null values in the columns from the right table; the left table is the table listed first (for more technical details, see [SQL Tutorial with DataNex Examples, LEFT JOIN](https://gitlab.com/dsc-clinic/datascope/-/wikis/SQL-Tutorial-with-DataNex-Examples#left-join)).
- Right Join: it is similar to a left join but returns all the rows from the right table and the matching rows from the left table (if there are any) and if there are no matching rows in the left table, the result set will contain null values in the columns from the left table; the right table is listed second (for more technical details, see [SQL Tutorial with DataNex Examples, RIGHT JOIN](https://gitlab.com/dsc-clinic/datascope/-/wikis/SQL-Tutorial-with-DataNex-Examples#right-join)).
To illustrate join types, let's use these two tables:
- Left table:
![image](uploads/92b578315bdf58ba9286c74582274e26/image.png)
- Right table:
![image](uploads/d3535eedff390630a0ae8804061d5c3b/image.png)
&nbsp;
So now let's show the inner, left and right joins derived from these two tables:
- Inner join:
![image](uploads/b5a65166d395a77661ac5977b69c3938/image.png)
- Left join:
![image](uploads/3b22f5928b76196aa26b90cc4e6f1357/image.png)
- Right join:
![image](uploads/4e283030d9c970a10b7abe62077a4957/image.png)
&nbsp;
Another join example (pay attention to row repetition from the left table):
- Left table:
![image](uploads/ec3aa28541d7bcf2a899d2565bcfdf20/image.png)
- Right table:
![image](uploads/ac09b671a4cc36906651d19f4723abec/image.png)
- Inner join:
![image](uploads/bec2b146f37b93e29c3dbf6d111e19dc/image.png)
---
[[\_TOC\_]]
&nbsp;
---
Index:
[[\_TOC\_]]
# The g\_special\_records table
Special records, also known as nursing records, are a specific type of dynamic form completed by nurses to collect clinical data in a structured manner. All of this data is recorded in the `g\_special\_records` table, where each special record appears as many times as it was saved in SAP. This is reflected in the `form\_date` variable, which stores the date or dates when the special record was saved.
The `g\_special\_records` table:
&nbsp;
| Attribute | Data type | Key | Definition |
| - | - | - | - |
| patient\_ref | INT | fk | Pseudonymized number that identifies a patient. |
| episode\_ref | INT | fk | Pseudonymized number that identifies an episode. |
| ou\_loc\_ref | CHAR(8) | fk | Physical hospitalization unit reference. |
| ou\_med\_ref | CHAR(8) | fk | Medical organizational unit reference. |
| status | CHAR(3) | | Record status:<br>• \*\*CO\*\*: completed;<br>• \*\*EC\*\*: in process. |
| form\_ref | CHAR(8) | | Form name identifier. |
| form\_descr | CHAR | | Form description. |
| tab\_ref | CHAR(10) | | Form tab (group) identifier. |
| tab\_descr | CHAR | | Tab description. |
| section\_ref | CHAR(10) | | Form section (parameter) identifier. |
| section\_descr | CHAR | | Section description. |
| type\_ref | CHAR(8) | | Form question (characteristic) identifier. |
| type\_descr | CHAR | | Characteristic description. |
| class\_ref | CHAR(3) | | Assessment class:<br>• \*\*RE\*\*: special record forms. |
| class\_descr | CHAR | | Class description. |
| value\_num | FLOAT | | Numeric value inserted. |
| value\_text | CHAR(255) | | Text value inserted. |
| value\_date | DATETIME | | Datetime value inserted. |
| form\_date | DATETIME | | Date when the form was saved. |
| load\_date | DATETIME | | Date of update. |
&nbsp;
# Descriptions for form, tab, section and type concepts
The following schema specifies the components of special records:
![FD2](uploads/ef9debd2c52ac0109a0fd481dd2bb839/FD2.PNG)
&nbsp;
---
# The g\_tags table
Tags are labels that some clinicians use to identify groups of patients.
We are not aware of the exact meaning of each tag and its maintenance; if any tag administrator wants to provide us with more information, we will include it in the wiki.
The `g\_tags` table contains the tags for each episode:
&nbsp;
| Attribute | Data type | Key | Definition |
| ------------ | --------- | --- | ----------------------------------------------- |
| patient\_ref | INT | fk | pseudonymized number that identifies a patient |
| episode\_ref | INT | fk | pseudonymized number that identifies an episode |
| tag\_ref | INT | fk | reference identifying the tag |
| tag\_group | CHAR | | tag group |
| tag\_subgroup | CHAR | | tag subgroup |
| tag\_descr | CHAR | | description of the tag reference |
| inactive\_atr | INT | | inactivity off (0) or on (1) |
| start\_date | DATETIME | | start date and time of the tag |
| end\_date | DATETIME | | end date and time of the tag |
| load\_date | DATETIME | | update date and time |
&nbsp;