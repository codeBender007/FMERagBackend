"""Physical MSSQL schema catalog for the FME / Furukawa LMS Text-to-SQL agent.

AUTO-GENERATED from the database structure dump supplied on 2026-09-19.
This file deliberately avoids inferred/hallucinated columns.
"""

TABLE_CATALOG = r"""FME / Furukawa LMS PHYSICAL MSSQL SCHEMA
Source of truth: database structure dump supplied on 2026-09-19.
RULE: Column/table names below are physical identifiers. Do not invent identifiers not listed here.

========================================================================
TABLE: abnormal_condition_sheets
PRIMARY KEY: id
FOREIGN KEYS:
- departmentId -> departments(id)
COLUMNS:
- id (int; PK, NOT NULL)
- departmentId (int; FK->departments(id), NOT NULL)
- date (date; NOT NULL)
- entries (nvarchar(MAX); NULL)
- signatures (nvarchar(MAX); NULL)
- metadata (nvarchar(MAX); NULL)
- isSubmitted (bit; NULL)
- updatedBy (nvarchar(255); NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: AIChatMessage
PRIMARY KEY: id
FOREIGN KEYS:
- session_id -> AIChatSessions(id)
COLUMNS:
- id (int; PK, NOT NULL)
- session_id (varchar(50); FK->AIChatSessions(id), NOT NULL)
- sender (varchar(10); NOT NULL)
- message_text (varchar(MAX); NOT NULL)
- sql_executed (varchar(MAX); NULL)
- created_at (datetime; NULL)

========================================================================
TABLE: AIChatSessions
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (varchar(50); PK, NOT NULL)
- user_id (int; NOT NULL)
- title (varchar(255); NOT NULL)
- created_at (datetime; NULL)

========================================================================
TABLE: assignments
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- courseId (int; NOT NULL)
- moduleId (int; NULL)
- lessonId (int; NULL)
- scope (nvarchar(50); NOT NULL)
- instructor (int; NULL)
- title (nvarchar(255); NOT NULL)
- description (nvarchar(MAX); NULL)
- resources (nvarchar(MAX); NULL)
- dueDate (datetime; NOT NULL)
- maxScore (int; NULL)
- allowResubmission (bit; NULL)
- status (nvarchar(50); NULL)
- createdBy (int; NOT NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: attempt_extension_requests
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- quiz (nvarchar(255); NOT NULL)
- student (nvarchar(255); NOT NULL)
- reason (nvarchar(MAX); NULL)
- status (nvarchar(50); NULL)
- reviewedBy (nvarchar(255); NULL)
- reviewedAt (datetime; NULL)
- extraAttemptsGranted (int; NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: attempted_quizzes
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- quiz (nvarchar(255); NOT NULL)
- student (nvarchar(255); NOT NULL)
- answer (nvarchar(MAX); NULL)
- score (int; NULL)
- status (nvarchar(50); NULL)
- startedAt (datetime; NULL)
- completedAt (datetime; NULL)
- attemptNumber (int; NULL)
- timeTaken (int; NULL)
- manuallyAdjusted (bit; NULL)
- adjustedBy (nvarchar(255); NULL)
- adjustedAt (datetime; NULL)
- adjustmentNotes (nvarchar(MAX); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- conductedBy (nvarchar(255); NULL)
- studentName (nvarchar(255); NULL)
- studentEmpId (nvarchar(255); NULL)
- studentIsTemporary (bit; NULL)
- studentDeptId (int; NULL)
- studentSectionId (int; NULL)
- studentLineId (int; NULL)
- studentSubSectionId (int; NULL)

========================================================================
TABLE: attendance_logs
PRIMARY KEY: id
FOREIGN KEYS:
- userId -> users(id)
COLUMNS:
- id (int; PK, NOT NULL)
- userId (int; FK->users(id), NOT NULL)
- payCode (nvarchar(50); NULL)
- cardNo (nvarchar(50); NULL)
- employeeName (nvarchar(255); NULL)
- date (date; NOT NULL)
- department (nvarchar(100); NULL)
- designation (nvarchar(100); NULL)
- shift (nvarchar(50); NULL)
- startTime (time; NULL)
- inTime (time; NULL)
- outTime (time; NULL)
- hrsWorked (decimal(5,2); NULL)
- status (nvarchar(20); NOT NULL)
- lateArrival (decimal(5,2); NULL)
- earlyDeparture (decimal(5,2); NULL)
- otHrs (decimal(5,2); NULL)
- otAmount (decimal(10,2); NULL)
- updatedBy (int; NULL)
- updatedByRole (nvarchar(50); NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: attendance_unmapped_logs
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- payCode (nvarchar(100); NULL)
- cardNo (nvarchar(100); NULL)
- employeeName (nvarchar(510); NULL)
- date (date; NOT NULL)
- department (nvarchar(200); NULL)
- designation (nvarchar(200); NULL)
- shift (nvarchar(100); NULL)
- startTime (time; NULL)
- inTime (time; NULL)
- outTime (time; NULL)
- hrsWorked (decimal(5,2); NULL)
- status (nvarchar(40); NOT NULL)
- lateArrival (decimal(5,2); NULL)
- earlyDeparture (decimal(5,2); NULL)
- otHrs (decimal(5,2); NULL)
- otAmount (decimal(10,2); NULL)
- reason (nvarchar(255); NULL)
- createdAt (datetime; NULL)

========================================================================
TABLE: audits
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- user (nvarchar(50); NULL)
- action (nvarchar(255); NOT NULL)
- resourceType (nvarchar(255); NULL)
- resourceId (nvarchar(255); NULL)
- severity (nvarchar(50); NULL)
- status (nvarchar(50); NULL)
- ip (nvarchar(255); NULL)
- userAgent (nvarchar(MAX); NULL)
- details (nvarchar(MAX); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: certificate_templates
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- name (nvarchar(255); NOT NULL)
- description (nvarchar(MAX); NULL)
- template (nvarchar(MAX); NOT NULL)
- styles (nvarchar(MAX); NULL)
- placeholders (nvarchar(MAX); NULL)
- isDefault (bit; NULL)
- isActive (bit; NULL)
- createdBy (nvarchar(255); NOT NULL)
- updatedBy (nvarchar(255); NOT NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: certificates
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- student (nvarchar(255); NOT NULL)
- course (nvarchar(255); NOT NULL)
- issuedBy (nvarchar(255); NOT NULL)
- grade (nvarchar(10); NULL)
- issueDate (datetime; NULL)
- expiryDate (datetime; NULL)
- fileUrl (nvarchar(MAX); NULL)
- status (nvarchar(20); NULL)
- type (nvarchar(50); NULL)
- level (nvarchar(50); NULL)
- metadata (nvarchar(MAX); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: contractors
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- name (nvarchar(255); NOT NULL)
- location (nvarchar(255); NULL)
- phoneNumber (nvarchar(50); NULL)
- email (nvarchar(255); NULL)
- startDate (date; NULL)
- status (nvarchar(50); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: course_level_configs
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- name (nvarchar(255); NOT NULL)
- description (nvarchar(MAX); NULL)
- levels (nvarchar(MAX); NOT NULL)
- isActive (bit; NULL)
- isDefault (bit; NULL)
- createdBy (nvarchar(255); NULL)
- lastModifiedBy (nvarchar(255); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: courses
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- title (nvarchar(255); NOT NULL)
- description (nvarchar(MAX); NULL)
- thumbnail (nvarchar(MAX); NULL)
- category (nvarchar(255); NOT NULL)
- tags (nvarchar(MAX); NULL)
- instructor (int; NOT NULL)
- students (nvarchar(MAX); NULL)
- price (decimal(10,2); NULL)
- difficulty (nvarchar(50); NULL)
- status (nvarchar(50); NULL)
- modules (nvarchar(MAX); NULL)
- reviews (nvarchar(MAX); NULL)
- totalEnrollments (int; NULL)
- averageRating (decimal(3,2); NULL)
- slug (nvarchar(255); NULL)
- createdBy (int; NULL)
- quizzes (nvarchar(MAX); NULL)
- assignments (nvarchar(MAX); NULL)
- resources (nvarchar(MAX); NULL)
- isDeleted (bit; NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- departmentId (nvarchar(MAX); NULL)
- sectionId (nvarchar(MAX); NULL)

========================================================================
TABLE: custom_roles
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- name (nvarchar(100); NOT NULL)
- description (nvarchar(500); NULL)
- color (nvarchar(20); NULL)
- allowedPages (nvarchar(MAX); NULL)
- isSystem (bit; NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- permissions (nvarchar(MAX); NULL)
- targetLayout (nvarchar(50); NULL)
- generateManagementPage (bit; NULL)

========================================================================
TABLE: daily_5m_assignments
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- departmentId (nvarchar(255); NOT NULL)
- role (nvarchar(50); NOT NULL)
- userId (int; NOT NULL)
- userName (nvarchar(255); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: daily_5m_config_history
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- departmentId (nvarchar(255); NOT NULL)
- config (nvarchar(MAX); NULL)
- remark (nvarchar(MAX); NULL)
- updatedBy (nvarchar(255); NULL)
- createdAt (datetime; NULL)

========================================================================
TABLE: daily_5m_configs
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- departmentId (nvarchar(255); NOT NULL)
- config (nvarchar(MAX); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: daily_5m_records
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- departmentId (nvarchar(255); NOT NULL)
- date (date; NOT NULL)
- shift (nvarchar(50); NULL)
- line (nvarchar(50); NULL)
- recordData (nvarchar(MAX); NULL)
- submittedBy (nvarchar(255); NULL)
- createdAt (datetime2; NULL)
- updatedAt (datetime2; NULL)
- formType (nvarchar(50); NULL)
- sessionId (int; NULL)
- status (nvarchar(20); NULL)
- approvedBy (int; NULL)
- sectionId (nvarchar(255); NULL)
- adminRemarks (nvarchar(MAX); NULL)

========================================================================
TABLE: daily_production_report_config_history
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- departmentId (nvarchar(255); NOT NULL)
- config (nvarchar(MAX); NULL)
- remark (nvarchar(MAX); NULL)
- updatedBy (nvarchar(255); NULL)
- createdAt (datetime; NULL)

========================================================================
TABLE: daily_production_report_configs
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- departmentId (nvarchar(255); NOT NULL)
- config (nvarchar(MAX); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: daily_production_reports
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- date (date; NOT NULL)
- department_id (int; NOT NULL)
- line_id (int; NOT NULL)
- shift (varchar(50); NOT NULL)
- leaderName (varchar(255); NULL)
- delivery (nvarchar(MAX); NULL)
- quality (nvarchar(MAX); NULL)
- downTime (nvarchar(MAX); NULL)
- shiftCommunication (nvarchar(MAX); NULL)
- moral (nvarchar(MAX); NULL)
- directEfficiency (nvarchar(MAX); NULL)
- madeBy (varchar(255); NULL)
- checkedBy (varchar(255); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- customerEndDefectDetails (nvarchar(MAX); NULL)
- internalDefectDetails (nvarchar(MAX); NULL)
- manpowerAttendance (nvarchar(MAX); NULL)
- kaizenDetails (nvarchar(MAX); NULL)
- isSubmitted (bit; NULL)
- submittedBy (int; NULL)
- status (varchar(20); NULL)
- checkedByUserId (int; NULL)

========================================================================
TABLE: departments
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- name (varchar(255); NOT NULL)
- uniCode (varchar(255); NULL)
- slug (varchar(255); NULL)
- course (varchar(255); NULL)
- courses (nvarchar(MAX); NULL)
- instructor (nvarchar(MAX); NULL)
- students (nvarchar(MAX); NULL)
- startDate (datetime; NULL)
- endDate (datetime; NULL)
- capacity (int; NULL)
- status (varchar(50); NULL)
- schedule (nvarchar(MAX); NULL)
- notes (nvarchar(MAX); NULL)
- statusUpdatedAt (datetime; NULL)
- departmentQuiz (varchar(255); NULL)
- departmentAssignment (varchar(255); NULL)
- isDeleted (bit; NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- isReportingEnabled (bit; NULL)
- daily5mApproverDeptId (int; NULL)
- daily5mApproverSectionId (int; NULL)
- daily5mApproverLineId (int; NULL)
- dojoMandatoryQuizId (nvarchar(MAX); NULL)
- dojoHandoverQuizId (nvarchar(MAX); NULL)
- dojoInterviewQuizId (nvarchar(MAX); NULL)
- dojoEligibilityEvaluationId (nvarchar(MAX); NULL)
- dojoInterviewEvaluationId (nvarchar(MAX); NULL)
- isDojoSpecificDept (bit; NULL)
- skillMatrixApproverQaDeptId (int; NULL)
- skillMatrixApproverQaSectionId (int; NULL)
- skillMatrixApproverQaLineId (int; NULL)
- skillMatrixApproverSafetyDeptId (int; NULL)
- skillMatrixApproverSafetySectionId (int; NULL)
- skillMatrixApproverSafetyLineId (int; NULL)
- skillMatrixApproverProcessDeptId (int; NULL)
- skillMatrixApproverProcessSectionId (int; NULL)
- skillMatrixApproverProcessLineId (int; NULL)

========================================================================
TABLE: designation_shutters
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- designation (nvarchar(255); NOT NULL)
- createdAt (datetime; NULL)

========================================================================
TABLE: dpr_manual_statistics
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- date (date; NOT NULL)
- srcEffPlan (int; NULL)
- srcEffActual (int; NULL)
- srcEffTarget (float(53,0); NULL)
- srcDefAuto (int; NULL)
- srcDefManual (int; NULL)
- srcDefJoint (int; NULL)
- srcDefProduction (int; NULL)
- srcDefTarget (float(53,0); NULL)
- qaDefAuto (int; NULL)
- qaDefManual (int; NULL)
- qaDefJoint (int; NULL)
- qaDefProduction (int; NULL)
- qaDefTarget (float(53,0); NULL)
- qaEffPlan (int; NULL)
- qaEffActual (int; NULL)
- qaEffTarget (float(53,0); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: email_configurations
PRIMARY KEY: id
FOREIGN KEYS:
- departmentId -> departments(id)
COLUMNS:
- id (int; PK, NOT NULL)
- formName (varchar(150); NOT NULL)
- departmentId (int; FK->departments(id), NULL)
- toEmails (nvarchar(MAX); NULL)
- ccEmails (nvarchar(MAX); NULL)
- includeTrainer (bit; NULL)
- isActive (bit; NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- sectionId (int; NULL)
- scheduledTime (varchar(5); NULL)

========================================================================
TABLE: email_report_recipients
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- email (varchar(255); NOT NULL)
- isDailyReport (bit; NULL)
- isMonthlyReport (bit; NULL)
- reportTypes (varchar(255); NULL)
- createdAt (datetime; NULL)
- isManagementDailyReport (bit; NULL)

========================================================================
TABLE: enrollments
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- student (int; NOT NULL)
- course (int; NOT NULL)
- enrolledBy (int; NOT NULL)
- paymentStatus (nvarchar(50); NULL)
- paymentMethod (nvarchar(50); NULL)
- enrolledAt (datetime; NULL)
- expiresAt (datetime; NULL)
- isActive (bit; NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: evaluation_test_attempts
PRIMARY KEY: id
FOREIGN KEYS:
- testId -> evaluation_tests(id)
COLUMNS:
- id (int; PK, NOT NULL)
- testId (int; FK->evaluation_tests(id), NOT NULL)
- traineeName (nvarchar(255); NULL)
- employeeNo (nvarchar(255); NULL)
- educatorName (nvarchar(255); NULL)
- attemptData (nvarchar(MAX); NULL)
- createdBy (nvarchar(255); NULL)
- createdAt (datetime; NULL)
- userId (int; NULL)
- isHandoverEligible (bit; NULL)
- passedDate (date; NULL)
- studentIsTemporary (bit; NULL)
- studentDeptId (int; NULL)
- studentSectionId (int; NULL)
- studentLineId (int; NULL)
- studentSubSectionId (int; NULL)

========================================================================
TABLE: evaluation_tests
PRIMARY KEY: id
FOREIGN KEYS:
- departmentId -> departments(id)
COLUMNS:
- id (int; PK, NOT NULL)
- title (nvarchar(255); NOT NULL)
- performDateCount (int; NULL)
- contentStructure (nvarchar(MAX); NULL)
- createdBy (nvarchar(255); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- processType (nvarchar(255); NULL)
- departmentId (int; FK->departments(id), NULL)

========================================================================
TABLE: extra_attempt_allowances
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- quiz (nvarchar(255); NOT NULL)
- student (nvarchar(255); NOT NULL)
- extraAttemptsGranted (int; NULL)
- grantedBy (nvarchar(255); NULL)
- approvedAt (datetime; NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: global_cc_emails
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- email (nvarchar(255); NOT NULL)
- is_active (bit; NOT NULL)
- created_at (datetime; NOT NULL)
- updated_at (datetime; NULL)

========================================================================
TABLE: handover_sheet_config_history
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- departmentId (nvarchar(255); NOT NULL)
- config (nvarchar(MAX); NULL)
- remark (nvarchar(MAX); NULL)
- updatedBy (nvarchar(255); NULL)
- createdAt (datetime; NULL)
- sectionId (int; NULL)

========================================================================
TABLE: handover_sheet_configs
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- departmentId (nvarchar(255); NOT NULL)
- config (nvarchar(MAX); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- sectionId (int; NULL)

========================================================================
TABLE: handover_sheets
PRIMARY KEY: id
FOREIGN KEYS:
- departmentId -> departments(id)
COLUMNS:
- id (int; PK, NOT NULL)
- departmentId (int; FK->departments(id), NOT NULL)
- date (date; NULL)
- entries (nvarchar(MAX); NULL)
- signatures (nvarchar(MAX); NULL)
- metadata (nvarchar(MAX); NULL)
- createdBy (nvarchar(255); NULL)
- updatedBy (nvarchar(255); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- sectionId (int; NULL)
- isSubmitted (bit; NULL)
- submittedAt (datetime; NULL)
- remarksHistory (nvarchar(MAX); NULL)
- shift (nvarchar(10); NULL)

========================================================================
TABLE: headcount_reports
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- departmentId (int; NOT NULL)
- month (int; NOT NULL)
- year (int; NOT NULL)
- tableData (nvarchar(MAX); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: import_log_details
PRIMARY KEY: id
FOREIGN KEYS:
- logId -> import_logs(id)
COLUMNS:
- id (int; PK, NOT NULL)
- logId (int; FK->import_logs(id), NOT NULL)
- rowNumber (int; NULL)
- rowData (nvarchar(MAX); NULL)
- status (nvarchar(20); NULL)
- errorMessage (nvarchar(MAX); NULL)
- entityId (int; NULL)
- changes (nvarchar(MAX); NULL)

========================================================================
TABLE: import_logs
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- fileName (nvarchar(255); NOT NULL)
- importType (nvarchar(50); NOT NULL)
- totalRows (int; NULL)
- successCount (int; NULL)
- failCount (int; NULL)
- importedBy (int; NULL)
- createdAt (datetime; NULL)
- updatedCount (int; NULL)

========================================================================
TABLE: learning_comparisons
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- title (nvarchar(255); NOT NULL)
- description (nvarchar(MAX); NULL)
- beforeVideo (nvarchar(MAX); NULL)
- beforePdf (nvarchar(MAX); NULL)
- beforeExcel (nvarchar(MAX); NULL)
- beforeWord (nvarchar(MAX); NULL)
- beforePpt (nvarchar(MAX); NULL)
- afterVideo (nvarchar(MAX); NULL)
- afterPdf (nvarchar(MAX); NULL)
- afterExcel (nvarchar(MAX); NULL)
- afterWord (nvarchar(MAX); NULL)
- afterPpt (nvarchar(MAX); NULL)
- createdBy (int; NOT NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- beforeDescription (nvarchar(MAX); NULL)
- afterDescription (nvarchar(MAX); NULL)
- beforeImage (nvarchar(MAX); NULL)
- afterImage (nvarchar(MAX); NULL)
- beforeVideoDescriptions (nvarchar(MAX); NULL)
- beforePdfDescriptions (nvarchar(MAX); NULL)
- beforeExcelDescriptions (nvarchar(MAX); NULL)
- beforeWordDescriptions (nvarchar(MAX); NULL)
- beforePptDescriptions (nvarchar(MAX); NULL)
- beforeImageDescriptions (nvarchar(MAX); NULL)
- afterVideoDescriptions (nvarchar(MAX); NULL)
- afterPdfDescriptions (nvarchar(MAX); NULL)
- afterExcelDescriptions (nvarchar(MAX); NULL)
- afterWordDescriptions (nvarchar(MAX); NULL)
- afterPptDescriptions (nvarchar(MAX); NULL)
- afterImageDescriptions (nvarchar(MAX); NULL)

========================================================================
TABLE: lessons
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- module (int; NOT NULL)
- title (nvarchar(255); NOT NULL)
- content (nvarchar(MAX); NULL)
- slides (nvarchar(MAX); NULL)
- duration (int; NULL)
- order (int; NULL)
- slug (nvarchar(255); NULL)
- resources (nvarchar(MAX); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: line_requirement_history
PRIMARY KEY: id
FOREIGN KEYS:
- lineId -> lines(id)
- changedBy -> users(id)
COLUMNS:
- id (int; PK, NOT NULL)
- lineId (int; FK->lines(id), NOT NULL)
- oldQuantity (int; NULL)
- newQuantity (int; NOT NULL)
- type (nvarchar(10); NOT NULL)
- requirementDate (date; NULL)
- requirementMonth (int; NULL)
- requirementYear (int; NULL)
- changedBy (int; FK->users(id), NULL)
- createdAt (datetime; NULL)
- oldFn01 (int; NULL)
- newFn01 (int; NULL)
- oldFn02 (int; NULL)
- newFn02 (int; NULL)

========================================================================
TABLE: line_requirements
PRIMARY KEY: id
FOREIGN KEYS:
- lineId -> lines(id)
- sectionId -> sections(id)
COLUMNS:
- id (int; PK, NOT NULL)
- lineId (int; FK->lines(id), NOT NULL)
- requirementDate (date; NULL)
- requirementMonth (int; NULL)
- requirementYear (int; NOT NULL)
- quantity (int; NULL)
- type (nvarchar(10); NOT NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- fn01 (int; NULL)
- fn02 (int; NULL)
- sectionId (int; FK->sections(id), NULL)

========================================================================
TABLE: lines
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- name (nvarchar(255); NOT NULL)
- uniCode (nvarchar(255); NULL)
- department (int; NOT NULL)
- sectionId (int; NULL)
- description (nvarchar(MAX); NULL)
- isActive (bit; NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- lineLeader (nvarchar(MAX); NULL)
- mentor (nvarchar(255); NULL)
- requirement (int; NULL)
- tenCycleFormType (nvarchar(255); NULL)
- users (nvarchar(MAX); NULL)

========================================================================
TABLE: machine_assignments
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- machine_id (int; NOT NULL)
- user_id (int; NOT NULL)
- assigned_by (int; NULL)
- assigned_at (datetime; NULL)

========================================================================
TABLE: machines
PRIMARY KEY: id
FOREIGN KEYS:
- subSectionId -> sub_sections(id)
COLUMNS:
- id (int; PK, NOT NULL)
- name (nvarchar(255); NOT NULL)
- line (int; NOT NULL)
- subSectionId (int; FK->sub_sections(id), NULL)
- description (nvarchar(MAX); NULL)
- isActive (bit; NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- minimumRequiredLevel (nvarchar(50); NULL)
- criticality (nvarchar(50); NULL)

========================================================================
TABLE: mails
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- email (varchar(255); NOT NULL)
- isDailyReport (bit; NULL)
- isMonthlyReport (bit; NULL)
- reportTypes (varchar(255); NULL)
- createdAt (datetime; NULL)

========================================================================
TABLE: mentee_feedbacks
PRIMARY KEY: id
FOREIGN KEYS:
- studentId -> users(id)
COLUMNS:
- id (int; PK, NOT NULL)
- studentId (int; FK->users(id), NOT NULL)
- topTableData (nvarchar(MAX); NULL)
- dailyLogs (nvarchar(MAX); NULL)
- status (varchar(50); NULL)
- createdBy (varchar(255); NULL)
- updatedBy (varchar(255); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: module_timelines
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- course (int; NOT NULL)
- module (int; NOT NULL)
- department (int; NOT NULL)
- deadline (datetime; NOT NULL)
- gracePeriodHours (int; NULL)
- isActive (bit; NULL)
- enableWarnings (bit; NULL)
- warningPeriods (nvarchar(MAX); NULL)
- createdBy (int; NOT NULL)
- updatedBy (int; NULL)
- missedDeadlineStudents (nvarchar(MAX); NULL)
- warningsSent (nvarchar(MAX); NULL)
- description (nvarchar(MAX); NULL)
- lastProcessedAt (datetime; NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: modules
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- course (int; NOT NULL)
- title (nvarchar(255); NOT NULL)
- description (nvarchar(MAX); NULL)
- slug (nvarchar(255); NULL)
- order (int; NULL)
- lessons (nvarchar(MAX); NULL)
- resources (nvarchar(MAX); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: monitoring_config_history
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- configId (int; NOT NULL)
- type (varchar(20); NULL)
- departmentId (varchar(255); NULL)
- config (nvarchar(MAX); NULL)
- remark (nvarchar(MAX); NULL)
- updatedBy (varchar(255); NULL)
- updatedAt (datetime; NULL)
- sectionId (int; NULL)

========================================================================
TABLE: monitoring_configs
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- type (varchar(20); NOT NULL)
- departmentId (varchar(255); NULL)
- config (nvarchar(MAX); NOT NULL)
- remark (nvarchar(MAX); NULL)
- updatedBy (varchar(255); NULL)
- updatedAt (datetime; NULL)
- sectionId (int; NULL)

========================================================================
TABLE: multi_skilling_plan_config_history
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- departmentId (nvarchar(255); NOT NULL)
- config (nvarchar(MAX); NULL)
- remark (nvarchar(MAX); NULL)
- updatedBy (nvarchar(255); NULL)
- createdAt (datetime; NULL)

========================================================================
TABLE: multi_skilling_plan_configs
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- departmentId (nvarchar(255); NOT NULL)
- config (nvarchar(MAX); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: multi_skilling_plans
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- departmentId (int; NOT NULL)
- selectedLines (nvarchar(MAX); NULL)
- tableData (nvarchar(MAX); NULL)
- createdBy (nvarchar(255); NULL)
- updatedBy (nvarchar(255); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- sectionId (int; NULL)
- year (int; NULL)

========================================================================
TABLE: on_job_trainings
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- student (varchar(255); NULL)
- name (nvarchar(255); NULL)
- department (varchar(255); NOT NULL)
- line (nvarchar(255); NULL)
- machine (nvarchar(255); NULL)
- entries (nvarchar(MAX); NULL)
- scoring (nvarchar(MAX); NULL)
- totalMarks (decimal(10,2); NULL)
- totalMarksObtained (decimal(10,2); NULL)
- totalPercentage (decimal(5,2); NULL)
- result (varchar(50); NULL)
- guidelines (nvarchar(MAX); NULL)
- remarks (nvarchar(MAX); NULL)
- remarkImage (nvarchar(MAX); NULL)
- areaLine (nvarchar(255); NULL)
- trainingDate (date; NULL)
- trainingGivenBy (nvarchar(255); NULL)
- trainingTopic (nvarchar(255); NULL)
- trainingStartTime (varchar(50); NULL)
- trainingEndTime (varchar(50); NULL)
- trainingDetail (nvarchar(MAX); NULL)
- attendanceRecords (nvarchar(MAX); NULL)
- trainingDetailImage (nvarchar(MAX); NULL)
- trainingLog (nvarchar(MAX); NULL)
- createdBy (varchar(255); NULL)
- updatedBy (varchar(255); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- section (nvarchar(255); NULL)
- subSection (nvarchar(255); NULL)
- shareToken (nvarchar(64); NULL)

========================================================================
TABLE: operator_observances
PRIMARY KEY: id
FOREIGN KEYS:
- studentId -> users(id)
COLUMNS:
- id (int; PK, NOT NULL)
- studentId (int; FK->users(id), NOT NULL)
- lineName (varchar(255); NULL)
- processName (varchar(255); NULL)
- level1Date (datetime; NULL)
- operatorNameCode (varchar(255); NULL)
- observanceData (nvarchar(MAX); NULL)
- checkedBy (varchar(255); NULL)
- verifiedBy (varchar(255); NULL)
- revHistory (nvarchar(MAX); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- preparedBy (varchar(255); NULL)
- status (varchar(50); NULL)

========================================================================
TABLE: privileges
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- name (nvarchar(100); NOT NULL)

========================================================================
TABLE: progress
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- student (int; NOT NULL)
- course (int; NOT NULL)
- completedLessons (nvarchar(MAX); NULL)
- completedModules (nvarchar(MAX); NULL)
- quizzes (nvarchar(MAX); NULL)
- assignments (nvarchar(MAX); NULL)
- currentLevel (nvarchar(50); NULL)
- levelStartDate (datetime; NULL)
- pendingLevelUpgrade (nvarchar(50); NULL)
- levelLockEnabled (bit; NULL)
- lockedLevel (nvarchar(50); NULL)
- progressPercent (decimal(5,2); NULL)
- lastAccessed (datetime; NULL)
- currentAccessibleModule (int; NULL)
- timelineViolations (nvarchar(MAX); NULL)
- timelineNotifications (nvarchar(MAX); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: quizzes
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- title (nvarchar(255); NOT NULL)
- slug (nvarchar(255); NULL)
- description (nvarchar(MAX); NULL)
- questions (nvarchar(MAX); NULL)
- passingScore (int; NOT NULL)
- timeLimit (int; NULL)
- createdBy (nvarchar(255); NOT NULL)
- isPublished (bit; NULL)
- attemptsAllowed (int; NULL)
- skillUpgradation (nvarchar(MAX); NULL)
- issueCertificate (bit; NULL)
- courseId (nvarchar(255); NULL)
- course (nvarchar(255); NULL)
- moduleId (nvarchar(255); NULL)
- module (nvarchar(255); NULL)
- lesson (nvarchar(255); NULL)
- lessonId (nvarchar(255); NULL)
- type (nvarchar(50); NULL)
- scope (nvarchar(50); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- departmentId (nvarchar(MAX); NULL)
- sectionId (nvarchar(MAX); NULL)
- isDojo (bit; NULL)
- isHandover (bit; NULL)
- isTheoretical (bit; NULL)
- lineId (nvarchar(MAX); NULL)
- subSectionId (nvarchar(MAX); NULL)
- level (nvarchar(50); NULL)
- conductedBy (nvarchar(255); NULL)
- paperTitle (nvarchar(500); NULL)
- paperSubTitle (nvarchar(500); NULL)
- isMultiSkilling (bit; NULL)
- targetDeptId (nvarchar(MAX); NULL)
- targetSectionId (nvarchar(MAX); NULL)

========================================================================
TABLE: report_clubs
PRIMARY KEY: id
FOREIGN KEYS:
- departmentId -> departments(id)
- createdBy -> users(id)
COLUMNS:
- id (int; PK, NOT NULL)
- name (nvarchar(255); NOT NULL)
- departmentId (int; FK->departments(id), NOT NULL)
- sectionIds (nvarchar(MAX); NOT NULL)
- createdBy (int; FK->users(id), NOT NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- showInReport (bit; NULL)

========================================================================
TABLE: requirement_tokens
PRIMARY KEY: token
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- token (nvarchar(64); PK, NOT NULL)
- requirement_id (int; NULL)
- recipient_email (nvarchar(255); NOT NULL)
- sender_email (nvarchar(255); NULL)
- expires_at (datetime; NOT NULL)
- status (nvarchar(50); NULL)
- rejection_reason (nvarchar(MAX); NULL)
- created_at (datetime; NULL)
- upload_batch_id (nvarchar(50); NULL)
- section_code (nvarchar(100); NULL)
- section_name (nvarchar(255); NULL)

========================================================================
TABLE: requirementLogs
PRIMARY KEY: log_id
FOREIGN KEYS:
- requirement_id -> requirements_old(id)
COLUMNS:
- log_id (int; PK, NOT NULL)
- requirement_id (int; FK->requirements_old(id), NULL)
- section_id (int; NULL)
- old_values (nvarchar(MAX); NULL)
- new_values (nvarchar(MAX); NULL)
- employee_id (int; NULL)
- employee_role (varchar(50); NULL)
- created_at (datetime; NULL)

========================================================================
TABLE: requirements
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- srNo (int; NULL)
- sectionCode (varchar(50); NULL)
- sectionName (nvarchar(255); NULL)
- lineCode (varchar(50); NULL)
- lineDescription (nvarchar(MAX); NULL)
- monthName (varchar(15); NULL)
- monthNumber (int; NULL)
- salesPlan (float(53,0); NULL)
- prodPlan (float(53,0); NULL)
- year (int; NULL)
- createdAt (datetime; NULL)
- is_active (bit; NULL)
- approvalStatus (nvarchar(50); NULL)
- approvalOwnerName (nvarchar(255); NULL)
- approvalOwnerEmail (nvarchar(255); NULL)
- approvedBy (nvarchar(255); NULL)
- approvedByEmail (nvarchar(255); NULL)
- approvedAt (datetime; NULL)
- approvalSource (nvarchar(50); NULL)
- rejectedBy (nvarchar(255); NULL)
- rejectedAt (datetime; NULL)
- uploadBatchId (nvarchar(255); NULL)
- prodPlanFN01 (float(53,0); NULL)
- prodPlanFN02 (float(53,0); NULL)
- category (varchar(255); NULL)

========================================================================
TABLE: requirements_old
PRIMARY KEY: id
FOREIGN KEYS:
- sectionId -> departments(id)
- subSectionId -> lines(id)
COLUMNS:
- id (int; PK, NOT NULL)
- sectionId (int; FK->departments(id), NULL)
- sectionCode (varchar(50); NULL)
- sectionName (varchar(255); NULL)
- subSectionId (int; FK->lines(id), NULL)
- subSectionCode (varchar(50); NULL)
- subSectionName (varchar(255); NULL)
- lineId (int; NULL)
- lineArea (varchar(100); NULL)
- supervisorName (varchar(255); NULL)
- mentor (varchar(255); NULL)
- stationNo (varchar(50); NULL)
- month (varchar(20); NULL)
- year (int; NULL)
- salesPlan (float(53,0); NULL)
- prodPlan (float(53,0); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: RequirementUpdateLogs
PRIMARY KEY: log_id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- log_id (int; PK, NOT NULL)
- requirement_id (int; NOT NULL)
- section_id (int; NULL)
- subsection_id (int; NULL)
- action_type (nvarchar(50); NULL)
- old_salesPlan (float(53,0); NULL)
- new_salesPlan (float(53,0); NULL)
- old_prodPlan (float(53,0); NULL)
- new_prodPlan (float(53,0); NULL)
- old_prodPlanFN01 (float(53,0); NULL)
- new_prodPlanFN01 (float(53,0); NULL)
- old_prodPlanFN02 (float(53,0); NULL)
- new_prodPlanFN02 (float(53,0); NULL)
- old_values (nvarchar(MAX); NULL)
- new_values (nvarchar(MAX); NULL)
- employee_id (int; NULL)
- employee_role (nvarchar(200); NULL)
- updated_by_name (nvarchar(510); NULL)
- updated_at (datetime; NOT NULL)

========================================================================
TABLE: requriementLogs
PRIMARY KEY: log_id
FOREIGN KEYS:
- requirement_id -> requirements(id)
COLUMNS:
- log_id (int; PK, NOT NULL)
- requirement_id (int; FK->requirements(id), NOT NULL)
- section_id (int; NULL)
- old_values (nvarchar(MAX); NULL)
- new_values (nvarchar(MAX); NULL)
- employee_id (int; NULL)
- employee_role (nvarchar(50); NULL)
- created_at (datetime; NULL)

========================================================================
TABLE: resources
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- courseId (int; NULL)
- moduleId (int; NULL)
- lessonId (int; NULL)
- scope (nvarchar(50); NOT NULL)
- title (nvarchar(255); NOT NULL)
- type (nvarchar(50); NOT NULL)
- description (nvarchar(MAX); NULL)
- url (nvarchar(MAX); NOT NULL)
- publicId (nvarchar(255); NULL)
- fileSize (int; NULL)
- format (nvarchar(50); NULL)
- fileName (nvarchar(255); NULL)
- createdBy (int; NOT NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: section_heads
PRIMARY KEY: id
FOREIGN KEYS:
- sectionId -> sections(id)
- subSectionId -> lines(id)
- subSectionId -> lines(id)
COLUMNS:
- id (int; PK, NOT NULL)
- sectionId (int; FK->sections(id), NULL)
- subSectionId (int; FK->lines(id), NULL)
- subSectionId (int; FK->lines(id), NULL)
- email (nvarchar(255); NOT NULL)
- name (nvarchar(255); NULL)
- created_at (datetime; NULL)
- CCMail (nvarchar(2000); NULL)

========================================================================
TABLE: sections
PRIMARY KEY: id
FOREIGN KEYS:
- departmentId -> departments(id)
COLUMNS:
- id (int; PK, NOT NULL)
- name (nvarchar(255); NOT NULL)
- uniCode (nvarchar(255); NULL)
- description (nvarchar(MAX); NULL)
- category (nvarchar(50); NULL)
- departmentId (int; FK->departments(id), NOT NULL)
- isActive (bit; NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- daily5mFormType (nvarchar(255); NULL)
- tenCycleFormType (nvarchar(255); NULL)
- users (nvarchar(MAX); NULL)
- daily5mApproverDeptId (int; NULL)
- daily5mApproverSectionId (int; NULL)
- daily5mApproverLineId (int; NULL)
- skillMatrixApproverQaDeptId (int; NULL)
- skillMatrixApproverQaSectionId (int; NULL)
- skillMatrixApproverQaLineId (int; NULL)
- skillMatrixApproverSafetyDeptId (int; NULL)
- skillMatrixApproverSafetySectionId (int; NULL)
- skillMatrixApproverSafetyLineId (int; NULL)
- skillMatrixApproverProcessDeptId (int; NULL)
- skillMatrixApproverProcessSectionId (int; NULL)
- skillMatrixApproverProcessLineId (int; NULL)

========================================================================
TABLE: sixteen_day_monitorings
PRIMARY KEY: id
FOREIGN KEYS:
- studentId -> users(id)
COLUMNS:
- id (int; PK, NOT NULL)
- studentId (int; FK->users(id), NOT NULL)
- employeeName (varchar(255); NULL)
- employeeCode (varchar(255); NULL)
- processName (varchar(255); NULL)
- dept (varchar(255); NULL)
- handoverDate (varchar(255); NULL)
- trgResult (varchar(255); NULL)
- workingWith (varchar(255); NULL)
- lineLeaderName (varchar(255); NULL)
- gridData (nvarchar(MAX); NULL)
- createdBy (varchar(255); NULL)
- updatedBy (varchar(255); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- checkedBy (varchar(255); NULL)
- verifiedBy (varchar(255); NULL)
- approvedBy (varchar(255); NULL)
- status (varchar(50); NULL)
- attemptNumber (int; NULL)
- startDate (varchar(255); NULL)
- adminRemarksHistory (nvarchar(MAX); NULL)
- verifiedByEduCell (varchar(255); NULL)

========================================================================
TABLE: skill_matrices
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- department (varchar(255); NOT NULL)
- line (varchar(255); NULL)
- entries (nvarchar(MAX); NULL)
- headerInfo (nvarchar(MAX); NULL)
- footerInfo (nvarchar(MAX); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- month (varchar(7); NULL)
- section (varchar(255); NULL)
- subSection (varchar(255); NULL)
- station (varchar(255); NULL)

========================================================================
TABLE: skill_matrix_certificate_config_history
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- configId (int; NOT NULL)
- departmentId (varchar(255); NULL)
- config (nvarchar(MAX); NOT NULL)
- remark (nvarchar(MAX); NULL)
- updatedBy (int; NULL)
- createdAt (datetime; NULL)

========================================================================
TABLE: skill_matrix_certificate_configs
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- departmentId (varchar(255); NULL)
- config (nvarchar(MAX); NOT NULL)
- updatedBy (int; NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: skill_matrix_dashboard_config_history
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- departmentId (nvarchar(255); NOT NULL)
- config (nvarchar(MAX); NULL)
- remark (nvarchar(MAX); NULL)
- updatedBy (nvarchar(255); NULL)
- createdAt (datetime; NULL)

========================================================================
TABLE: skill_matrix_dashboard_configs
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- departmentId (nvarchar(255); NOT NULL)
- config (nvarchar(MAX); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: skill_matrix_evaluations
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- studentId (int; NOT NULL)
- departmentId (varchar(255); NULL)
- headerData (nvarchar(MAX); NULL)
- docData (nvarchar(MAX); NULL)
- evalData (nvarchar(MAX); NULL)
- opinion (nvarchar(MAX); NULL)
- updatedBy (int; NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- sheetIndex (int; NULL)
- period (varchar(50); NULL)
- isActive (bit; NULL)
- earnedLevel (varchar(50); NULL)
- efficiency (float(53,0); NULL)

========================================================================
TABLE: skill_upgradation_plan_config_history
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- departmentId (nvarchar(255); NOT NULL)
- config (nvarchar(MAX); NULL)
- remark (nvarchar(MAX); NULL)
- updatedBy (nvarchar(255); NULL)
- createdAt (datetime; NULL)

========================================================================
TABLE: skill_upgradation_plan_configs
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- departmentId (nvarchar(255); NOT NULL)
- config (nvarchar(MAX); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: skill_upgradation_plans
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- departmentId (int; NOT NULL)
- sectionId (int; NULL)
- selectedLines (nvarchar(MAX); NULL)
- tableData (nvarchar(MAX); NULL)
- createdBy (nvarchar(255); NULL)
- updatedBy (nvarchar(255); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- year (int; NULL)

========================================================================
TABLE: sub_sections
PRIMARY KEY: id
FOREIGN KEYS:
- lineId -> lines(id)
COLUMNS:
- id (int; PK, NOT NULL)
- name (nvarchar(255); NOT NULL)
- lineId (int; FK->lines(id), NOT NULL)
- description (nvarchar(MAX); NULL)
- isActive (bit; NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- users (nvarchar(MAX); NULL)
- minimumRequiredLevel (nvarchar(50); NULL)
- minEfficiency (decimal(5,2); NULL)
- maxEfficiency (decimal(5,2); NULL)

========================================================================
TABLE: submissions
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- assignment (int; NOT NULL)
- student (int; NOT NULL)
- fileUrl (nvarchar(MAX); NULL)
- attachments (nvarchar(MAX); NULL)
- grade (decimal(5,2); NULL)
- feedback (nvarchar(MAX); NULL)
- submittedAt (datetime; NULL)
- isLate (bit; NULL)
- resubmissionCount (int; NULL)
- status (nvarchar(50); NULL)
- gradedAt (datetime; NULL)
- gradedBy (int; NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: ten_cycle_checks
PRIMARY KEY: id
FOREIGN KEYS:
- studentId -> users(id)
COLUMNS:
- id (int; PK, NOT NULL)
- studentId (int; FK->users(id), NOT NULL)
- qualityEngineer (varchar(255); NULL)
- qualityEngineerSign (varchar(255); NULL)
- dojoEngineer (varchar(255); NULL)
- dojoEngineerSign (varchar(255); NULL)
- formType (varchar(50); NULL)
- entries (nvarchar(MAX); NULL)
- createdBy (varchar(255); NULL)
- updatedBy (varchar(255); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)

========================================================================
TABLE: ten_cycle_sheets
PRIMARY KEY: id
FOREIGN KEYS:
- departmentId -> departments(id)
COLUMNS:
- id (int; PK, NOT NULL)
- departmentId (int; FK->departments(id), NOT NULL)
- formType (nvarchar(50); NULL)
- createdDate (date; NULL)
- qualityEngineer (nvarchar(255); NULL)
- qualityEngineerSign (nvarchar(255); NULL)
- dojoEngineer (nvarchar(255); NULL)
- dojoEngineerSign (nvarchar(255); NULL)
- entries (nvarchar(MAX); NULL)
- createdBy (nvarchar(255); NULL)
- updatedBy (nvarchar(255); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- sectionId (int; NULL)
- lineId (int; NULL)
- subSectionId (int; NULL)
- status (nvarchar(50); NULL)
- checkedBy (nvarchar(255); NULL)
- verifiedBy (nvarchar(255); NULL)
- verifiedStatus (nvarchar(50); NULL)
- verifiedAt (datetime; NULL)
- reviewedBy (nvarchar(255); NULL)
- reviewedStatus (nvarchar(50); NULL)
- reviewedAt (datetime; NULL)

========================================================================
TABLE: three_day_monitorings
PRIMARY KEY: id
FOREIGN KEYS:
- studentId -> users(id)
COLUMNS:
- id (int; PK, NOT NULL)
- studentId (int; FK->users(id), NOT NULL)
- processName (varchar(255); NULL)
- lineName (varchar(255); NULL)
- entries (nvarchar(MAX); NULL)
- evaluation (nvarchar(MAX); NULL)
- checkedBy (varchar(255); NULL)
- verifiedBy (varchar(255); NULL)
- approvedBy (varchar(255); NULL)
- createdBy (varchar(255); NULL)
- updatedBy (varchar(255); NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- status (varchar(50); NULL)
- attemptNumber (int; NULL)

========================================================================
TABLE: user_hierarchy_snapshots
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- employeename (nvarchar(255); NULL)
- employeeid (nvarchar(255); NULL)
- shift (nvarchar(50); NULL)
- status (nvarchar(50); NULL)
- role (nvarchar(255); NULL)
- department (nvarchar(255); NULL)
- section (nvarchar(255); NULL)
- lines (nvarchar(255); NULL)
- sub-section (nvarchar(255); NULL)
- station (nvarchar(255); NULL)
- department_unicode (nvarchar(255); NULL)
- section_unicode (nvarchar(255); NULL)
- line_unicode (nvarchar(255); NULL)
- createdAt (datetime; NULL)
- schedule_shift (nvarchar(MAX); NULL)

========================================================================
TABLE: users
PRIMARY KEY: id
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; PK, NOT NULL)
- fullName (nvarchar(255); NOT NULL)
- userName (nvarchar(255); NOT NULL)
- slug (nvarchar(255); NULL)
- email (nvarchar(255); NULL)
- phoneNumber (nvarchar(50); NULL)
- password (nvarchar(255); NOT NULL)
- avatar (nvarchar(MAX); NULL)
- refreshToken (nvarchar(MAX); NULL)
- resetPasswordToken (nvarchar(255); NULL)
- resetPasswordExpiry (datetime; NULL)
- role (nvarchar(50); NULL)
- currentLevel (nvarchar(50); NULL)
- status (nvarchar(50); NULL)
- isVerified (bit; NULL)
- enrolledCourses (nvarchar(MAX); NULL)
- createdCourses (nvarchar(MAX); NULL)
- lastLogin (datetime; NULL)
- loginHistory (nvarchar(MAX); NULL)
- isDeleted (bit; NULL)
- department (nvarchar(255); NULL)
- sub_section (nvarchar(255); NULL)
- departments (nvarchar(MAX); NULL)
- unit (nvarchar(50); NOT NULL)
- empId (nvarchar(255); NULL)
- isEmployee (bit; NULL)
- isAdmin (bit; NULL)
- isTrainer (bit; NULL)
- shift (nvarchar(100); NULL)
- idCard (nvarchar(255); NULL)
- privileges (nvarchar(255); NULL)
- joiningDate (nvarchar(255); NULL)
- leavingDate (nvarchar(255); NULL)
- isTemporary (bit; NULL)
- sectionId (int; NULL)
- subSectionId (int; NULL)
- lineId (int; NULL)
- createdAt (datetime; NULL)
- updatedAt (datetime; NULL)
- customRoleId (int; NULL)
- fatherHusbandName (nvarchar(255); NULL)
- gender (nvarchar(50); NULL)
- dob (nvarchar(50); NULL)
- education (nvarchar(MAX); NULL)
- district (nvarchar(255); NULL)
- state (nvarchar(255); NULL)
- pin (nvarchar(50); NULL)
- busRoute (nvarchar(255); NULL)
- reasonOfLeaving (nvarchar(MAX); NULL)
- mentor (nvarchar(255); NULL)
- designation (nvarchar(255); NULL)
- stationId (int; NULL)
- departmentId (int; NULL)
- supervisor (nvarchar(255); NULL)
- incharge (nvarchar(255); NULL)
- isMentor (bit; NULL)
- isSupervisor (bit; NULL)
- isIncharge (bit; NULL)
- section (nvarchar(255); NULL)
- line (nvarchar(255); NULL)
- stationNo (nvarchar(255); NULL)
- targetDeptId (int; NULL)
- targetSectionId (int; NULL)
- targetLineId (int; NULL)
- targetSubSectionId (int; NULL)
- targetStationId (int; NULL)
- currentSkill (nvarchar(MAX); NULL)
- currentEffeciency (float(53,0); NULL)
- skillEffeciency (nvarchar(MAX); NULL)
- contractor (nvarchar(255); NULL)
- ojt (nvarchar(MAX); NULL)
- stations (nvarchar(MAX); NULL)
- expectedHandover (date; NULL)
- contractorId (int; NULL)
- sections (nvarchar(MAX); NULL)
- lines (nvarchar(MAX); NULL)
- subSections (nvarchar(MAX); NULL)
- shiftSchedule (nvarchar(MAX); NULL)

========================================================================
TABLE: users_joiningDate_backup_20260715
PRIMARY KEY: None declared in dump
FOREIGN KEYS:
- None declared in dump
COLUMNS:
- id (int; NOT NULL)
- empId (nvarchar(255); NULL)
- fullName (nvarchar(255); NOT NULL)
- joiningDate (nvarchar(255); NULL)
- updatedAt (datetime; NULL)
- BackupCreatedAt (datetime; NOT NULL)
"""

