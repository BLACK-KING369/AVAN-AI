import re


class TaskPlanner:

    def __init__(self):
        self.last_plan = []

    def create_plan(self, command):

        command = command.strip()

        if not command:
            return []

        text = command.lower()

        # ==========================================
        # WEBSITE / WEB PROJECT
        # ==========================================

        if (
            "website" in text
            or "web site" in text
            or "webpage" in text
            or "web page" in text
        ):

            plan = [
                {
                    "step": 1,
                    "action": "analyze_request",
                    "description": "Understand the requested website."
                },
                {
                    "step": 2,
                    "action": "create_project",
                    "description": "Create the website project structure."
                },
                {
                    "step": 3,
                    "action": "write_code",
                    "description": "Generate the required website code."
                },
                {
                    "step": 4,
                    "action": "verify_files",
                    "description": "Check that all required files exist."
                },
                {
                    "step": 5,
                    "action": "run_project",
                    "description": "Start the website locally."
                },
                {
                    "step": 6,
                    "action": "verify_result",
                    "description": "Verify that the project starts correctly."
                }
            ]

            self.last_plan = plan

            return plan

        # ==========================================
        # CREATE APP / PROJECT
        # ==========================================

        if (
            "create app" in text
            or "make an app" in text
            or "build an app" in text
            or "application banao" in text
        ):

            plan = [
                {
                    "step": 1,
                    "action": "analyze_request",
                    "description": "Understand the application requirements."
                },
                {
                    "step": 2,
                    "action": "create_project",
                    "description": "Create the application project."
                },
                {
                    "step": 3,
                    "action": "write_code",
                    "description": "Generate the required source code."
                },
                {
                    "step": 4,
                    "action": "verify_files",
                    "description": "Check the generated project."
                },
                {
                    "step": 5,
                    "action": "run_project",
                    "description": "Run the application."
                }
            ]

            self.last_plan = plan

            return plan

        # ==========================================
        # FILE / FOLDER TASK
        # ==========================================

        if (
            "create folder" in text
            or "make folder" in text
            or "create file" in text
            or "make file" in text
        ):

            plan = [
                {
                    "step": 1,
                    "action": "analyze_request",
                    "description": "Understand the requested file operation."
                },
                {
                    "step": 2,
                    "action": "create_files",
                    "description": "Create the requested files or folders."
                },
                {
                    "step": 3,
                    "action": "verify_files",
                    "description": "Verify the created files."
                }
            ]

            self.last_plan = plan

            return plan

        # ==========================================
        # GENERAL TASK
        # ==========================================

        plan = [
            {
                "step": 1,
                "action": "analyze_request",
                "description": "Understand the command."
            },
            {
                "step": 2,
                "action": "execute_task",
                "description": "Execute the appropriate Avan skill."
            },
            {
                "step": 3,
                "action": "verify_result",
                "description": "Verify the result."
            }
        ]

        self.last_plan = plan

        return plan


# ==========================================
# GLOBAL PLANNER
# ==========================================

planner = TaskPlanner()


def create_plan(command):

    return planner.create_plan(command)


def show_plan(command):

    plan = create_plan(command)

    print("\n🧠 AVAN TASK PLAN")
    print("=" * 40)

    for step in plan:

        print(
            f"{step['step']}. "
            f"{step['action']} → "
            f"{step['description']}"
        )

    print("=" * 40)

    return plan