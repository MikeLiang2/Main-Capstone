# from app.models.checklists import ChecklistStep, ChecklistStage, ProcessCategory, ProcessInstance

# fake_stages = {
#     1: [  # Onboarding Process
#         ChecklistStage(
#             id=1,
#             name="Document Collection",
#             order=1,
#             steps=[
#                 ChecklistStep(id=101, name="Upload ID", description="Upload a valid government-issued ID.", completed=True, resourceUrl=""),
#                 ChecklistStep(id=102, name="Upload Resume", description="Upload the latest version of your resume.", completed=False, resourceUrl="")
#             ]
#         ),
#         ChecklistStage(
#             id=2,
#             name="Account Setup",
#             order=2,
#             steps=[
#                 ChecklistStep(id=103, name="Create Company Email", description="Set up your company email address.", completed=False, resourceUrl="https://email.example.com/setup"),
#                 ChecklistStep(id=104, name="Set Password", description="Set a strong password for internal systems.", completed=False, resourceUrl="")
#             ]
#         ),
#         ChecklistStage(
#             id=3,
#             name="Orientation",
#             order=3,
#             steps=[
#                 ChecklistStep(id=105, name="Watch Welcome Video", description="Watch the 15-minute company introduction.", completed=False, resourceUrl="https://video.example.com/welcome"),
#                 ChecklistStep(id=106, name="Fill Feedback Form", description="Provide your feedback about onboarding.", completed=False, resourceUrl="")
#             ]
#         )
#     ],
#     2: [  # Travel Authorization Process
#         ChecklistStage(
#             id=4,
#             name="Request Submission",
#             order=1,
#             steps=[
#                 ChecklistStep(id=201, name="Submit Travel Request", description="Fill out the travel request form.", completed=False, resourceUrl=""),
#                 ChecklistStep(id=202, name="Manager Approval", description="Get your manager’s approval for the trip.", completed=False, resourceUrl="")
#             ]
#         ),
#         ChecklistStage(
#             id=5,
#             name="Logistics",
#             order=2,
#             steps=[
#                 ChecklistStep(id=203, name="Book Flights", description="Reserve your flights through the system.", completed=False, resourceUrl="https://travel.example.com"),
#                 ChecklistStep(id=204, name="Book Hotel", description="Select a hotel near the venue.", completed=False, resourceUrl="")
#             ]
#         )
#     ],
#     3: [  # IT Equipment Setup
#         ChecklistStage(
#             id=6,
#             name="Hardware Setup",
#             order=1,
#             steps=[
#                 ChecklistStep(id=301, name="Laptop Pickup", description="Pick up your assigned laptop from IT.", completed=False, resourceUrl=""),
#                 ChecklistStep(id=302, name="Connect to VPN", description="Install and configure the VPN client.", completed=False, resourceUrl="https://vpn.example.com")
#             ]
#         ),
#         ChecklistStage(
#             id=7,
#             name="Software Installation",
#             order=2,
#             steps=[
#                 ChecklistStep(id=303, name="Install Office Suite", description="Install MS Office or LibreOffice.", completed=False, resourceUrl=""),
#                 ChecklistStep(id=304, name="Install Security Tools", description="Setup antivirus and monitoring tools.", completed=False, resourceUrl="")
#             ]
#         )
#     ],
#     4: [  # Research Project Workflow
#         ChecklistStage(
#             id=8,
#             name="Proposal Phase",
#             order=1,
#             steps=[
#                 ChecklistStep(id=401, name="Define Research Question", description="Clearly articulate the main research question.", completed=True, resourceUrl=""),
#                 ChecklistStep(id=402, name="Literature Review", description="Compile relevant academic references.", completed=False, resourceUrl="")
#             ]
#         ),
#         ChecklistStage(
#             id=9,
#             name="Execution Phase",
#             order=2,
#             steps=[
#                 ChecklistStep(id=403, name="Data Collection", description="Collect quantitative and qualitative data.", completed=False, resourceUrl=""),
#                 ChecklistStep(id=404, name="Analysis", description="Run statistical analysis on gathered data.", completed=False, resourceUrl="")
#             ]
#         ),
#         ChecklistStage(
#             id=10,
#             name="Publication Phase",
#             order=3,
#             steps=[
#                 ChecklistStep(id=405, name="Draft Paper", description="Write the first draft of the research paper.", completed=False, resourceUrl=""),
#                 ChecklistStep(id=406, name="Peer Review", description="Send the draft to peers for review.", completed=False, resourceUrl="")
#             ]
#         )
#     ]
# }

# fake_checklist_data = {
#     1: ProcessInstance(
#         id=1,
#         name="Employee Onboarding",
#         description="Complete all onboarding tasks before the first workday.",
#         category=ProcessCategory(id=1, name="Human Resources"),
#         stages=fake_stages[1]
#     ),
#     2: ProcessInstance(
#         id=2,
#         name="Business Travel Request",
#         description="Submit and prepare for an official business trip.",
#         category=ProcessCategory(id=2, name="Travel"),
#         stages=fake_stages[2]
#     ),
#     3: ProcessInstance(
#         id=3,
#         name="IT Equipment Provisioning",
#         description="Receive and set up all necessary IT equipment.",
#         category=ProcessCategory(id=3, name="IT Services"),
#         stages=fake_stages[3]
#     ),
#     4: ProcessInstance(
#         id=4,
#         name="Academic Research Project",
#         description="Guided steps for academic research from start to publication.",
#         category=ProcessCategory(id=4, name="Research"),
#         stages=fake_stages[4]
#     )
# }



# def get_next_step_id():
#     return max(
#         step.id for stages in fake_stages.values() for s in stages for step in s.steps
#     ) + 1