TABLE_METADATA: dict[str, dict] = {
    'abnormal_condition_sheets': {
        "purpose": 'Shop floor abnormal condition, line stoppage, and safety exception logs. Join intent: departmentId joins departments.id.',
        "synonyms": 'abnormal condition, abnormality, line issue, stoppage, exception log, safety issue',
        "key_columns": 'id, departmentId, date, isSubmitted, updatedBy, updatedAt',
    },
    'AIChatMessage': {
        "purpose": 'Individual chat messages and executed SQL queries logged in chat sessions. Join intent: session_id joins AIChatSessions.id.',
        "synonyms": 'chat message, ai message, user message, sql executed',
        "key_columns": 'id, session_id, sender, message_text, sql_executed, created_at',
    },
    'AIChatSessions': {
        "purpose": 'Chat conversation sessions created by users interacting with the AI agent. Logical relationship note: user_id may be used as the application-level lookup to users.id where stored values follow that identifier.',
        "synonyms": 'chat session, ai chat session, conversation thread',
        "key_columns": 'id, user_id, title, created_at',
    },
    'assignments': {
        "purpose": 'Homework, projects, and practical training assignments given to students/trainees. Logical relationship note: instructor may be used as the application-level lookup to users.id where stored values follow that identifier; createdBy may be used as the application-level lookup to users.id where stored values follow that identifier.',
        "synonyms": 'assignment, assignments, task, homework, project, practical work',
        "key_columns": 'id, courseId, title, description, dueDate, maxScore, status',
    },
    'attempt_extension_requests': {
        "purpose": 'Student requests for extra quiz attempt allowances. Logical relationship note: student may be used as the application-level lookup to users.id where stored values follow that identifier; quiz is an application-level quiz reference and may match quizzes.id or quizzes.title depending on stored value.',
        "synonyms": 'attempt extension, extra attempt request, quiz retry request',
        "key_columns": 'id, quiz, student, reason, status, extraAttemptsGranted',
    },
    'attempted_quizzes': {
        "purpose": 'Student and employee quiz attempt records, scores, pass/fail status, and timings. Logical relationship note: student may be used as the application-level lookup to users.id where stored values follow that identifier; quiz is an application-level quiz reference and may match quizzes.id or quizzes.title depending on stored value.',
        "synonyms": 'attempted quiz, quiz score, exam result, test attempt, student score, fail, pass, who passed the exam, who failed the exam, exam score, assessment result, attempt history',
        "key_columns": 'id, quiz, student, score, status, startedAt, completedAt, attemptNumber, timeTaken, studentName, studentEmpId',
    },
    'attendance_logs': {
        "purpose": 'Daily employee attendance punches, in/out timings, hours worked, and overtime records. Join intent: userId joins users.id. Logical relationship note: department may be used as the application-level lookup to departments.id where stored values follow that identifier.',
        "synonyms": 'attendance, punch, punches, in time, out time, late arrival, early departure, present, absent, leave, overtime, ot, attendance record, punch record, absenteeism, hours worked, overtime hours, late coming',
        "key_columns": 'id, userId, employeeName, date, department, shift, inTime, outTime, hrsWorked, status, lateArrival, otHrs',
    },
    'attendance_unmapped_logs': {
        "purpose": 'Raw unmapped attendance biometric logs where employee ID was unlinked. Logical relationship note: department may be used as the application-level lookup to departments.id where stored values follow that identifier.',
        "synonyms": 'unmapped attendance, raw punch, invalid card, missing user punch',
        "key_columns": 'id, payCode, cardNo, employeeName, date, department, shift, inTime, outTime, status, reason',
    },
    'audits': {
        "purpose": 'System security, user action, and modification audit trail logs.',
        "synonyms": 'audit, audits, audit log, security log, user action, activity trail, audit trail, system activity, security audit, change traceability',
        "key_columns": 'id, user, action, resourceType, resourceId, severity, status, ip, createdAt',
    },
    'certificate_templates': {
        "purpose": 'Master design templates for generating LMS completion certificates. Logical relationship note: createdBy may be used as the application-level lookup to users.id where stored values follow that identifier.',
        "synonyms": 'certificate template, cert template, template design',
        "key_columns": 'id, name, template, isDefault, isActive',
    },
    'certificates': {
        "purpose": 'Certificates issued to students upon course or training completion. Logical relationship note: student may be used as the application-level lookup to users.id where stored values follow that identifier; course may be used as the application-level lookup to courses.id where stored values follow that identifier.',
        "synonyms": 'certificate, certificates, course certificate, issue certificate, pass certificate',
        "key_columns": 'id, student, course, issuedBy, grade, issueDate, expiryDate, status, type, level',
    },
    'contractors': {
        "purpose": 'Master table for third-party manpower vendors and contractor companies.',
        "synonyms": 'contractor, contractors, vendor, vendors, agency, manpower contractor, staffing vendor, contract workforce supplier',
        "key_columns": 'id, name, location, phoneNumber, email, startDate, status',
    },
    'course_level_configs': {
        "purpose": 'Configuration settings for course difficulty and skill levels. Logical relationship note: createdBy may be used as the application-level lookup to users.id where stored values follow that identifier.',
        "synonyms": 'course level config, level configuration',
        "key_columns": 'id, name, levels, isActive',
    },
    'courses': {
        "purpose": 'LMS training courses, curriculum, modules, and instructional programs. Logical relationship note: instructor may be used as the application-level lookup to users.id where stored values follow that identifier; createdBy may be used as the application-level lookup to users.id where stored values follow that identifier; sectionId may be used as the application-level lookup to sections.id where stored values follow that identifier.',
        "synonyms": 'course, courses, training, syllabus, learning module, training course, learning program, course catalog, training curriculum',
        "key_columns": 'id, title, description, category, instructor, difficulty, status, totalEnrollments, departmentId',
    },
    'custom_roles': {
        "purpose": 'Role-based access control (RBAC) definitions and page permissions.',
        "synonyms": 'custom role, role permission, access level, user role',
        "key_columns": 'id, name, description, allowedPages, isSystem',
    },
    'daily_5m_assignments': {
        "purpose": 'Shop-floor daily 5M checklist assignment delegation to operators/leaders. Logical relationship note: userId may be used as the application-level lookup to users.id where stored values follow that identifier.',
        "synonyms": '5m assignment, daily 5m assignment, 5m assign, 5m duty, 5m allocation',
        "key_columns": 'id, departmentId, role, userId, userName, createdAt',
    },
    'daily_5m_config_history': {
        "purpose": 'Audit history of daily 5M configuration modifications.',
        "synonyms": '5m config history, 5m template history',
        "key_columns": 'id, departmentId, config, remark, updatedBy',
    },
    'daily_5m_configs': {
        "purpose": 'Dynamic form configuration JSON templates for daily 5M inspection.',
        "synonyms": '5m config, daily 5m form config',
        "key_columns": 'id, departmentId, config',
    },
    'daily_5m_records': {
        "purpose": 'Completed 5M daily check sheet submissions (Man, Machine, Material, Method, Measurement). Logical relationship note: sectionId may be used as the application-level lookup to sections.id where stored values follow that identifier.',
        "synonyms": '5m, daily 5m, 5m record, 5m submission, five m, shop floor checklist, 5m inspection',
        "key_columns": 'id, departmentId, date, shift, line, submittedBy, status, approvedBy',
    },
    'daily_production_report_config_history': {
        "purpose": 'Revision history of Daily Production Report configurations.',
        "synonyms": 'dpr config history',
        "key_columns": 'id, departmentId, config, remark',
    },
    'daily_production_report_configs': {
        "purpose": 'Form field configurations for Daily Production Reports.',
        "synonyms": 'dpr config, daily production report config',
        "key_columns": 'id, departmentId, config',
    },
    'daily_production_reports': {
        "purpose": 'Daily shop floor production, scrap, defect, downtime, and efficiency reports (DPR).',
        "synonyms": 'daily production report, dpr, production, scrap, downtime, direct efficiency, defects, delivery, quality, planned vs actual production, production efficiency, internal defect, customer defect, kaizen, manpower attendance',
        "key_columns": 'id, date, department_id, line_id, shift, leaderName, delivery, quality, downTime, directEfficiency, status, madeBy',
    },
    'departments': {
        "purpose": 'Master table defining organizational departments and division units. Logical relationship note: course may be used as the application-level lookup to courses.id where stored values follow that identifier; instructor may be used as the application-level lookup to users.id where stored values follow that identifier.',
        "synonyms": 'department, departments, dept, depts, department master, organizational unit, plant department',
        "key_columns": 'id, name, uniCode, slug, status, isDeleted',
    },
    'designation_shutters': {
        "purpose": 'Designation categorization and shutter mappings.',
        "synonyms": 'designation shutter, designation mapping',
        "key_columns": 'id, designation, createdAt',
    },
    'dpr_manual_statistics': {
        "purpose": 'Manual daily production report metrics, target vs actual efficiency and defects.',
        "synonyms": 'dpr stats, target efficiency, actual efficiency, defects target, qa defects',
        "key_columns": 'id, date, srcEffPlan, srcEffActual, srcEffTarget, srcDefAuto, qaDefAuto, qaEffPlan, qaEffActual',
    },
    'email_configurations': {
        "purpose": 'Scheduled automated email report configurations for departments and sections. Join intent: departmentId joins departments.id. Logical relationship note: sectionId may be used as the application-level lookup to sections.id where stored values follow that identifier.',
        "synonyms": 'email config, email configuration, report mail config, scheduled mail',
        "key_columns": 'id, formName, departmentId, toEmails, ccEmails, includeTrainer, isActive, scheduledTime',
    },
    'email_report_recipients': {
        "purpose": 'Recipient email list for daily and monthly management reports.',
        "synonyms": 'report recipients, email list, management daily report',
        "key_columns": 'id, email, isDailyReport, isMonthlyReport, reportTypes',
    },
    'enrollments': {
        "purpose": 'Course enrollment records linking students to registered courses. Logical relationship note: student may be used as the application-level lookup to users.id where stored values follow that identifier; course may be used as the application-level lookup to courses.id where stored values follow that identifier; enrolledBy may be used as the application-level lookup to users.id where stored values follow that identifier.',
        "synonyms": 'enrollment, enrollments, enrolled student, course registration, course enrollment, training registration, active enrollment',
        "key_columns": 'id, student, course, paymentStatus, enrolledAt, expiresAt, isActive',
    },
    'evaluation_test_attempts': {
        "purpose": 'Trainee results and scores on Dojo practical evaluation tests and handover eligibility. Join intent: testId joins evaluation_tests.id. Logical relationship note: createdBy may be used as the application-level lookup to users.id where stored values follow that identifier; userId may be used as the application-level lookup to users.id where stored values follow that identifier.',
        "synonyms": 'evaluation attempt, dojo result, handover eligible, dojo score, trainee evaluation, practical test result, practical assessment result, handover eligibility, trainee evaluation result',
        "key_columns": 'id, testId, traineeName, employeeNo, educatorName, isHandoverEligible, passedDate, userId',
    },
    'evaluation_tests': {
        "purpose": 'Shop-floor Dojo practical evaluation tests and skill verification assessments. Join intent: departmentId joins departments.id. Logical relationship note: createdBy may be used as the application-level lookup to users.id where stored values follow that identifier.',
        "synonyms": 'evaluation test, dojo test, practical evaluation, dojo exam, practical test',
        "key_columns": 'id, title, performDateCount, processType, departmentId',
    },
    'extra_attempt_allowances': {
        "purpose": 'Granted extra attempts for specific quizzes and students. Logical relationship note: student may be used as the application-level lookup to users.id where stored values follow that identifier; quiz is an application-level quiz reference and may match quizzes.id or quizzes.title depending on stored value.',
        "synonyms": 'extra attempt allowance, granted attempts, retry allowance',
        "key_columns": 'id, quiz, student, extraAttemptsGranted, grantedBy',
    },
    'global_cc_emails': {
        "purpose": 'System-wide global CC recipients for automated notifications.',
        "synonyms": 'global cc, notification cc, cc email',
        "key_columns": 'id, email, is_active',
    },
    'handover_sheet_config_history': {
        "purpose": 'Revision history of Shift Handover sheet configurations. Logical relationship note: sectionId may be used as the application-level lookup to sections.id where stored values follow that identifier.',
        "synonyms": 'handover config history',
        "key_columns": 'id, departmentId, config, remark',
    },
    'handover_sheet_configs': {
        "purpose": 'Form field configurations for Shift Handover sheets. Logical relationship note: sectionId may be used as the application-level lookup to sections.id where stored values follow that identifier.',
        "synonyms": 'handover config, shift handover config',
        "key_columns": 'id, departmentId, config, sectionId',
    },
    'handover_sheets': {
        "purpose": 'Shift handover logs between outgoing and incoming shift leaders/operators. Join intent: departmentId joins departments.id. Logical relationship note: createdBy may be used as the application-level lookup to users.id where stored values follow that identifier; sectionId may be used as the application-level lookup to sections.id where stored values follow that identifier.',
        "synonyms": 'handover sheet, shift handover, shift change, charge handover, transfer shift',
        "key_columns": 'id, departmentId, date, shift, sectionId, isSubmitted, submittedAt',
    },
    'headcount_reports': {
        "purpose": 'Monthly departmental manpower headcount summary reports.',
        "synonyms": 'headcount report, monthly headcount, manpower summary, planned vs actual headcount, monthly workforce headcount, department headcount',
        "key_columns": 'id, departmentId, month, year, createdAt',
    },
    'import_log_details': {
        "purpose": 'Row-level validation and error records for batch imports. Join intent: logId joins import_logs.id.',
        "synonyms": 'import log details, upload error, failed row',
        "key_columns": 'id, logId, rowNumber, status, errorMessage',
    },
    'import_logs': {
        "purpose": 'Batch Excel/CSV data import session summaries.',
        "synonyms": 'import log, bulk upload, excel import, data upload',
        "key_columns": 'id, fileName, importType, totalRows, successCount, failCount, importedBy',
    },
    'learning_comparisons': {
        "purpose": 'Before vs After training skill comparison media and documents. Logical relationship note: createdBy may be used as the application-level lookup to users.id where stored values follow that identifier.',
        "synonyms": 'learning comparison, before after, kaizen training comparison',
        "key_columns": 'id, title, description, createdBy, createdAt',
    },
    'lessons': {
        "purpose": 'Individual training lessons, lecture slides, and video contents inside modules. Logical relationship note: module may be used as the application-level lookup to modules.id where stored values follow that identifier.',
        "synonyms": 'lesson, lessons, lecture, slide, class',
        "key_columns": 'id, module, title, content, duration, order',
    },
    'line_requirement_history': {
        "purpose": 'Historical audit log of line requirement modifications. Join intent: lineId joins lines.id; changedBy joins users.id.',
        "synonyms": 'line requirement history, requirement audit, old quantity, new quantity',
        "key_columns": 'id, lineId, oldQuantity, newQuantity, type, requirementDate, changedBy',
    },
    'line_requirements': {
        "purpose": 'Specific quantity and head-count requirements per line and section. Join intent: lineId joins lines.id; sectionId joins sections.id.',
        "synonyms": 'line requirement, line manpower, requirement per line, planned manpower by line, line staffing requirement, FN01 requirement, FN02 requirement',
        "key_columns": 'id, lineId, requirementDate, requirementMonth, requirementYear, quantity, type, fn01, fn02, sectionId',
    },
    'lines': {
        "purpose": 'Master table for shop-floor production lines within departments/sections. Logical relationship note: department may be used as the application-level lookup to departments.id where stored values follow that identifier; sectionId may be used as the application-level lookup to sections.id where stored values follow that identifier.',
        "synonyms": 'line, lines, production line, assembly line',
        "key_columns": 'id, name, uniCode, department, sectionId, isActive, lineLeader, mentor',
    },
    'machine_assignments': {
        "purpose": 'Operator allocations and machine assignment history. Logical relationship note: machine_id may be used as the application-level lookup to machines.id where stored values follow that identifier; user_id may be used as the application-level lookup to users.id where stored values follow that identifier; assigned_by may be used as the application-level lookup to users.id where stored values follow that identifier.',
        "synonyms": 'machine assignment, assign machine, operator machine, machine allotment',
        "key_columns": 'id, machine_id, user_id, assigned_by, assigned_at',
    },
    'machines': {
        "purpose": 'Master table of shop-floor machines, equipment, and work stations. Join intent: subSectionId joins sub_sections.id.',
        "synonyms": 'machine, machines, equipment, station, stations, machine master, equipment master, workstation, machine criticality',
        "key_columns": 'id, name, line, subSectionId, isActive, minimumRequiredLevel, criticality',
    },
    'mails': {
        "purpose": 'Legacy email distribution records for automated reporting.',
        "synonyms": 'mails, mail dispatch',
        "key_columns": 'id, email, isDailyReport, isMonthlyReport',
    },
    'mentee_feedbacks': {
        "purpose": 'Feedback and daily logs submitted by mentors regarding assigned trainees/mentees. Join intent: studentId joins users.id. Logical relationship note: createdBy may be used as the application-level lookup to users.id where stored values follow that identifier.',
        "synonyms": 'mentee feedback, mentor feedback, trainee progress log',
        "key_columns": 'id, studentId, status, createdBy, createdAt',
    },
    'module_timelines': {
        "purpose": 'Deadlines, grace periods, and warning thresholds for training modules. Logical relationship note: course may be used as the application-level lookup to courses.id where stored values follow that identifier; module may be used as the application-level lookup to modules.id where stored values follow that identifier; createdBy may be used as the application-level lookup to users.id where stored values follow that identifier; department may be used as the application-level lookup to departments.id where stored values follow that identifier.',
        "synonyms": 'module timeline, module deadline, training deadline, warning period',
        "key_columns": 'id, course, module, department, deadline, gracePeriodHours, isActive',
    },
    'modules': {
        "purpose": 'Course chapter modules dividing LMS courses into topics. Logical relationship note: course may be used as the application-level lookup to courses.id where stored values follow that identifier.',
        "synonyms": 'module, modules, course module, chapter, unit',
        "key_columns": 'id, course, title, description, order',
    },
    'monitoring_config_history': {
        "purpose": 'Revision history of operator monitoring configurations. Logical relationship note: sectionId may be used as the application-level lookup to sections.id where stored values follow that identifier.',
        "synonyms": 'monitoring config history',
        "key_columns": 'id, configId, type, departmentId, config',
    },
    'monitoring_configs': {
        "purpose": 'Configurations for operator monitoring forms and checklists. Logical relationship note: sectionId may be used as the application-level lookup to sections.id where stored values follow that identifier.',
        "synonyms": 'monitoring config',
        "key_columns": 'id, type, departmentId, config',
    },
    'multi_skilling_plan_config_history': {
        "purpose": 'Revision history of multi-skilling plan configurations.',
        "synonyms": 'multiskilling config history',
        "key_columns": 'id, departmentId, config',
    },
    'multi_skilling_plan_configs': {
        "purpose": 'Templates for multi-skilling planning sheets.',
        "synonyms": 'multiskilling plan config',
        "key_columns": 'id, departmentId, config',
    },
    'multi_skilling_plans': {
        "purpose": 'Departmental multi-skilling roadmaps and line operator versatility plans. Logical relationship note: createdBy may be used as the application-level lookup to users.id where stored values follow that identifier; sectionId may be used as the application-level lookup to sections.id where stored values follow that identifier.',
        "synonyms": 'multiskilling plan, operator flexibility, versatile operator',
        "key_columns": 'id, departmentId, sectionId, selectedLines, year',
    },
    'on_job_trainings': {
        "purpose": 'On-The-Job Training (OJT) records, scores, trainer remarks, and line training results. Logical relationship note: student may be used as the application-level lookup to users.id where stored values follow that identifier; createdBy may be used as the application-level lookup to users.id where stored values follow that identifier; department may be used as the application-level lookup to departments.id where stored values follow that identifier.',
        "synonyms": 'ojt, on job training, shop floor training, training score, total percentage, result, OJT record, operator training, training effectiveness, practical training result',
        "key_columns": 'id, student, name, department, line, machine, totalMarks, totalMarksObtained, totalPercentage, result, trainingDate',
    },
    'operator_observances': {
        "purpose": 'Supervisor and quality engineer process observance audits for operators. Join intent: studentId joins users.id.',
        "synonyms": 'operator observance, observance audit, process audit, standard work audit',
        "key_columns": 'id, studentId, lineName, processName, level1Date, operatorNameCode, status',
    },
    'privileges': {
        "purpose": 'Granular system permission privileges.',
        "synonyms": 'privilege, privileges, system permission',
        "key_columns": 'id, name',
    },
    'progress': {
        "purpose": 'Student LMS learning progress, completed lessons, module levels, and progress percentages. Logical relationship note: student may be used as the application-level lookup to users.id where stored values follow that identifier; course may be used as the application-level lookup to courses.id where stored values follow that identifier.',
        "synonyms": 'progress, learning progress, course progress, progress percent, completed lessons, currentLevel, training completion, learning completion, current skill level, module progress',
        "key_columns": 'id, student, course, currentLevel, progressPercent, lastAccessed',
    },
    'quizzes': {
        "purpose": 'Master question papers, quizzes, online exams, and theoretical assessments. Logical relationship note: course may be used as the application-level lookup to courses.id where stored values follow that identifier; module may be used as the application-level lookup to modules.id where stored values follow that identifier; lesson may be used as the application-level lookup to lessons.id where stored values follow that identifier; createdBy may be used as the application-level lookup to users.id where stored values follow that identifier; sectionId may be used as the application-level lookup to sections.id where stored values follow that identifier; lineId may be used as the application-level lookup to lines.id where stored values follow that identifier; subSectionId may be used as the application-level lookup to sub_sections.id where stored values follow that identifier.',
        "synonyms": 'quiz, quizzes, exam, test, tests, assessment, question paper, paper, assessment paper, theoretical test, who failed the exam, passing score, quiz attempts',
        "key_columns": 'id, title, passingScore, timeLimit, attemptsAllowed, courseId, isPublished, isDojo, level',
    },
    'report_clubs': {
        "purpose": 'Grouping sections and departments for consolidated reporting. Join intent: departmentId joins departments.id; createdBy joins users.id.',
        "synonyms": 'report club, department group, consolidated report',
        "key_columns": 'id, name, departmentId, sectionIds, showInReport',
    },
    'requirement_tokens': {
        "purpose": 'Approval tokens and workflow links for requirement approval emails.',
        "synonyms": 'requirement token, approval token, email approval',
        "key_columns": 'token, requirement_id, recipient_email, expires_at, status',
    },
    'requirementLogs': {
        "purpose": 'Audit history for planning requirement modifications. Join intent: requirement_id joins requirements_old.id.',
        "synonyms": 'requirement log, requirement change history',
        "key_columns": 'log_id, requirement_id, section_id, old_values, new_values',
    },
    'requirements': {
        "purpose": 'Production and manpower planning targets, sales plans, and line requirements by month/year.',
        "synonyms": 'requirement, requirements, sales plan, prod plan, manpower requirement, fn01, fn02, planning target, production plan, section requirement, approval status, FN01 production plan, FN02 production plan',
        "key_columns": 'id, sectionCode, sectionName, lineCode, monthName, monthNumber, salesPlan, prodPlan, year, prodPlanFN01, prodPlanFN02',
    },
    'requirements_old': {
        "purpose": 'Legacy historical requirements table. Join intent: sectionId joins departments.id; subSectionId joins lines.id. Logical relationship note: lineId may be used as the application-level lookup to lines.id where stored values follow that identifier.',
        "synonyms": 'requirements old, legacy requirements',
        "key_columns": 'id, sectionId, lineId, salesPlan, prodPlan',
    },
    'RequirementUpdateLogs': {
        "purpose": 'Detailed logs of changes to sales and production planning numbers.',
        "synonyms": 'requirement update log, prod plan update log',
        "key_columns": 'log_id, requirement_id, old_prodPlan, new_prodPlan',
    },
    'requriementLogs': {
        "purpose": 'Historical typo alias table for requirement modification logs. Join intent: requirement_id joins requirements.id.',
        "synonyms": 'requriement log',
        "key_columns": 'log_id, requirement_id, section_id',
    },
    'resources': {
        "purpose": 'Downloadable course resources, PDFs, files, and links. Logical relationship note: createdBy may be used as the application-level lookup to users.id where stored values follow that identifier.',
        "synonyms": 'resource, resources, course material, pdf, document, download',
        "key_columns": 'id, courseId, moduleId, lessonId, title, type, url',
    },
    'section_heads': {
        "purpose": 'Section and subsection head contact details and CC emails. Join intent: sectionId joins sections.id; subSectionId joins lines.id.',
        "synonyms": 'section head, incharge, section leader',
        "key_columns": 'id, sectionId, subSectionId, email, name, CCMail',
    },
    'sections': {
        "purpose": 'Master table for departmental sections under departments. Join intent: departmentId joins departments.id.',
        "synonyms": 'section, sections, section master, department section, shop-floor section',
        "key_columns": 'id, name, uniCode, departmentId, isActive',
    },
    'sixteen_day_monitorings': {
        "purpose": 'Extended 16-day shop floor operator performance and handover monitoring sheet. Join intent: studentId joins users.id. Logical relationship note: createdBy may be used as the application-level lookup to users.id where stored values follow that identifier.',
        "synonyms": '16 day monitoring, 16-day, sixteen day monitoring, handover monitoring, trg result, 16-day operator observation, post-handover monitoring, operator performance monitoring',
        "key_columns": 'id, studentId, employeeName, employeeCode, processName, dept, handoverDate, trgResult, status',
    },
    'skill_matrices': {
        "purpose": 'Department and line skill matrix mapping operator competency levels. Logical relationship note: department may be used as the application-level lookup to departments.id where stored values follow that identifier.',
        "synonyms": 'skill matrix, skill, multiskilling, competency, operator skill level, level 1, level 2, level 3, level 4, operator competency matrix, skill level matrix, multi-skill matrix, workforce competency',
        "key_columns": 'id, department, line, section, subSection, station, month',
    },
    'skill_matrix_certificate_config_history': {
        "purpose": 'History of skill matrix certificate configurations.',
        "synonyms": 'skill matrix cert history',
        "key_columns": 'id, configId, departmentId, config',
    },
    'skill_matrix_certificate_configs': {
        "purpose": 'Certificate configuration rules for skill matrix levels.',
        "synonyms": 'skill matrix cert config',
        "key_columns": 'id, departmentId, config',
    },
    'skill_matrix_dashboard_config_history': {
        "purpose": 'History of skill matrix dashboard configurations.',
        "synonyms": 'skill matrix dashboard history',
        "key_columns": 'id, departmentId, config',
    },
    'skill_matrix_dashboard_configs': {
        "purpose": 'Dashboard visualization settings for skill matrices.',
        "synonyms": 'skill matrix dashboard config',
        "key_columns": 'id, departmentId, config',
    },
    'skill_matrix_evaluations': {
        "purpose": 'Individual operator skill matrix level evaluations and efficiency ratings.',
        "synonyms": 'skill evaluation, earned level, skill efficiency, operator evaluation, operator efficiency, earned competency level, skill assessment',
        "key_columns": 'id, studentId, departmentId, period, earnedLevel, efficiency, isActive',
    },
    'skill_upgradation_plan_config_history': {
        "purpose": 'History of skill upgradation configurations.',
        "synonyms": 'skill upgradation history',
        "key_columns": 'id, departmentId, config',
    },
    'skill_upgradation_plan_configs': {
        "purpose": 'Templates and rules for skill upgradation planning.',
        "synonyms": 'skill upgradation config',
        "key_columns": 'id, departmentId, config',
    },
    'skill_upgradation_plans': {
        "purpose": 'Annual and monthly skill upgradation and multi-skilling training plans. Logical relationship note: createdBy may be used as the application-level lookup to users.id where stored values follow that identifier; sectionId may be used as the application-level lookup to sections.id where stored values follow that identifier.',
        "synonyms": 'skill upgradation plan, multi skilling plan, training plan, skill upgrade',
        "key_columns": 'id, departmentId, sectionId, selectedLines, year',
    },
    'sub_sections': {
        "purpose": 'Master table for sub-sections or work cells under lines. Join intent: lineId joins lines.id.',
        "synonyms": 'sub section, sub sections, sub_sections, subsection master, work cell, production cell',
        "key_columns": 'id, name, lineId, isActive, minimumRequiredLevel',
    },
    'submissions': {
        "purpose": 'Student submissions for course assignments and grades received. Logical relationship note: student may be used as the application-level lookup to users.id where stored values follow that identifier; assignment may be used as the application-level lookup to assignments.id where stored values follow that identifier; gradedBy may be used as the application-level lookup to users.id where stored values follow that identifier.',
        "synonyms": 'submission, submissions, submitted assignment, grade, marks, feedback',
        "key_columns": 'id, assignment, student, grade, submittedAt, isLate, status',
    },
    'ten_cycle_checks': {
        "purpose": 'Student-specific 10-cycle process verification records. Join intent: studentId joins users.id. Logical relationship note: createdBy may be used as the application-level lookup to users.id where stored values follow that identifier.',
        "synonyms": 'ten cycle check, 10 cycle student check, operator 10-cycle check, process verification',
        "key_columns": 'id, studentId, qualityEngineer, dojoEngineer, formType',
    },
    'ten_cycle_sheets': {
        "purpose": 'Ten-cycle time and quality verification inspection sheets. Join intent: departmentId joins departments.id. Logical relationship note: createdBy may be used as the application-level lookup to users.id where stored values follow that identifier; sectionId may be used as the application-level lookup to sections.id where stored values follow that identifier; lineId may be used as the application-level lookup to lines.id where stored values follow that identifier; subSectionId may be used as the application-level lookup to sub_sections.id where stored values follow that identifier.',
        "synonyms": 'ten cycle sheet, 10 cycle, ten cycle check, cycle time inspection, quality check, 10-cycle verification, process cycle verification, quality verification',
        "key_columns": 'id, departmentId, formType, createdDate, qualityEngineer, dojoEngineer, sectionId, lineId, status',
    },
    'three_day_monitorings': {
        "purpose": 'Initial 3-day post-training shop floor operator monitoring sheet. Join intent: studentId joins users.id. Logical relationship note: createdBy may be used as the application-level lookup to users.id where stored values follow that identifier.',
        "synonyms": '3 day monitoring, 3-day, three day monitoring, new joinee monitoring, initial observation, post-training monitoring, 3-day operator observation, handover readiness',
        "key_columns": 'id, studentId, processName, lineName, status, attemptNumber, checkedBy, verifiedBy',
    },
    'user_hierarchy_snapshots': {
        "purpose": 'Periodic organizational snapshots of employee hierarchy and reporting lines. Logical relationship note: department may be used as the application-level lookup to departments.id where stored values follow that identifier.',
        "synonyms": 'user hierarchy snapshot, employee hierarchy, reporting structure, shift snapshot',
        "key_columns": 'id, employeename, employeeid, shift, role, department, section, lines',
    },
    'users': {
        "purpose": 'Primary master table for employees, operators, trainers, admins, and staff members. Logical relationship note: department may be used as the application-level lookup to departments.id where stored values follow that identifier; sectionId may be used as the application-level lookup to sections.id where stored values follow that identifier; lineId may be used as the application-level lookup to lines.id where stored values follow that identifier; subSectionId may be used as the application-level lookup to sub_sections.id where stored values follow that identifier.',
        "synonyms": 'user, users, employee, employees, emp, staff, worker, workers, operator, operators, person, name, designation, status, joiningDate, employee master, operator master, workforce roster, employee status, employee designation, temporary workforce',
        "key_columns": 'id, empId, fullName, userName, email, role, department, designation, status, line, section, isDeleted, isTemporary',
    },
    'users_joiningDate_backup_20260715': {
        "purpose": 'Static database backup table for employee joining dates.',
        "synonyms": 'users backup, joining date backup',
        "key_columns": 'id, empId, fullName, joiningDate, BackupCreatedAt',
    },
}

# Compact summary formatted for prompt injection during table routing

COMPACT_TABLE_CATALOG = "\n".join(
    f"- {tbl}: {meta['purpose']} (Topics: {meta['synonyms']}) [Columns: {meta['key_columns']}]"
    for tbl, meta in sorted(TABLE_METADATA.items())
)

# Exact physical table whitelist used by nodes.py to reject hallucinated table names
TABLE_NAMES = frozenset(TABLE_METADATA.keys())
