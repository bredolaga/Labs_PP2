from datetime import datetime, timedelta

current_date = datetime.now()
past_date = current_date - timedelta(days=5)

print("Current date:", current_date)
print("Date minus 5 days:", past_date)

