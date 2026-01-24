# The g_administrations table
The `g_administrations` table contains the administered pharmaceuticals (drugs) for each episode. The `treatment_ref` field serves as a foreign key that links the `g_prescriptions`, `g_administrations` and `g_perfusions` tables.
The `g_administrations` table:
&nbsp;
| Attribute | Data type | Key | Definition |
|-------|--------------|-------|------------|
| patient_ref | INT | fk | pseudonymized number that identifies a patient |
| episode_ref | INT | fk | pseudonymized number that identifies an episode |
| treatment_ref | INT |  | code that identifies a treatment prescription |
| administration_date | DATE |  | date of administration |
| route_ref | INT | fk | administration route reference |
| route_descr | CHAR |  | description of route_ref |
| prn | CHAR |  | null value or "X"; the "X" indicates that this drug is administered only if needed |
| given | CHAR |  | null value or "X"; the "X" indicates that this drug has not been administered |
| not_given_reason_ref | INT |  | number that indicates the reason for non-administration |
| drug_ref | CHAR | fk | medical product identifier |
| drug_descr | CHAR |  | description of the drug_ref field |
| atc_ref | CHAR |  | ATC code |
| atc_descr | CHAR |  | description of the ATC code |
| enum | INT |  | role of the drug in the prescription (see complementary descriptions [**here**](https://gitlab.com/dsc-clinic/datascope/-/wikis/Prescriptions#complementary-descriptions), where `enum` equals `drug_type_ref`) |
| quantity | INT |  | dose actually administred to the patient|
| quantity_planing | INT |  | planned dose |
| quantity_unit | CHAR | fk | dose unit (see complementary descriptions [**here**](https://gitlab.com/dsc-clinic/datascope/-/wikis/Prescriptions#complementary-descriptions)) |
| load_date | DATETIME |  | date of update |
| care_level_ref | INT | fk | unique identifier that groups care levels (ICU, WARD, etc) if they are consecutive and belong to the same level |
&nbsp;
---
# The g_adm_disch table
The `g_adm_disch` table holds the reasons for admission and discharge per episode:
&nbsp;
| Attribute   | Data type   | Key | Definition                                                                                |
| ----------- | ----------- | --- | ----------------------------------------------------------------------------------------- |
| patient_ref  | INT       | fk  | pseudonymized number that identifies a patient                                                                                                                                                                             |
| episode_ref | INT         | fk  | pseudonymized number that identifies an episode                                                                 |
| mot_ref     | INT         | fk  | reason for admission or discharge (numeric) |
| mot_descr     | CHAR(32)  |        | description of the mot_ref                                         |
| mot_type    | VARCHAR(45) |     | it indicates if it is the starting motive (ST) or the ending motive (END) of the episode  |
| load_date   | DATETIME    |     | update date                                                                               |
&nbsp;
---
# The g_antibiograms table
The `g_antibiograms` table contains the antibiograms for each episode:
&nbsp;
| Attribute | Data type | Key | Definition |
|-------|--------------|-------|------------|
| patient_ref | INT | fk | pseudonymized number that identifies a patient |
| episode_ref | INT | fk | pseudonymized number that identifies an episode |
| extrac_date | DATETIME |  | date and time the sample was extracted |
| result_date | DATETIME |  | date and time the result was obtained |
| sample_ref | CHAR |  | code that identifies the type or origin of the sample |
| sample_descr | CHAR |  | description of the type or origin of the sample; it provides a general classification of the sample |
| antibiogram_ref | INT |  | unique identifier for the antibiogram |
| micro_ref | CHAR |  | code that identifies the microorganism |
| micro_descr | CHAR |  | scientific name of the microorganism |
| antibiotic_ref | CHAR |  | code of the antibiotic used in the sensitivity testing |
| antibiotic_descr | CHAR |  | full name of the antibiotic |
| result | CHAR |  | the result of the antibiotic sensitivity test; the value represents the minimum inhibitory concentration (MIC) required to inhibit the growth of the bacteria |
| sensitivity | CHAR |  | sensitivity (S) or resistance (R) of the bacteria to the antibiotic tested |
| load_date | DATETIME |  | date of update |
| care_level_ref | INT | fk | unique identifier that groups care levels (intensive care unit, conventional hospitalization, etc.) if they are consecutive and belong to the same level |
&nbsp;
---
# The g_rc table
The `g_rc` table contains the clinical records for each episode (currently, the fields `episode_ref` and `care_level_ref` are empty but they will be filled soon):
&nbsp;
| Attribute | Data type | Key | Definition |
|-------|--------------|-------|------------|
| patient_ref | INT | fk | pseudonymized number that identifies a patient |
| episode_ref | INT | fk | pseudonymized number that identifies an episode |
| result_date | DATETIME |  | date and time of the measurement |
| meas_type_ref | CHAR(1) |  | 0 (manual input), 1 (from machine, result not validated), 2 (from machine, result validated) |
| load_date | DATETIME |  | date of update |
| ou_loc_ref | CHAR(8) | fk | physical hospitalization unit; this cell is filled if the clinical registry is manually collected but it is left empty if the clinical registry is automatically collected |
| ou_med_ref | CHAR(8) | fk | medical organizational unit; this cell is filled if the clinical registry is manually collected but it is left empty if the clinical registry is automatically collected |
| rc_sap_ref | CHAR(16) |  | SAP clinical record reference |
| rc_descr | CHAR(32) |  | description of the SAP clinical record reference |
| result_num | FLOAT |  | numerical result of the clinical record |
| result_txt | VARCHAR(128) |  | text result from the DataNex clinical record reference; check its [**<ins>dictionary</ins>**](https://dsc-clinic.gitlab.io/datascope/rc_result_txt_dic.html) |
| units | CHAR(8) |  | units |
| care_level_ref | INT | fk | unique identifier that groups care levels (intensive care unit, conventional hospitalization, etc.) if they are consecutive and belong to the same level |
&nbsp;
---
# The g_demographics table
The `g_demographics` table contains demographic information for each patient:
&nbsp;
| Attribute | Data type | Key | Definition |
|-------|--------------|-------|------------|
| patient_ref | INT | PK | pseudonymized number that identifies a patient |
| birth_date | DATE |  | date of birth |
| sex | INT |  | -1 (not reported in SAP), 1 (male), 2 (female), 3 (other) |
| natio_ref | CHAR(8) | fk | reference code for nationality |
| natio_descr | CHAR(512) |  | description of the country code according to ISO:3 |
| health_area | CHAR |  | health area |
| postcode | CHAR |  | postal code |
| load_date | DATETIME |  | date of update |
&nbsp;
---
# A. The g_diagnostics table
| Attribute | Data type | Key | Definition |
| --- | --- | --- | --- |
| patient_ref | INT | fk | pseudonymized number that identifies a patient |
| episode_ref | INT | fk | pseudonymized number that identifies an episode |
| diag_date | DATETIME |  | diagnostic code registration date |
| diag_ref | INT | fk | DataNex own diagnosis reference number |
| catalog | INT |  | catalog to which the 'code' belongs. * 1 is CIE9 MC (until 2017) * 2 is MDC * 3 is CIE9 Emergencies * 4 is ACR * 5 is SNOMED * 7 is MDC-AP * 8 is SNOMEDCT * 9 is Subset ANP SNOMED CT * 10 is Subset ANP SNOMED ID * 11 is CIE9 in Outpatients * 12 is CIE10 MC * 13 is CIE10 Outpatients |
| code | CHAR(8) |  | ICD-9 or ICD-10 code for each diagnosis |
| diag_descr | CHAR(32) |  | description of the diagnosis |
| class | CHAR(2) |  | * **P** (code for primary diagnosis in hospitalization episodes validated by the documentalist) * **S** (code for secondary diagnosis in hospitalization episodes validated by the documentalist) * **H** (code for diagnosis in hospitalization episodes not validated by the documentalist) * **E** (code for diagnosis in emergency episodes) and * **A** (code for diagnosis in outpatient episodes) A hospitalization episode has only one P diagnosis and zero or more S or H diagnoses |
| poa | CHAR(2) |  | the Present on Admission (POA) indicator indicates whether the condition was present at admission (a comorbidity) or whether it arose during the hospitalization (a complication); options: * **Y** (Yes, present at the time of inpatient admission) * **N** (No, not present at the time of inpatient admission) * **U** (Unknown, documentation is insufficient to determine if condition is present on admission) * **W** (Clinically undetermined, provider is unable to clinically determine whether condition was present on admission or not) * **E** (Exempt) * **-** (Unreported, it means that the documentalist has not registered the diagnostic code) |
| load_date | DATETIME |  | date of update |
# B. The g_diagnostic_related_groups table
In this table are recorded the [Diagnosis-Related-Groups](https://en.wikipedia.org/wiki/Diagnosis-related_group) (DRG). DRG is a concept used to categorize hospital cases into groups according to diagnosis, procedures, age, comorbidities and other factors. These DRG are used mainly for administrative purposes, billing and resource allocation. DRG are further classified in Major Diagnostic Categories (MDC).
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| patient_ref | INT | fk | pseudonymized number that identifies a patient |
| episode_ref | INT | fk | pseudonymized number that identifies an episode |
| weight | FLOAT |  | drg cost weight, meaning the relative resource consumption for that group compared to others |
| drg_ref | INT | fk | drg (diagnosis-related group) reference |
| severity_ref | CHAR(2) | fk | soi (Severity of Illness) reference: a metric to evaluate how sick a patient is |
| severity_descr | CHAR(128) |  | description of the soi reference |
| mortality_risk_ref | CHAR(2) | fk | rom (Risk of Mortality) reference: a metric to evaluate the likelihood of a patient dying |
| mortality_risk_descr | CHAR(128) |  | description of the rom reference |
| mdc_ref | INT | fk | mdc (Major Diagnostic Categories) reference: those are broad categories used to group DRG based on similar clinical conditions or body systems |
| load_date | DATETIME |  | date of update |
---
# The g_dynamic_forms table
Dynamic forms collect clinical data in a structured manner. All of this data is recorded in the `g_dynamic_forms` table, where each dynamic form and its characteristics appear as many times as the form was saved in SAP. This is reflected in the `form_date` variable, which stores the date or dates when the form was saved.
The `g_dynamic_forms` table:
&nbsp;
| Attribute | Data type | Key | Definition |
| - | - | - | - |
| patient_ref | INT | fk | Pseudonymized number that identifies a patient. |
| episode_ref | INT | fk | Pseudonymized number that identifies an episode. |
| ou_loc_ref | CHAR(8) | fk | Physical hospitalization unit reference. |
| ou_med_ref | CHAR(8) | fk | Medical organizational unit reference. |
| status | CHAR(3) |  | Record status:<br>• **CO**: completed;<br>• **EC**: in process. |
| form_ref | CHAR(8) |  | Form name identifier. |
| form_descr | CHAR |  | Form description. |
| tab_ref | CHAR(10) |  | Form tab (group) identifier. |
| tab_descr | CHAR |  | Tab description. |
| section_ref | CHAR(10) |  | Form section (parameter) identifier. |
| section_descr | CHAR |  | Section description. |
| type_ref | CHAR(8) |  | Form question (characteristic) identifier. |
| type_descr | CHAR |  | Characteristic description. |
| class_ref | CHAR(3) |  | Assessment class:<br>• **CC**: structured clinical course forms;<br>• **EF**: physical examination forms;<br>• **ES**: scale forms;<br>• **RG**: record or report forms;<br>• **RE**: special record forms;<br>• **VA**: assessment forms;<br>• **TS**: social work forms. |
| class_descr | CHAR |  | Class description. |
| value_num | FLOAT |  | Numeric value inserted. |
| value_text | CHAR(255) |  | Text value inserted. |
| value_date | DATETIME |  | Datetime value inserted. |
| form_date | DATETIME |  | Date when the form was saved. |
| load_date | DATETIME |  | Date of update. |
&nbsp;
# Descriptions for form, tab, section and type concepts
The following schema specifies the components of the dynamic forms:
![FD2](uploads/ef9debd2c52ac0109a0fd481dd2bb839/FD2.PNG)
&nbsp;
---
# The g_encounters table
An encounter refers to a punctual event in which detailed information is recorded about a medical interaction or procedure involving a patient (for instance a chest radiograph, an outpatient visit, etc).
The dictionaries of the `encounter_type`, `agen_ref` and `act_type_ref` fields will be available in the next updates.
The `g_encounters` table contains the encounters for each episode:
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| patient_ref | INT | fk | pseudonymized number that identifies a patient |
| episode_ref | INT | fk | pseudonymized number that identifies an episode |
| date | DATETIME |  | date of the encounter event |
| load_date | DATETIME |  | update date |
| ou_med_ref | CHAR(8) | fk | medical organizational unit reference; points to the ou_med_dic table |
| ou_loc_ref | CHAR(8) | fk | physical hospitalization unit reference; points to the ou_loc_dic table |
| encounter_type | CHAR(8) | fk | encounter type |
| agen_ref | CHAR | fk | code that identifies the encounter |
| act_type_ref | CHAR(8) | fk | activity type |
&nbsp;
The dictionary for encounter_type is:
| Code | Description          |
|--------|---------------------|
| 2O     | 2ª opinión          |
| AD     | Hosp. día domic.    |
| BO     | Blog. obstétrico    |
| CA     | Cirugía mayor A     |
| CM     | Cirugía menor A     |
| CU     | Cura                |
| DH     | Derivación hosp     |
| DI     | Der. otros serv.    |
| DU     | Derivación urg.     |
| EI     | Entrega ICML        |
| HD     | Hospital de día     |
| IC     | Interconsulta       |
| IH     | Servicio final      |
| IQ     | Interv. quir.       |
| LT     | Llamada telef.      |
| MA     | Copia mater.        |
| MO     | Morgue              |
| NE     | Necropsia           |
| PA     | Preanestesia        |
| PD     | Posible donante     |
| PF     | Pompas fúnebres     |
| PP     | Previa prueba       |
| PR     | Prueba              |
| PV     | Primera vista       |
| RE     | Recetas             |
| SM     | Sec. multicentro    |
| TR     | Tratamiento         |
| UD     | Urg. hosp. día      |
| UR     | Urgencias           |
| VD     | Vis. domicilio      |
| VE     | V. Enf. Hospital    |
| VU     | Vista URPA          |
| VS     | Vista sucesiva      |
| VU     | Vista urgencias     |
---
# The g_exitus table
The `g_exitus` table contains the date of death for each patient:
&nbsp;
| Attribute | Data type | Key | Definition |
|-------|--------------|-------|------------|
| patient_ref | INT | PK | pseudonymized number that identifies a patient |
| exitus_date | DATE |  | date of death |
| load_date | DATETIME |  | date and time of update |
---
# The g_health_issues table
The `g_health_issues` table contains information about all the health problems related to a patient. Health problems are SNOMED-CT (Systematized Nomenclature of Medicine Clinical Terms) codified health problems that a patient may present. SNOMED is a comprehensive multilingual clinical terminology used worlwide in healthcare. Those health problems are codified by the doctors taking care of the patients, thus expanding and enriching the codification possibilities.
Health problems have a start date, indicating when they were first recorded by the clinician, and may also have an end date, marking when the clinician determined the health problem was no longer active. The `end_motive` field records the reason for the change in this status.
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| patient_ref | INT | fk | pseudonymized number that identifies a patient |
| episode_ref | INT | fk | pseudonymized number that identifies an episode |
| snomed_ref | INT |  | SNOMED code for a health problem |
| snomed_descr | CHAR(255) |  | description of the SNOMED code |
| ou_med_ref | CHAR(8) | fk | medical organizational unit reference |
| start_date | DATE |  | start date of the health problem |
| end_date | DATE |  | end date of the health problem (not mandatory) |
| end_motive | INT |  | reason for the change (not mandatory) |
| load_date | DATETIME |  | date of update |
---
# The g_labs table
The `g_labs` table contains the laboratory tests for each episode:
&nbsp;
| Attribute | Data type | Key | Definition |
|-------|--------------|-------|------------|
| patient_ref | INT | fk | pseudonymized number that identifies a patient |
| episode_ref | INT | fk | pseudonymized number that identifies an episode |
| extrac_date | DATETIME |  | date and time the sample was extracted |
| result_date | DATETIME |  | date and time the result was obtained |
| load_date | DATETIME |  | date of update |
| ou_med_ref | CHAR(8) | fk | medical organizational unit |
| care_level_ref | INT | fk | unique identifier that groups care levels (ICU, WARD, etc) if they are consecutive and belong to the same level; the care_level_ref is absent if the lab test is requested after the end of the episode in EM, HOSP and HAH episodes |
| lab_sap_ref | CHAR(16) | fk | SAP laboratory parameter reference |
| lab_descr | CHAR(32) |  | lab_sap_ref description |
| result_num | FLOAT |  | numerical result of the laboratory test |
| result_txt | VARCHAR(128) |  | text result from the DataNex laboratory reference |
| units | CHAR(32) |  | units |
| lab_group_ref | INT |  | reference for grouped laboratory parameters |
&nbsp;
---
# The g_micro table
The `g_micro` table contains the microbiology results for each episode:
&nbsp;
| Attribute | Data type | Key | Definition |
|-------|--------------|-------|------------|
| patient_ref | INT | fk | pseudonymized number that identifies a patient |
| episode_ref | INT | fk | pseudonymized number that identifies an episode |
| extrac_date | DATETIME |  | date and time the sample was extracted |
| res_date | DATETIME |  | date and time the result was obtained |
| ou_med_ref | CHAR(8) | fk | medical organizational unit |
| mue_ref | CHAR |  | code that identifies the type or origin of the sample |
| mue_descr | CHAR |  | description of the type or origin of the sample; it provides a general classification of the sample |
| method_descr | CHAR |  | detailed description of the sample itself or the method used to process the sample; it includes specific procedures and tests performed |
| positive | CHAR |  | 'X' means that a microorganism has been detected in the sample |
| antibiogram_ref | INT |  | unique identifier for the antibiogram |
| micro_ref | CHAR |  | code that identifies the microorganism |
| micro_descr | CHAR |  | scientific name of the microorganism |
| num_micro | INT |  | a number that starts at 1 for the first identified microbe and increments by 1 unit for each newly identified microbe in the sample |
| result_text | VARCHAR(128) |  | text result from the microbiology sample |
| load_date | DATETIME |  | date of update |
| care_level_ref | INT | fk | unique identifier that groups care levels (intensive care unit, conventional hospitalization, etc.) if they are consecutive and belong to the same level |
&nbsp;
---
# Overview
DataNex is a database made up of several tables. Keeping information in different tables allows us to reduce storage space and group that information by topic.
The central tables in DataNex are g_episodes, g_care_levels and g_movements:
- Episodes are medical events experienced by a patient: an admission (planned or from the emergency department), an assessment in the emergency department, a set of visits for a medical specialty in outpatients, etc. The [**g_episodes**](https://gitlab.com/dsc-clinic/datascope/-/wikis/Episodes,-care-levels-and-movements#a-the-g_episodes-table) table stores these episodes.
- Care level refers to the intensity of healthcare needs that a patient requires. The [**g_care_levels**](https://gitlab.com/dsc-clinic/datascope/-/wikis/Episodes,-care-levels-and-movements#b-the-g_care_levels-table) table stores the care levels for each episode.
- Movements are changes in the patient's location. The [**g_movements**](https://gitlab.com/dsc-clinic/datascope/-/wikis/Episodes,-care-levels-and-movements#c-the-g_movements-table) table stores the movements for each care level.
These three central tables follow a hierarchy: episodes hold care levels and care levels hold movements.
&nbsp;
The central tables are linked to the peripheral tables, which are:
- The [**g_adm_disch**](https://gitlab.com/dsc-clinic/datascope/-/wikis/Admission-and-discharge-reasons) table holds the reasons for admission and discharge per episode.
- The [**g_diagnostics**](https://gitlab.com/dsc-clinic/datascope/-/wikis/Diagnoses-and-DRG#a-the-g_diagnostics-table) and [**g_diagnostic_related_groups**](https://gitlab.com/dsc-clinic/datascope/-/wikis/Diagnoses-and-DRG#b-the-g_diagnostic_related_groups-table) tables contain information about the diagnoses and the diagnosis-related group (DRG) for each episode, respectively.
- The [**g_labs**](https://gitlab.com/dsc-clinic/datascope/-/wikis/Laboratory) table contains the laboratory tests for each episode.
- The [**g_micro**](https://gitlab.com/dsc-clinic/datascope/-/wikis/Microbiology) table contains the microbiology results for each episode.
- The [**g_antibiograms**](https://gitlab.com/dsc-clinic/datascope/-/wikis/Antibiograms) table contains the antibiograms for each episode.
- The [**g_rc**](https://gitlab.com/dsc-clinic/datascope/-/wikis/Clinical-records) table contains the clinical records for each episode.
- The [**g_prescriptions**](https://gitlab.com/dsc-clinic/datascope/-/wikis/Prescriptions) table contains the prescribed medical products, which are pharmaceuticals (drugs) and medical devices, for each episode.
- The [**g_administrations**](https://gitlab.com/dsc-clinic/datascope/-/wikis/Administrations) table contains the administered pharmaceuticals (drugs) for each episode.
- The [**g_perfusions**](https://gitlab.com/dsc-clinic/datascope/-/wikis/Perfusions) table contains data about the administered drug perfusions for each episode.
- The [**g_encounters**](https://gitlab.com/dsc-clinic/datascope/-/wikis/Encounters) table: an encounter refers to a specific instance or event in which detailed information is recorded about a medical interaction or procedure involving a patient, for instance a chest radiograph; this table contains the encounters for each episode.
- The [**g_demographics**](https://gitlab.com/dsc-clinic/datascope/-/wikis/Demography) table contains demographic information for each patient.
- The [**g_exitus**](https://gitlab.com/dsc-clinic/datascope/-/wikis/Exitus) table contains the date of death for each patient.
- The [**g_tags**](https://gitlab.com/dsc-clinic/datascope/-/wikis/Tags) table: tags are labels used to identify groups of patients; this table contains the tags for each episode.
---
# A. The g_pathology_sample table
It contains all Pathology samples and their descriptions for each case.
The `g_pathology_sample` table:
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| patient_ref | INT | fk | Pseudonymized number that identifies a patient. |
| episode_ref | INT | fk | Pseudonymized number that identifies an episode. |
| case_ref | CHAR | fk | Case reference. |
| case_date | DATETIME |  | Date of the case. |
| sample_ref | CHAR | fk | Sample reference (a case holds one or more samples). |
| sample_descr | CHAR |  | Sample description. |
| validated_by | INT |  | Employee who validated the sample. |
# B. The g_pathology_diagnostic table
It contains all Pathology diagnoses associated with each case.
The `g_pathology_diagnostic` table:
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| patient_ref | INT | fk | Pseudonymized number that identifies a patient. |
| episode_ref | INT | fk | Pseudonymized number that identifies an episode. |
| case_ref | CHAR | fk | Case reference. |
| case_date | DATETIME |  | Date of the case. |
| sample_ref | CHAR | fk | Sample reference (a case holds one or more samples). |
| diag_type | CHAR |  | Type of diagnosis. |
| diag_code | INT |  | Diagnosis code. |
| diag_date | DATETIME |  | Diagnosis date. |
| diag_descr | CHAR |  | Diagnosis description. |
| validated_by | INT |  | Employee who validated the sample. |
---
# The g_perfusions table
The `g_perfusions` table contains data about the administered drug perfusions for each episode. The `treatment_ref` field serves as a foreign key that links the `g_prescriptions`, `g_administrations` and `g_perfusions` tables.
The `g_perfusions` table:
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| patient_ref | INT | fk | pseudonymized number that identifies a patient |
| episode_ref | INT | fk | pseudonymized number that identifies an episode |
| treatment_ref | INT |  | code that identifies a treatment prescription. Points to the `treatment_ref` in the `g_administrations` and `g_prescriptions` tables |
| infusion_rate | INT |  | rate in ml/h |
| rate_change_counter | INT |  | perfusion rate change counter: starts at 1 (first rate) and increments by one unit with each change (each new rate) |
| start_date | DATETIME |  | start date of the perfusion |
| end_date | DATETIME |  | end date of the perfusion |
| load_date | DATETIME |  | date of update |
| care_level_ref | INT | fk | unique identifier that groups care levels (ICU, WARD, etc) if they are consecutive and belong to the same level |
---
# The g_prescriptions table
The `g_prescriptions` table contains the prescribed medical products, which are pharmaceuticals (drugs) and medical devices, for each episode. A treatment prescription (identified by `treatment_ref`) may be composed by one or more medical products so this table will show as many rows as prescribed medical products per treatment prescription. The `treatment_ref` field serves as a foreign key that links the `g_prescriptions`, `g_administrations` and `g_perfusions` tables.
The `g_prescriptions` table:
&nbsp;
| Attribute | Data type | Key | Definition |
|-------|--------------|-------|------------|
| patient_ref | INT | fk | pseudonymized number that identifies a patient |
| episode_ref | INT | fk | pseudonymized number that identifies an episode |
| treatment_ref | INT |  | code that identifies a treatment prescription |
| prn | CHAR |  | null value or "X"; the "X" indicates that this drug is administered only if needed |
| freq_ref | CHAR | fk | administration frequency code |
| phform_ref | INT | fk | pharmaceutical form identifier |
| phform_descr | CHAR |  | description of phform_ref |
| prescr_env_ref | INT | fk | healthcare setting where the prescription was generated (complementary descriptions below) |
| adm_route_ref | INT | fk | administration route reference |
| route_descr | CHAR |  | description of adm_route_ref |
| atc_ref | CHAR |  | ATC code |
| atc_descr | CHAR |  | description of the ATC code |
| ou_loc_ref | CHAR(8) | fk | physical hospitalization unit |
| ou_med_ref | CHAR(8) | fk | medical organizational unit |
| start_drug_date | DATETIME |  | start date of prescription validity |
| end_drug_date | DATETIME |  | end date of prescription validity |
| load_date | DATETIME |  | date of update |
| drug_ref | CHAR | fk | medical product identifier |
| drug_descr | CHAR |  | description of the drug_ref field |
| enum | INT |  | role of the drug in the prescription (complementary descriptions below, where `enum` equals `drug_type_ref`) |
| dose | INT |  | prescribed dose |
| unit | CHAR | fk | dose unit (complementary descriptions below) |
| care_level_ref | INT | fk | unique identifier that groups care levels (ICU, WARD, etc) if they are consecutive and belong to the same level |
&nbsp;
# Complementary descriptions
The table is complemented by:
---
# The g_procedures table
The `g_procedures` table contains all procedures per episode:
&nbsp;
| Attribute | Data type | Key | Definition |
|-------|--------------|-------|------------|
| patient_ref | INT | fk | pseudonymized number that identifies a patient |
| episode_ref | INT | fk | pseudonymized number that identifies an episode |
| ou_loc_ref | CHAR(8) | fk | physical hospitalization unit |
| ou_med_ref | CHAR(8) | fk | medical organizational unit |
| catalog | CHAR(10) |  | 1 is ICD9; 12 is ICD10 |
| code | CHAR(10) |  | procedure code |
| descr | CHAR(255) |  | procedure description |
| text | CHAR(255) |  | details about the procedure |
| place | CHAR(2) |  | it specifies the location of the procedure: **1** (Bloque quirúrgico), **2** (Gabinete diagnóstico y terapéutico), **3** (Cirugía menor), **4** (Radiología intervencionista o medicina nuclear), **5** (Sala de no intervención), **6** (Bloque obstétrico), **EX** (Procedimiento externo) |
| class | CHAR(2) |  | P (primary procedure), S (secondary procedure) |
| start_date | DATETIME |  | start date of the procedure |
| end_date | DATETIME |  | end date of the procedure |
| load_date | DATETIME |  | date and time of update |
---
# The g_provisions table
Provisions are healthcare benefits. They are usually categorized into three levels: each level 1 class contains its own level 2 classes, and each level 2 class contains its own level 3 classes. However, this structure is not mandatory, so some provisions may not have any levels at all. In any case, each provision always has a code (prov_ref) that identifies it.
The `g_provisions` table contains the provisions for each episode:
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| patient_ref | INT | fk | Pseudonymized number that identifies a patient. |
| episode_ref | INT | fk | Pseudonymized number that identifies an episode. |
| ou_med_ref_order | VARCHAR(8) | fk | Medical organizational unit that requests the provision; points to the dic_ou_med table. |
| prov_ref | VARCHAR(32) |  | Code that identifies the healthcare provision. |
| prov_descr | VARCHAR(255) |  | Description of the provision code. |
| level_1_ref | VARCHAR(16) |  | Level 1 code; it may end with '_inferido', which indicates that this level was not recorded in SAP but has been inferred from the context in SAP tables. |
| level_1_descr | VARCHAR(45) |  | Level 1 code description. |
| level_2_ref | VARCHAR(3) |  | Level 2 code. |
| level_2_descr | VARCHAR(55) |  | Level 2 code description. |
| level_3_ref | VARCHAR(3) |  | Level 3 code. |
| level_3_descr | VARCHAR(50) |  | Level 3 code description. |
| category | INT |  | Class of the provision:<br>• **2**: generic provisions;<br>• **6**: imaging diagnostic provisions. |
| start_date | DATETIME |  | Start date of the provision. |
| end_date | DATETIME |  | End date of the provision. |
| accession_number | VARCHAR(10) | PK | The accession number is a unique identifier for each patient provision. For example, if a patient undergoes two ECGs on the same day, this will result in two separate provisions, each with its own accession number. This field links to the XNAT data repository. |
| ou_med_ref_exec | VARCHAR(8) | fk | Medical organizational unit that executes the provision; points to the dic_ou_med table. |
| start_date_plan | DATETIME |  | Scheduled start date of the provision. |
| end_date_plan | DATETIME |  | Scheduled end date of the provision. |
---
# The g_special_records table
Special records, also known as nursing records, are a specific type of dynamic form completed by nurses to collect clinical data in a structured manner. All of this data is recorded in the `g_special_records` table, where each special record appears as many times as it was saved in SAP. This is reflected in the `form_date` variable, which stores the date or dates when the special record was saved.
The `g_special_records` table:
&nbsp;
| Attribute | Data type | Key | Definition |
| - | - | - | - |
| patient_ref | INT | fk | Pseudonymized number that identifies a patient. |
| episode_ref | INT | fk | Pseudonymized number that identifies an episode. |
| ou_loc_ref | CHAR(8) | fk | Physical hospitalization unit reference. |
| ou_med_ref | CHAR(8) | fk | Medical organizational unit reference. |
| status | CHAR(3) |  | Record status:<br>• **CO**: completed;<br>• **EC**: in process. |
| form_ref | CHAR(8) |  | Form name identifier. |
| form_descr | CHAR |  | Form description. |
| tab_ref | CHAR(10) |  | Form tab (group) identifier. |
| tab_descr | CHAR |  | Tab description. |
| section_ref | CHAR(10) |  | Form section (parameter) identifier. |
| section_descr | CHAR |  | Section description. |
| type_ref | CHAR(8) |  | Form question (characteristic) identifier. |
| type_descr | CHAR |  | Characteristic description. |
| class_ref | CHAR(3) |  | Assessment class:<br>• **RE**: special record forms. |
| class_descr | CHAR |  | Class description. |
| value_num | FLOAT |  | Numeric value inserted. |
| value_text | CHAR(255) |  | Text value inserted. |
| value_date | DATETIME |  | Datetime value inserted. |
| form_date | DATETIME |  | Date when the form was saved. |
| load_date | DATETIME |  | Date of update. |
&nbsp;
# Descriptions for form, tab, section and type concepts
The following schema specifies the components of special records:
![FD2](uploads/ef9debd2c52ac0109a0fd481dd2bb839/FD2.PNG)
&nbsp;
---
# A. The g_surgery table
This table contains general information about the surgical procedures.
The `g_surgery` table:
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| patient_ref | INT | fk | Pseudonymized number that identifies a patient. |
| episode_ref | INT | fk | Pseudonymized number that identifies an episode. |
| mov_ref | INT | fk | Reference that joins the surgery with its movement. |
| ou_med_ref | CHAR | fk | Medical organizational unit reference. |
| ou_loc_ref | CHAR | fk | Physical hospitalization unit reference. |
| operating_room | CHAR |  | Assigned operating room. |
| start_date | DATETIME |  | When the surgery starts. |
| end_date | DATETIME |  | When the surgery ends. |
| surgery_ref | INT | fk | Number that identifies a surgery; it links to other Surgery tables. |
| surgery_code | CHAR |  | Standard code for the surgery. Local code named Q codes|
| surgery_code_descr | CHAR |  | Surgery code description. |
surgery_code is the Hospital Clinic local code for surgeries. The codes start with Q followed by numbers. Ex: surgery_code Q01972, surgery_code_descr: injeccio intravitria.
# B. The g_surgery_team table
It contains information about surgical tasks performed during surgical procedures.
The `g_surgery_team` table:
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| patient_ref | INT | fk | Pseudonymized number that identifies a patient. |
| episode_ref | INT | fk | Pseudonymized number that identifies an episode. |
| surgery_ref | INT | fk | Number that identifies a surgery; it links to other Surgery tables. |
| task_ref | CHAR |  | Code that identifies the surgical task. |
| task_descr | CHAR |  | Description of the surgical task. |
| employee | INT |  | Employee who performed the task. |
# C. The g_surgery_timestamps table
This table stores the timestamps of surgical events for each surgical procedure.
The `g_surgery_timestamps` table:
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| patient_ref | INT | fk | Pseudonymized number that identifies a patient. |
| episode_ref | INT | fk | Pseudonymized number that identifies an episode. |
| event_label | CHAR |  | Surgical event code. |
| event_descr | CHAR |  | Description of the surgical event. |
| event_timestamp | DATETIME |  | Timestamp indicating when the surgical event happened. |
| surgery_ref | INT | fk | Number that identifies a surgery; it links to other Surgery tables. |
# D. The g_surgery_waiting_list table
It contains the waiting list information for requested surgical procedures.
The `g_surgery_waiting_list` table:
| Attribute | Data type | Key | Definition |
|-----------|-----------|-----|------------|
| patient_ref | INT | fk | Pseudonymized number that identifies a patient. |
| episode_ref | INT | fk | Pseudonymized number that identifies an episode. |
| surgeon_code | INT |  | Code identifying the surgeon |
| waiting_list | CHAR |  | Name of the waiting list. |
| planned_date | DATETIME |  | Scheduled date and time of the surgical intervention. |
| proc_ref | CHAR |  | Procedure code. |
| registration_date | DATETIME |  | Date and time when the patient was registered on the waiting list. |
| requesting_physician | INT |  | Physician who requested the surgery. |
| priority | INT |  | Priority assigned to the patient in the waiting list. |
---
# The g_tags table
Tags are labels that some clinicians use to identify groups of patients.
We are not aware of the exact meaning of each tag and its maintenance; if any tag administrator wants to provide us with more information, we will include it in the wiki.
The `g_tags` table contains the tags for each episode:
&nbsp;
| Attribute    | Data type | Key | Definition                                      |
| ------------ | --------- | --- | ----------------------------------------------- |
| patient_ref  | INT       | fk  | pseudonymized number that identifies a patient  |
| episode_ref  | INT       | fk  | pseudonymized number that identifies an episode |
| tag_ref      | INT       | fk  | reference identifying the tag                   |
| tag_group    | CHAR      |     | tag group                                         |
| tag_subgroup | CHAR      |     | tag subgroup                                         |
| tag_descr        | CHAR      |     | description of the tag reference |
| inactive_atr | INT       |     | inactivity off (0) or on (1)                   |
| start_date   | DATETIME |     | start date and time of the tag                  |
| end_date     | DATETIME |     | end date and time of the tag                    |
| load_date    | DATETIME |     | update date and time                            |
&nbsp;
---
# Home
<div>
![DataNex](uploads/51add36de341521f87f3fd3373541286/image.png){height="100"} ![Clínic Barcelona](uploads/7e64cac371bb227839f18303c5dca8ec/image.png){height="100"}
</div>![visitors](https://visitor-badge.laobi.icu/badge?page_id=dsc-clinic.datascope.wiki.home)
# Welcome to DataNex, a platform that gives you acces to Datascope, the data warehouse of Hospital Clínic Barcelona.
<details>
<summary>
:rocket: Introduction
</summary>
DataNex is accessible to physicians and nurses contracted by Hospital Clínic and to investigators affiliated with Campus Clinic.
Please note that the **data is pseudonymized**; therefore, the actual patient identifier (NHC) and episode number are not displayed in the database; instead, masked numbers have been assigned to replace these values.
To access the database, use an institutional computer, VDI or VPN and go to the [Datascope webpage](https://dsc.clinic.cat/) and sign in using your institutional Office356 email and password to obtain the credentials (more information is available [here](https://gitlab.com/dsc-clinic/datascope/-/wikis/Access-Instructions#3-datascope)).
All wiki content is organized and accessible through the index on the left.
![Captura de pantalla 2025-03-26 145616.png](uploads/9edc229172648a84d57f56df86bf3002/Captura_de_pantalla_2025-03-26_145616.png){width="2167" height="1326"}
In the Datanex **data loading process** we upload all patient's episodes that started between two Index Dates. An episode can be hospitalary, outpatient, etc, and includes all data generated during that interaction. Episodes are loaded into Datanex following this logic: an Index Date and an End Index Date are chosen and all the new episodes and movements within those two dates are loaded into Datanex. A movement is each single granular sanitary interaction within an episode (a single visit to the ED, an admission to the ICU, etc). Data generated before the Index Date or after the End Index Date will not be available in Datanex. Data of episodes beyond the End Index Date will be uploaded in the next forward uploading cycles. Data of episodes created before the Index Date will be uploaded in next backward uploading cycle, dragging all data created between the Index Date and the End Index Date.
![Screenshot 2025-03-05 at 10.06.51.png](uploads/187135bd1f93ff0f2e1231d53cf305b6/Screenshot_2025-03-05_at_10.06.51.png)
We are working hard to increase the time period of the database. If there are some doubts about the data availability, please refer to the [Catalog](https://dsc-clinic.gitlab.io/datascope/catalog_notebook.html) and you can ask questions in the [Issues](https://gitlab.com/dsc-clinic/datascope/-/issues) section. We will be pleased to answer them.
</details>
<details>
<summary>
:bar_chart: Available data
</summary>
Please visit our [**Catalog**](https://dsc-clinic.gitlab.io/datascope/catalog_notebook.html).
</details>
<details>
<summary>
:loudspeaker: News
</summary>
Please visit our [**News page**](https://gitlab.com/dsc-clinic/datascope/-/wikis/News).
</details>
<details>
<summary>
:mortar_board: Aula Oberta Datanex (on Wednesdays at 2 PM)
</summary>
Join us every Wednesday at 14:00 in [**this Teams meeting**](https://teams.microsoft.com/meet/327740190513?p=zg633JrCrhs4BQCc5k) to answer questions and participate in data mining examples. The meeting will **end at 14:30 if no one joins**.
</details>