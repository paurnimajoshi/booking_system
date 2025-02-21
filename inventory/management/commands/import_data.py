import os
import pandas as pd
import datetime
from django.core.management.base import BaseCommand
from inventory.models import Member, Inventory

class Command(BaseCommand):
    help = "Import members and inventory data from specified CSV files"

    def add_arguments(self, parser):
        parser.add_argument(
            'members_file', type=str, help="Path to the members CSV file"
        )
        parser.add_argument(
            'inventory_file', type=str, help="Path to the inventory CSV file"
        )

    def validate_file(self, file_path, expected_columns):
        """Check if file exists, is a valid CSV, and contains required columns."""
        if not os.path.exists(file_path):
            raise ValueError(f"File not found: {file_path}")

        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            raise ValueError(f"Error reading CSV file {file_path}: {e}")
        missing_columns = [col for col in expected_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing columns in {file_path}: {missing_columns}")

        return df

    def handle(self, *args, **kwargs):
        members_file = kwargs['members_file']
        inventory_file = kwargs['inventory_file']

        # Validate and read files
        try:
            members_df = self.validate_file(members_file, ["name", "surname", "booking_count", "date_joined"])
            inventory_df = self.validate_file(inventory_file, ["title", "description", "remaining_count", "expiration_date"])
        except ValueError as e:
            self.stderr.write(self.style.ERROR(str(e)))
            return

        # Import Members
        try:
            for _, row in members_df.iterrows():
                try:
                    date_joined = datetime.datetime.fromisoformat(row["date_joined"]).date()
                except ValueError:
                    self.stderr.write(self.style.ERROR(f"Invalid date format in members file: {row['date_joined']}"))
                    continue  # Skip invalid row
                
                Member.objects.get_or_create(
                    name=f"{row['name']} {row['surname']}",
                    email=f"{row['name'].lower()}.{row['surname'].lower()}@example.com",
                    defaults={"booking_count": row["booking_count"], "date_joined": date_joined}
                )
            self.stdout.write(self.style.SUCCESS(f"Members data imported from {members_file}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error importing members: {e}"))

        # Import Inventory
        try:
            for _, row in inventory_df.iterrows():
                try:
                    expiration_date = datetime.datetime.strptime(row["expiration_date"], "%d/%m/%y").date()
                except ValueError:
                    self.stderr.write(self.style.ERROR(f"Invalid date format in inventory file: {row['expiration_date']}"))
                    continue  # Skip invalid row
                
                Inventory.objects.get_or_create(
                    name=row["title"],
                    defaults={
                        "description": row["description"],
                        "remaining_count": row["remaining_count"],
                        "total_count": row["remaining_count"],
                        "expiration_date": expiration_date,
                    }
                )
            self.stdout.write(self.style.SUCCESS(f"Inventory data imported from {inventory_file}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error importing inventory: {e}"))
