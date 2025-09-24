"""Management command for running development server with hot reloading."""

import logging

from django.core.management.commands.runserver import Command as RunserverCommand


class Command(RunserverCommand):
    """Enhanced runserver command with additional development features."""

    help = (
        "Start the Django development server with hot reloading and enhanced debugging"
    )

    def add_arguments(self, parser):
        """Add command arguments."""
        super().add_arguments(parser)
        parser.add_argument(
            "--watchman",
            action="store_true",
            help="Use Watchman for file watching (faster)",
        )
        parser.add_argument(
            "--print-sql",
            action="store_true",
            help="Print SQL queries to console",
        )

    def handle(self, *args, **options):
        """Handle the command execution."""
        if options.get("print_sql"):
            logging.getLogger("django.db.backends").setLevel(logging.DEBUG)

        # Enable auto-reloading by default in development
        options["use_reloader"] = True

        # Set threading to True for better performance
        options["use_threading"] = True

        self.stdout.write(
            self.style.SUCCESS(
                "Starting development server with hot reloading enabled..."
            )
        )
        self.stdout.write(
            self.style.WARNING(
                "The admin panel will automatically refresh when you save files."
            )
        )

        # Call the parent runserver command
        super().handle(*args, **options)
