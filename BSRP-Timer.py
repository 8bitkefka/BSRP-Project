import tkinter as tk
from datetime import datetime, timedelta

# --- Utility functions ---
def format_duration(seconds, include_seconds=True):
    days, remainder = divmod(int(seconds), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days > 0:
        return f"{days}d:{hours:02}:{minutes:02}" if not include_seconds else f"{days}d:{hours:02}:{minutes:02}:{seconds:02}"
    elif hours > 0 and not include_seconds:
        return f"{hours:02}:{minutes:02}"
    elif include_seconds:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    else:
        return f"{hours:02}:{minutes:02}"


def update_timers():
    now = datetime.now()

    # --- Boss Timers ---
    for boss, label, var, trigger_minute in [
        ("Right", boss_right_label, boss_right_var, 28),
        ("Left", boss_left_label, boss_left_var, 58),
    ]:
        if var.get():
            next_time = now.replace(minute=trigger_minute, second=0, microsecond=0)
            if now.minute >= trigger_minute:
                next_time += timedelta(hours=1)
            remaining = (next_time - now).total_seconds()
            label.config(text=format_duration(remaining, include_seconds=True))
        else:
            label.config(text="—")

    # --- Event Timers ---
    update_event_timer(daily_reset_label, next_daily_reset)
    update_event_timer(weekly_reset_label, next_weekly_reset)
    update_event_timer(guild_hunt_label, next_guild_hunt)
    update_event_timer(guild_dance_label, next_guild_dance)
    update_event_timer(world_boss_label, next_world_boss)

    root.after(1000, update_timers)


def update_event_timer(label, target_time):
    now = datetime.now()
    remaining = (target_time - now).total_seconds()
    if remaining <= 0:
        label.config(text="in 00:00", fg="#00BFFF")
    else:
        label.config(text=f"in {format_duration(remaining, include_seconds=False)}", fg="#00BFFF")


# --- Initialize Window ---
root = tk.Tk()
root.title("BSRP Boss & Event Timers")
root.configure(bg="#1a1a1a")
root.geometry("439x320")

# --- Title ---
tk.Label(root, text="BSRP Boss Timer", font=("Segoe UI", 14, "bold"), fg="white", bg="#1a1a1a").pack(pady=(6, 4))

# --- Boss Section ---
boss_frame = tk.Frame(root, bg="#1a1a1a")
boss_frame.pack(pady=4)

boss_right_var = tk.BooleanVar(value=True)
boss_left_var = tk.BooleanVar(value=True)

tk.Checkbutton(
    boss_frame, text="BOSS [Right]", variable=boss_right_var, bg="#1a1a1a",
    fg="white", selectcolor="#1a1a1a", activebackground="#1a1a1a",
    font=("Segoe UI", 11)
).grid(row=0, column=0, padx=5, sticky="w")
boss_right_label = tk.Label(boss_frame, text="00:00", fg="#00BFFF", bg="#1a1a1a", font=("Consolas", 12, "bold"))
boss_right_label.grid(row=0, column=1, sticky="e")

tk.Checkbutton(
    boss_frame, text="BOSS [Left]", variable=boss_left_var, bg="#1a1a1a",
    fg="white", selectcolor="#1a1a1a", activebackground="#1a1a1a",
    font=("Segoe UI", 11)
).grid(row=1, column=0, padx=5, sticky="w")
boss_left_label = tk.Label(boss_frame, text="00:00", fg="#00BFFF", bg="#1a1a1a", font=("Consolas", 12, "bold"))
boss_left_label.grid(row=1, column=1, sticky="e")

# --- Event Section ---
event_frame = tk.Frame(root, bg="#1a1a1a")
event_frame.pack(pady=2)

events = [
    ("Daily Reset:", "daily_reset_label"),
    ("Weekly Reset:", "weekly_reset_label"),
    ("Guild Hunt:", "guild_hunt_label"),
    ("Guild Dance:", "guild_dance_label"),
    ("World Boss Crusade:", "world_boss_label"),
]

for i, (label_text, var_name) in enumerate(events):
    tk.Label(event_frame, text=label_text, fg="white", bg="#1a1a1a", font=("Segoe UI", 11, "bold")).grid(row=i, column=0, sticky="w", padx=12)
    globals()[var_name] = tk.Label(event_frame, text="00:00", fg="#00BFFF", bg="#1a1a1a", font=("Consolas", 11, "bold"))
    globals()[var_name].grid(row=i, column=1, sticky="e", padx=12)

# --- Always on top ---
always_on_top_var = tk.BooleanVar(value=True)
def toggle_always_on_top():
    root.attributes("-topmost", always_on_top_var.get())

tk.Checkbutton(
    root, text="Always on top", variable=always_on_top_var, command=toggle_always_on_top,
    bg="#1a1a1a", fg="white", selectcolor="#1a1a1a", activebackground="#1a1a1a",
    font=("Segoe UI", 10)
).pack(pady=(2, 4))

# --- Set event times ---
now = datetime.now()
next_daily_reset = (now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1))
next_weekly_reset = (now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=7 - now.weekday()))
next_guild_hunt = now + timedelta(hours=1)
next_guild_dance = now + timedelta(hours=130)
next_world_boss = now + timedelta(hours=13)

toggle_always_on_top()
update_timers()
root.mainloop()
